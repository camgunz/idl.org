This is the source for intldoomleague.org.  It's written using Python, 
Mako (including XHTML), Javascript, CSS and SQL.  It requires ZDStack (the
most recent version from SVN), boto, saadmin (something else I wrote), Flask,
SMF, and PostgreSQL.  Postgres isn't a hard requirement, it's just that saadmin
doesn't work with anything else right now.  Adding support is trivial, but
more effort than none so I haven't done it.  Also MySQL won't store anything
smaller than a second in its datetime/time fields, so good luck there.

<This is in LICENSE as well>

IDL.org is in the public domain, so feel free to do whatever you want with it.
Note that original copyright holders still retain their copyrights, so the
graphics and screenshots are still copyright their creators.  Also there are
some included things, like Javascript libraries, etc. that are straight out of
other projects, so you must abide by whatever their licensing is as well.

