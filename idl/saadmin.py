################################################################################
#                                                                              #
# saadmin.py                                                                   #
#                                                                              #
# Copyright (c) 2009 Charles Gunyon (MIT License)                              #
#                                                                              #
# Permission is hereby granted, free of charge, to any person obtaining a copy #
# of this software and associated documentation files (the "Software"), to     #
# deal in the Software without restriction, including without limitation the   #
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or  #
# sell copies of the Software, and to permit persons to whom the Software is   #
# furnished to do so, subject to the following conditions:                     #
#                                                                              #
# The above copyright notice and this permission notice shall be included in   #
# all copies or substantial portions of the Software.                          #
#                                                                              #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR   #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,     #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER       #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING      #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS #
# IN THE SOFTWARE.                                                             #
#                                                                              #
################################################################################

"""

saadmin.py processes SQLAlchemy tables and models, adding an 'Admin' class to
these models that contains information on the model and its attributes.  In
turn, generating forms from the model should be much easier.

    import saadmin

    from awesome_project.model import meta, iterable_tables, iterable_models

    saadmin.set_global_session(meta.Session)
    saadmin.set_tables(iterable_tables)
    saadmin.set_models(iterable_models)

    saadmin.activate_all()

Note that the iterables of tables and models must have the same amount of
members, and that they must line up (i.e., cars_table is at the same index as
Car, and so on).

saadmin does this by monkeypatching an 'Admin' class into each of your models.
You can customize some behavior by defining this class in your models yourself,
for example: 

    import saadmin
    import awesome_project

    def Season(object):

        Admin = saadmin.ModelAdmin(
            column_attributes = {
                'season': {
                    'get_choices': lambda season: [
                        (u'winter', u'Winter'),
                        (u'summer', u'Summer')
                    ]
                    'get_label': lambda season: u'Season'
                }
                'year': {
                    'max_length': 4
                }
                'apocalypse_type': {
                    'blank_value': u'Barely escaped disaster',
                    'get_choices': lambda season: [
                        (u'flood', u'Flood'),
                        (u'plague', u'Plague'),
                        (u'thermonuclear_warfare', u'Thermonuclear warfare'),
                    ]
                }
            }
        )

So in this instance there's a Season model with three attributes, season, year
and apocalypse_type.  Each of these attributes is tweaked slightly:

    Season.season should only be one of two choices, Winter or Summer.
    Season.season's control should be displayed with a label 'Season'
    Season.year's control should only allow 4 characters in its field
    Season.apocalypse_type should only be one of three choices, with its blank
        option displayed as u'Barely escaped disaster'

Note that the given functions need to be defined as though they were instance
methods.  This allows you to access the Attribute, its ModelAdmin
(Attribute.admin), and its model (Attribute.admin.model) from your function.
Very handy!

Here are all of the keyword arguments that the initializer supports:

    get_session: a callable that returns a SQLAlchemy session instance
    get_label:   a callable that returns a Unicode string that will be used
                   as the model's label
    get_name:    a callable that returns returns a Unicode string that will be
                   used as the model's name
    get_all:     a callable that returns all instances of the augmented model
    get_choices: a callable that returns a list of 2-Tuples (id, value) for all
                   instances of the augmented model
    get_id:      a callable that, given an entry, returns the value of its
                   primary key
    get_display: a callable that, given an entry, returns a Unicode string that
                   will be used when displaying the entry
    get_entry:   a callable that, given a proper value for the model's primary
                   primary key column, returns the entry matching that value
    blank_value: a Unicode string that will be used as the blank option name

Here are all of the options that the 'column_attributes' keyword argument
supports:

    get_label:   a callable that returns a Unicode string used as the label
    get_choices: a callable that returns a list of 2-Tuples (id, value) of all
                   valid choices
    parser:      a callable used to parse (and thus validate) field values
    field_type:  a string indicating the type of field to use
    blank_value: a Unicode string that will be used as the blank option name
    max_length:  the maximum length of the (assumed) text entry field

Note that when you define 'get_choices', you are forcing the field type to a
<select>, and when you define 'max_length', you are forcing the field type to
an <input type="text">.  For this reason you may not define both, as they're
mutually exclusive.

Additionally, you can customize how your models are fetched from the database.
Normally this method is used:

    model.Admin.session.query(model.Admin.model).all()

Of course, this does no sorting or filtering or joining or anything!  So if you
wanted your models displayed in a particular order:

    import saadmin
    import sqlalchemy

    from awesome_project.model import meta, models

    def seasons():
        q = meta.Session.query(models.Season)
        return q.order_by(sqlalchemy.and_(
            models.Season.year.asc(),
            models.Season.season.desc()
        ))

    saadmin.set_getter(models.Season, seasons)

Note that the seasons() function only returns the Query instance, not the
results of the query.  This is for maximum flexibility inside of saadmin, even
though I currently don't do anything with it.

Lastly, I recommend starting out without defining any Admin classes, and then
adding them if you want/need to modify anything.

Stuff that is currently unsupported:

Composite primary keys.  I suppose I could make an argument against them, but
I'm not that opinionated.  saadmin was designed around the idea of a single
primary key field; if other fields are unique they should just have UNIQUE
indexes (that's all a primary_key is anyway).  If you have types that are only
unique based on multiple fields, then that's just outside the scope of saadmin.

The other things that are outside the scope of saadmin are (so far):

    Composite foreign keys  
    Custom SQLAlchemy types

Database-centric types.  Some from PostgreSQL are supported because I need
them, but not all, and nothing from other DB engines.  I only ran into this
using reflection, should be smooth sailing otherwise.

"""

import types
import decimal
import logging
import weakref
import datetime
import operator

import sqlalchemy as sa

def sqlalchemy_version_is_at_least(major=0, minor=0, patch=0):
    a, b, c = [int(x) for x in sa.__version__.split('.')]
    if a < major:
        return False
    if b < minor:
        return False
    if c < patch:
        return False
    return True

make_im = lambda i, f: types.MethodType(f, i, i.__class__)

def get_foreign_key_table(column):
    if sqlalchemy_version_is_at_least(minor=7):
        return tuple(column.foreign_keys)[0].column.table
    else:
        return column.foreign_keys[0].column.table

__SESSION = None
__MAPPERS = list()
__MODELS_TO_GETTERS = dict()
__MODELS_TO_DISPLAY = dict()

def set_global_session(session):
    global __SESSION
    __SESSION = session

def get_global_session():
    return __SESSION

def set_models(models):
    global __MAPPERS
    for model in models:
        mapper = sa.orm.class_mapper(model)
        if mapper not in __MAPPERS:
            __MAPPERS.append(mapper)

def get_models():
    return [m.class_ for m in __MAPPERS]

def get_tables():
    return [m.mapped_table for m in __MAPPERS]

def models_to_tables():
    return dict(zip(get_models(), get_tables()))

def tables_to_models():
    return dict(zip(get_tables(), get_models()))

def set_getter(model, getter):
    global __MODELS_TO_GETTERS
    __MODELS_TO_GETTERS[model] = getter

def models_to_getters():
    return dict(__MODELS_TO_GETTERS.items())

def set_display(model, display):
    global __MODELS_TO_DISPLAY
    __MODELS_TO_DISPLAY[model] = display

def models_to_display():
    return dict(__MODELS_TO_DISPLAY.items())

def labelize(n):
    if n.endswith('_id'):
        n = n[:-3]
    if n.startswith('idl_'):
        n = n[4:]
    label = []
    tokens = n.split(u'_')
    num_tokens = len(tokens)
    last_token = num_tokens - 1
    for i in range(len(tokens)):
        token = tokens[i]
        if i == 0 or i == last_token or i not in (u'and', 'or', 'nor'):
            label.append(token.capitalize())
        else:
            label.append(token)
    out = u' '.join(label)
    if u'And' in out:
        return out
    elif not out.endswith(u'ss'):
        out = out.rstrip(u's')
        if out.endswith(u'se'):
            out = out[:-1]
        return out
    else:
        return out

def iso_date(s):
    if s in (u'', ''):
        return None
    try:
        dt = datetime.datetime.strptime(s, '%Y-%m-%d')
        return datetime.date(dt.year, dt.month, dt.day)
    except ValueError:
        raise ValueError(u'Dates must be in "%Y-%m-%d" format')

def iso_time(s):
    if s in (u'', ''):
        return None
    formats = (
        '%H:%M:%S',
        '%H:%M:%S.%f'
    )
    if '.' in s:
        dt_format = formats[1]
    else:
        dt_format = formats[0]
    try:
        return datetime.datetime.strptime(s, dt_format)
    except ValueError:
        raise ValueError(u'Times must be in either "' + \
            u'" or "'.join(formats) + \
            u'" format'
        )

def iso_datetime(s):
    if s in (u'', ''):
        return None
    formats = (
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f'
    )
    if '.' in s:
        dt_format = formats[1]
    else:
        dt_format = formats[0]
    try:
        return datetime.datetime.strptime(s, dt_format)
    except ValueError:
        raise ValueError(u'Timestamps must be in either "' + \
            u'" or "'.join(formats) + \
            u'" format'
        )

###
# [CG] These should be rolled into ColumnTypes and explicitly associated with
#      the types they should parse.  I'll do that later I think.
###

def default_parser(s):
    if s in (u'', ''):
        return None
    return s

def formbool(s):
    return s == 'on'

def integer(s):
    if s in (u'', ''):
        return None
    return int(s)

def dec(s):
    if s in (u'', ''):
        return None
    return decimal.Decimal(s)

def flt(s):
    if s in (u'', ''):
        return None
    return float(s)

def string(s):
    if s in (u'', ''):
        return None
    return str(s)

def unc(s):
    if s in (u'', ''):
        return None
    return unicode(s)

class ColumnTypes(object):


    if sqlalchemy_version_is_at_least(minor=6):
        binary_types = [
            sa.types.Binary,
            sa.types.LargeBinary,
            sa.types.BINARY,
            sa.types.BLOB,
            sa.types.CLOB,
            sa.types.VARBINARY
        ]
    else:
        binary_types = [
            sa.types.Binary,
            sa.types.BLOB,
            sa.types.CLOB,
        ]

    if sqlalchemy_version_is_at_least(minor=6):
        boolean_types = [
            sa.types.Boolean,
            sa.types.BOOLEAN,
            sa.types.BOOLEANTYPE
        ]
    else:
        boolean_types = [
            sa.types.Boolean,
            sa.types.BOOLEAN,
        ]

    date_types = [
        sa.types.Date,
        sa.types.DATE
    ]

    time_types = [
        sa.types.Time,
        sa.types.TIME
    ]

    date_time_types = [
        sa.types.DateTime,
        sa.types.DATETIME,
        sa.types.TIMESTAMP
    ]

    if sqlalchemy_version_is_at_least(minor=6):
        integer_types = [
            sa.types.Integer,
            sa.types.BigInteger,
            sa.types.SmallInteger,
            sa.types.INT,
            sa.types.INTEGER,
            sa.types.BIGINT,
            sa.types.SMALLINT
        ]
    else:
        integer_types = [
            sa.types.Integer,
            sa.types.SmallInteger,
            sa.types.INT,
            sa.types.INTEGER,
            sa.types.SMALLINT
        ]

    float_types = [
        sa.types.Float,
        sa.types.FLOAT
    ]

    numeric_types = [
        sa.types.Numeric,
        sa.types.DECIMAL,
        sa.types.NUMERIC
    ]

    null_types = [
        sa.types.NULLTYPE,
        sa.types.NoneType,
        sa.types.NullType
    ]


    if sqlalchemy_version_is_at_least(minor=6):
        string_types = [
            sa.types.String,
            sa.types.NCHAR,
            sa.types.NVARCHAR,
            sa.types.VARCHAR
        ]
    else:
        string_types = [
            sa.types.String,
            sa.types.NCHAR,
            sa.types.VARCHAR
        ]

    text_types = [
        sa.types.Text,
        sa.types.TEXT
    ]

    unicode_types = [
        sa.types.Unicode,
    ]

    unicode_text_types = [
        sa.types.UnicodeText
    ]

    interval_types = [
        sa.types.Interval
    ]

    if sqlalchemy_version_is_at_least(minor=6):
        enumeration_types = [
            sa.types.Enum
        ]
    else:
        enumeration_types = [
        ]

    mutable_types = [
    ]

    bit_types = [
    ]

    misc_types = [
    ]

    @staticmethod
    def add_postgres_column_types():
        if sqlalchemy_version_is_at_least(minor=6):
            from sqlalchemy.dialects import postgresql as pg
            ColumnTypes.bit_types.append(pg.base.BIT)
            ColumnTypes.binary_types.append(pg.base.BYTEA)
            ColumnTypes.enumeration_types.append(pg.base.ENUM)
            ColumnTypes.interval_types.append(pg.base.INTERVAL)
            ColumnTypes.mutable_types.append(pg.base.ARRAY)
            ColumnTypes.misc_types.extend([
                pg.base.CIDR,
                pg.base.INET,
                pg.base.MACADDR,
                pg.base.UUID
            ])
            ColumnTypes.float_types.extend([
                pg.base.DOUBLE_PRECISION,
                pg.base.REAL
            ])
        else:
            from sqlalchemy.databases import postgres as pg
            ColumnTypes.bit_types.append(pg.PGBit)
            ColumnTypes.binary_types.append(pg.PGBinary)
            ColumnTypes.date_types.append(pg.PGDate)
            ColumnTypes.interval_types.append(pg.PGInterval)
            ColumnTypes.mutable_types.append(pg.PGArray)
            ColumnTypes.string_types.append(pg.PGString)
            ColumnTypes.text_types.append(pg.PGText)
            ColumnTypes.float_types.extend([
                pg.PGDoublePrecision,
            ])
            ColumnTypes.integer_types.extend([
                pg.PGInteger,
                pg.PGSmallInteger
            ])
            ColumnTypes.misc_types.extend([
                pg.PGCidr,
                pg.PGInet,
                pg.PGMacAddr,
                pg.PGUuid
            ])

class Attribute(object):

    valid_types = ('select', 'text', 'checkbox', 'textfield', 'file',
                   'datetime', 'date', 'time')

    def __default_get_label(self):
        return labelize(self.admin.table.c[self.name].name)

    def __init__(self, admin, name, **kwargs):
        self.admin = admin
        self.name = name
        if kwargs['field_type'] not in self.valid_types:
            raise ValueError("Invalid field type '%s'" % (kwargs['field_type']))
        if 'get_label' in kwargs:
            self._get_label = make_im(self, kwargs['get_label'])
        else:
            self._get_label = self.__default_get_label
        self._get_choices = \
                make_im(self, kwargs.get('get_choices', lambda self_: list()))
        if not 'parser' in kwargs:
            kwargs['parser'] = default_parser
        self.kwargs = kwargs
        self.field_type = kwargs['field_type']
        self.blank_value = kwargs.get('blank_value', None)
        self.max_length = kwargs.get('max_length', None)

    @property
    def label(self):
        return self._get_label()

    @property
    def choices(self):
        out = self._get_choices()
        return out

    @property
    def attribute_name(self):
        return u'new_' + self.name

    def get_entry_value(self, entry):
        return entry.__getattribute__(self.name)
        
    def set_entry_value(self, entry, new_values):
        if self.attribute_name in new_values:
            new_value = new_values[self.attribute_name]
            try:
                new_value = self.kwargs['parser'](new_value)
            except TypeError, e:
                es = str(e) + '; got %s, type %s - parser is %r' % (
                    new_value,
                    type(new_value),
                    self.kwargs['parser']
                )
                raise Exception(es)
            if new_value in (u'', ''):
                if 'parser' in self.kwargs:
                    raise Exception('Got blank value for %s, parser is %r' % (
                        self.name, self.kwargs['parser']
                    ))
                else:
                    raise Exception('Got blank value for %s, no parser' % (
                        self.name
                    ))
            try:
                entry.__setattr__(self.name, new_value)
                return entry
            except TypeError, e:
                es = str(e) + '; got %s, type %s - parser is %r' % (
                    new_value, type(new_value), self.kwargs['parser']
                )
            raise Exception(es)

class ModelAdmin(dict):

    def __default_get_label(self):
        return labelize(self.table.name)

    def __default_get_name(self):
        return self.label.lower() + u'_' + self.primary_key_name

    def __default_get_all(self):
        m2g = models_to_getters()
        if self.model in m2g:
            out = m2g[self.model](self).all()
        else:
            out = self.session.query(self.model).all()
        return out

    def __default_get_choices(self):
        return [(self.get_id(x), self.get_display(x)) for x in self.all]

    def __default_get_id(self, entry):
        return operator.attrgetter(self.primary_key_name)(entry)

    def __default_get_entry(self, entry_id):
        return self.session.query(self.model).get(entry_id)

    def __init__(self, **kwargs):
        if 'get_session' in kwargs:
            self._get_session = make_im(self, kwargs['get_session'])
        else:
            self._get_session = get_global_session
        if 'get_label' in kwargs:
            self._get_label = make_im(self, kwargs['get_label'])
        else:
            self._get_label = self.__default_get_label
        if 'get_name' in kwargs:
            self._get_name = make_im(self, kwargs['get_name'])
        else:
            self._get_name = self.__default_get_name
        if 'get_all' in kwargs:
            self._get_all = make_im(self, kwargs['get_all'])
        else:
            self._get_all = self.__default_get_all
        if 'get_choices' in kwargs:
            self._get_choices = make_im(self, kwargs['get_choices'])
        else:
            self._get_choices = self.__default_get_choices
        if 'get_display' in kwargs:
            f = kwargs['get_display']
        else:
            def f(self_, x):
                m2d = models_to_display()
                df = m2d.get(self.model, lambda self__, x: unicode(x))
                out = df(self_ ,x)
                return out
        self.get_display = make_im(self, f)
        if 'get_id' in kwargs:
            self.get_id = make_im(self, kwargs['get_id'])
        else:
            self.get_id = self.__default_get_id
        if 'get_entry' in kwargs:
            self.get_entry = make_im(self, kwargs['get_entry'])
        else:
            self.get_entry = self.__default_get_entry
        self.blank_value = kwargs.get('blank_value', None)
        self.attributes = list()
        dict.__init__(self, kwargs.get('column_attributes', dict()))

    def _get_primary_key_name(self):
        pkns = [x.name for x in self.table.primary_key]
        num_keys = len(pkns)
        if num_keys > 1:
            raise ValueError(u"Can't currently handle Composite Primary Keys.")
        elif not num_keys:
            raise ValueError(u'Models must have a Primary Key defined!')
        return pkns[0]

    @property
    def primary_key_name(self):
        return self._get_primary_key_name()

    @property
    def session(self):
        return self._get_session()

    @property
    def label(self):
        return self._get_label()

    @property
    def name(self):
        return self._get_name()

    @property
    def all(self):
        out = self._get_all()
        return out

    @property
    def choices(self):
        out = self._get_choices()
        return out

    def new_entry(self, new_values=None):
        entry = self.model()
        if new_values is not None:
            for x in self.attributes:
                x.set_entry_value(entry, new_values)
        self.session.add(entry)
        self.session.commit()
        return entry

    def get_values(self, entry_id):
        entry = self.get_entry(entry_id)
        return [x.get_entry_value(entry) for x in self.attributes]

    def set_values(self, entry_id, new_values):
        entry = self.get_entry(entry_id)
        for x in self.attributes:
            x.set_entry_value(entry, new_values)
        self.session.add(entry)
        self.session.commit()
        return entry

    def delete_entry(self, entry_id):
        entry = self.get_entry(entry_id)
        self.session.delete(entry)
        self.session.commit()

    def get_attribute_args(self):
        return dict(
            get_label   = lambda att_self: self.label,
            field_type  = 'select',
            get_choices = lambda att_self: self.choices,
            blank_value = self.blank_value
        )

def activate(table, model):
    if not hasattr(model, 'Admin'):
        model.Admin = ModelAdmin()
    if not hasattr(model.Admin, 'table'):
        model.Admin.table = table
    if not hasattr(model.Admin, 'model'):
        model.Admin.model = model
    for column in table.columns:
        kwargs = dict()
        if column.foreign_keys and \
           column.foreign_keys.issubset(table.foreign_keys) and \
           get_foreign_key_table(column) in tables_to_models():
            fm = tables_to_models()[get_foreign_key_table(column)]
            att_admin = fm.Admin
            kwargs.update(fm.Admin.get_attribute_args())
        else:
            att_admin = model.Admin
            column_type = type(column.type)
            if column_type in ColumnTypes.string_types:
                kwargs['field_type'] = 'text'
                kwargs['parser'] = string
                kwargs['max_length'] = column.type.length
            elif column_type in ColumnTypes.unicode_types:
                kwargs['field_type'] = 'text'
                kwargs['parser'] = unc
                kwargs['max_length'] = column.type.length
            elif column_type in ColumnTypes.text_types:
                kwargs['field_type'] = 'textfield'
                kwargs['parser'] = string
            elif column_type in ColumnTypes.unicode_text_types:
                kwargs['field_type'] = 'textfield'
                kwargs['parser'] = unc
            elif column_type in ColumnTypes.integer_types:
                kwargs['field_type'] = 'text'
                kwargs['parser'] = integer
            elif column_type in ColumnTypes.numeric_types:
                kwargs['field_type'] = 'text'
                kwargs['parser'] = dec
            elif column_type in ColumnTypes.float_types:
                kwargs['field_type'] = 'text'
                kwargs['parser'] = flt
            elif column_type in ColumnTypes.date_time_types:
                kwargs['field_type'] = 'datetime'
                kwargs['max_length'] = 19
                kwargs['parser'] = iso_datetime
            elif column_type in ColumnTypes.date_types:
                kwargs['field_type'] = 'date'
                kwargs['max_length'] = 10
                kwargs['parser'] = iso_date
            elif column_type in ColumnTypes.time_types:
                kwargs['field_type'] = 'time'
                kwargs['max_length'] = 8
                kwargs['parser'] = iso_time
            elif column_type in ColumnTypes.interval_types:
                kwargs['field_type'] = 'text'
                kwargs['parser'] = datetime.timedelta
            elif column_type in ColumnTypes.boolean_types:
                kwargs['field_type'] = 'checkbox'
                kwargs['parser'] = formbool
            elif column_type in ColumnTypes.binary_types:
                kwargs['field_type'] = 'file'
            else:
                es = u'Unsupported column type %r, table %s, column %s'
                raise Exception(es % (column.type, table, column))
        if column.name in model.Admin:
            cp = model.Admin[column.name]
            if 'get_choices' in cp and 'max_length' in cp:
                es =  u"Can't define both 'get_choices' and "
                es += u"'max_length' on an attribute"
                raise ValueError(es)
            kwargs.update(cp)
            if 'get_choices' in kwargs:
                kwargs['field_type'] = 'select'
            elif 'max_length' in kwargs:
                kwargs['field_type'] = 'text'
        att = Attribute(att_admin, column.name, **kwargs)
        model.Admin.attributes.append(att)

def activate_all():
    t_and_m = zip(get_tables(), get_models())
    for table, model in t_and_m:
        if not hasattr(model, 'Admin'):
            model.Admin = ModelAdmin()
        model.Admin.table = table
        model.Admin.model = model
    for table, model in t_and_m:
        activate(table, model)

if __name__ == "__main__":
    ColumnTypes.add_postgres_column_types()

