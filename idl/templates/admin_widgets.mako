<%namespace name="utils" file="utils.mako"/>

<%def name="admin_list(module, entries, js_load_func, model=None, entry=None,
                       label=None)"
      filter="trim">
    <%
        if label:
            header = label
        else:
            if module[0] in ("A", "E", "I", "O", "U") or module[:1] == "Hi":
                art = "an"
            else:
                art = "a"
            if module.endswith("ses"):
                cutoff = 2
            else:
                cutoff = 1
            sd = "%s %s" % (art, module[:-cutoff])
            if "Team Season" in sd:
                sd = sd.replace("Team Season", "Team")
            if "And" in module:
                header = " ".join([y.rstrip("s") for y in module.split()])
            else:
                header = module.rstrip("s")
    %>
    <div id="admin_list">
        <label>Select a ${header}: </label><br/>
        <select id="admin_select" name="admin_select"
            onchange="${js_load_func}('${module}');$('admin_delete').show()">
            <option value=""></option>
            % if admin_entries:
                % for value, display in admin_entries:
                    <option value="${value}">${display}</option>
                % endfor
            % endif
        </select>
        <%
            if model:
                name = model.Admin.label
            else:
                name = context["modules_to_models"][module].Admin.label
        %>
        <button onclick="adminNew('${module}');$('admin_delete').hide()">
            New
        </button>
        <button id="admin_delete" style="display: none;"
            onclick="adminDelete('${module}', '${name}');">
            Delete
        </button>
    </div>
    <hr/>
    % if module and model and entry:
        ${admin_entry(module, model, entry, False)}
    % endif
</%def>

<%def name="admin_log_upload_form(game)" filter="trim">
    <form action="${url_for("game_logs")}" method="POST"
          enctype="multipart/form-data"
          target="game_log_data" id="game_log_upload"
          onsubmit="adminLogUploadStarted();">
        <div class="file_input">
            <label for="game_log">Select a Game Log File: </label>
            <input type="file" id="game_log" class="file" name="game_log"/>
            <input type="hidden" id="entry" name="entry"
                   value="${game.id}"/>
            <input type="hidden" id="module" name="module"
                   value="Game Log"/>
            <button id="submit_game_log" type="submit">Upload</button>
        </div>
        <div id="uploading">
            <img src="${utils.image_link("uploading.gif")}"/>
            <span id="game_log_upload_result">Uploading...</span>
        </div>
        <iframe id="game_log_data" class="file_upload" name="game_log_data"
                src="#"></iframe>
    </form>
</%def>

<%def name="base_calendar(dt, mclass=None, eid='calendar', eclass='calendar',
                          deid=None, hidden=False)">
    <%
        from calendar import Calendar
        from datetime import datetime
        dt = dt or datetime.now()
        cal = Calendar(6)
        NUMS_TO_MONTHS = [u'January', u'February', u'March', u'April', u'May',
                          u'June', u'July', u'August', u'September',
                          u'October', u'November', u'December']
        ts = "(%s, %s, %s, %s, '%s', '%s', '%s', '%s', false)" % (
            dt.year, dt.month, dt.hour, dt.minute, mclass, eid, eclass, deid
        )
        pm_invok = 'previousMonth' + ts
        nm_invok = 'nextMonth' + ts
        if mclass:
            cal_class = " ".join((mclass, eclass))
        else:
            cal_class = eclass
    %>
    % if hidden:
        <div id="${eid}" class="${cal_class}" style="display: none;">
    % endif
        <table class="calendar">
            <tr class="calendar_header">
                <th class="calendar_header_cell centered">
                    <input type="button" class="previous_month" value="<"
                     onclick="${pm_invok}"/>
                </th>
                <th class="calendar_header_cell centered" colspan="5">
                    ${NUMS_TO_MONTHS[dt.month-1]} ${dt.year}
                </th>
                <th class="calendar_header_cell centered">
                    <input type="button" class="next_month" value=">"
                     onclick="${nm_invok}"/>
                </th>
            </tr>
            <tr class="calendar_header">
                <th class="calendar_header_cell centered">Su</th>
                <th class="calendar_header_cell centered">Mo</th>
                <th class="calendar_header_cell centered">Tu</th>
                <th class="calendar_header_cell centered">We</th>
                <th class="calendar_header_cell centered">Th</th>
                <th class="calendar_header_cell centered">Fr</th>
                <th class="calendar_header_cell centered">Sa</th>
            </tr>
            % for week in cal.monthdayscalendar(dt.year, dt.month):
            <tr class="calendar_row">
            % for day in week:
            % if day == 0:
                <td class="calendar_empty_cell centered"></td>
            % elif deid is not None:
                <td class="calendar_cell centered"
            onclick="setDateTime('${deid}', ${dt.year}, ${dt.month}, ${day})">
                    ${day}
                </td>
            % else:
                <td class="calendar_cell centered">${day}</td>
            % endif
            % endfor
            </tr>
            % endfor
        </table>
        <label class="calendar">Hour: </label>
        <select id="cal_hour" onchange="setTime('${deid}')">
        % for h in [str(x).zfill(2) for x in [dt.hour] + range(0, 24)]:
            <option value="${h}">${h}</option>
        % endfor
        </select>
        <label class="calendar">Minute: </label>
        <select id="cal_minute" onchange="setTime('${deid}')">
        % for m in [str(x).zfill(2) for x in [dt.minute] + range(0, 60, 5)]:
            <option value="${m}">${m}</option>
        % endfor
        </select>
    % if hidden:
    </div>
    % endif
</%def>

<%def name="calendar(a, entry, mclass=None)" filter="trim">
    <%
    from datetime import datetime, timedelta
    temp_dt = datetime.now() + timedelta(days=1)
    dt = datetime(temp_dt.year, temp_dt.month, temp_dt.day)
    if entry:
        dt = a.get_entry_value(entry)
    eid = a.name + u'_calendar'
    eclass = u'centered calendar'
    deid = a.attribute_name
    %>
    ${base_calendar(dt, mclass, eid, eclass, deid, hidden=True)}
</%def>

<%def name="admin_modules_widget(name)" filter="trim">
    <%
        if not name.endswith('s'):
            display_name = name + u's'
        else:
            display_name = name
    %>
    <li class="admin_entry" onclick="adminList('${name}');">
        ${display_name}
    </li>
</%def>

<%def name="admin_label(a)" filter="trim">
    <label>${a.label}:</label>
</%def>

<%def name="admin_select(a, entry=None)" filter="trim">
    <%
    top_option = (u'', a.blank_value or u'')
    all_options = a.choices
    ###
    # [CG] If there's an entry and the entry has a value for this attribute, we
    #      want to display it.  Otherwise we just want to display all the
    #      choices.
    ###
    if entry:
        entry_attribute_value = a.get_entry_value(entry) or u''
        if entry_attribute_value:
            ###
            # [CG] This will be an id, or the first part of the choice.
            ###
            subsequent_options = list()
            for x, y in all_options:
                if x == entry_attribute_value:
                    top_option = (x, y)
                else:
                    subsequent_options.append((x, y))
            all_options = subsequent_options
    all_options = [top_option] + all_options
    %>
    <select id="${a.attribute_name}" name="${a.attribute_name}">
        % for x, y in all_options:
            <option value="${x}">${y}</option>
        % endfor
    </select>
</%def>

<%def name="admin_text(a, entry=None)" filter="trim">
    <% entry_attribute_value = entry and a.get_entry_value(entry) or u'' %>
    % if a.max_length is not None:
        <input type="text" id="${a.attribute_name}" name="${a.attribute_name}"
               size="30" value="${entry_attribute_value}"
               maxlength="${a.max_length}"/>
    % else:
        <input type="text" id="${a.attribute_name}" name="${a.attribute_name}"
               size="30" value="${entry_attribute_value}"/>
    % endif
</%def>

<%def name="admin_file(a, entry)" filter="trim">
</%def>

<%def name="admin_date(a, entry)" filter="trim">
</%def>

<%def name="admin_time(a, entry)" filter="trim">
</%def>

<%def name="admin_datetime(a, entry)" filter="trim">
    <%
    ts = u''
    if entry:
        dt = a.get_entry_value(entry)
        if dt:
            ts = unicode(dt.strftime('%Y-%m-%d %H:%M:%S'))
    %>
    <input type="text" maxlength="19" name="${a.attribute_name}"
           id="${a.attribute_name}" value="${ts}" size="19"
           onclick="hideAllCalendars();$('#${a.name}_calendar').show();"/>
</%def>

<%def name="admin_checkbox(a, entry=None)" filter="trim">
    % if entry and a.get_entry_value(entry):
        <input type="checkbox" id="${a.attribute_name}"
               name="${a.attribute_name}"
               value="on"
               onclick="toggleChecked(this)"/>
    % else:
        <input type="checkbox" id="${a.attribute_name}"
               name="${a.attribute_name}"
               value="off"
               onclick="toggleChecked(this)"/>
    % endif
</%def>

<%def name="admin_textarea(a, entry=None)" filter="trim">
    <% v = entry and a.get_entry_value(entry) or u'' %>
    <textarea id="${a.attribute_name}"
              name="${a.attribute_name}">${v}</textarea>
</%def>

<%def name="admin_submit(module, model, entry)" filter="trim">
    <%
    attributes = [x.attribute_name for x in model.Admin.attributes]
    attributes = u"', '".join(attributes).join([u"Array('", u"')"])
    %>
    <button class="righted" onclick="adminSet('${module}', ${attributes})">
        Save Changes
    </button>
</%def>

<%def name="admin_bottom_row(module, model, entry)" filter="trim">
    <%
    if entry:
        x = model.Admin.get_id(entry)
    else:
        x = ''
    %>
    <tr>
        <td>
            <input type="hidden" id="entry_id" name="entry_id" value="${x}"/>
        </td>
        <td>
            ${admin_submit(module, model, entry)}
        </td>
    </tr>
</%def>

<%def name="admin_table(module, model, entry)" filter="trim">
    <table id="admin_table">
        % for attribute in model.Admin.attributes:
            <tr>
                <td>${attribute.label}:</td>
                % if attribute.field_type == 'select':
                    <td>${admin_select(attribute, entry)}</td>
                % elif attribute.field_type == 'text':
                    <td>${admin_text(attribute, entry)}</td>
                % elif attribute.field_type == 'date':
                    <td>${admin_date(attribute, entry)}</td>
                % elif attribute.field_type == 'time':
                    <td>${admin_time(attribute, entry)}</td>
                % elif attribute.field_type == 'datetime':
                    <td>${admin_datetime(attribute, entry)}</td>
                % elif attribute.field_type == 'checkbox':
                    <td>${admin_checkbox(attribute, entry)}</td>
                % elif attribute.field_type == 'textfield':
                    <td>${admin_textarea(attribute, entry)}</td>
                % elif attribute.field_type == 'file':
                    <td>${admin_file(attribute, entry)}</td>
                % endif
            </tr>
        % endfor
        ${admin_bottom_row(module, model, entry)}
    </table>
</%def>

<%def name="admin_entry(module, model, entry, show_new=False)" filter="trim">
    <%
        x = ('date', 'time', 'datetime')
        mclass = "_".join((module.lower().replace(" ", "_"), "calendar"))
    %>
    ${admin_table(module, model, entry)}
    % for att in [a for a in model.Admin.attributes if a.field_type in x]:
        ${calendar(att, entry, mclass)}
    % endfor
</%def>

