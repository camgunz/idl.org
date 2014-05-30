<%namespace name="utils" file="utils.mako"/>

<%def name="display(stat, label)" filter="trim">
    <%
        if label.endswith("ratio"):
            pct = True
            factor = 100
        else:
            pct = False
            factor = 1
    %>
    % if isinstance(stat, tuple) or isinstance(stat, list):
        ${utils.ratio(stat[0], stat[1], factor=factor, percentage=pct)}
    % else:
        ${stat}
    % endif
</%def>

<%def name="table(tclass, rowstyle, colstyle, name, labels, stats)"
      filter="trim">
    <%
        if context["order_by"] in labels:
            sorted_column_index = str(labels.index(context["order_by"]))
        else:
            sorted_column_index = "0"
        sorted_column = "sortable-onload-" + sorted_column_index
        rowstyle = "rowstyle-" + rowstyle
        colstyle = "colstyle-" + colstyle
    %>
    <table class="${tclass} ${sorted_column} ${rowstyle} ${colstyle}">
        <thead>
            <tr>
                <th class="centered first_cell"></th>
                <th class="centered" colspan="3">Ratios</th>
                <th class="centered" colspan="2">Frags</th>
                <th class="centered" colspan="2">Touches</th>
                <th class="centered" colspan="2">Captures</th>
                <th class="centered" colspan="2">Picks</th>
                <th class="centered" colspan="2">PCaptures</th>
            </tr>
            <tr>
                <th class="centered first_cell sortable">${name}</th>
                <th class="centered sortable favour-reverse sortable-numeric">
                    Frag
                </th>
                <th class="centered sortable favour-reverse sortable-numeric">
                    Flag
                </th>
                <th class="centered sortable favour-reverse sortable-numeric">
                    Pick
                </th>
                <th class="centered sortable favour-reverse">T</th>
                <th class="centered sortable favour-reverse">R</th>
                <th class="centered sortable favour-reverse">T</th>
                <th class="centered sortable favour-reverse">R</th>
                <th class="centered sortable favour-reverse">T</th>
                <th class="centered sortable favour-reverse">R</th>
                <th class="centered sortable favour-reverse">T</th>
                <th class="centered sortable favour-reverse">R</th>
                <th class="centered sortable favour-reverse">T</th>
                <th class="centered sortable favour-reverse last_cell">R</th>
            </tr>
        </thead>
        <tbody>
            % for row in stats:
                <tr>
                    % for n, l in enumerate(labels):
                        % if n == 0:
                            <td class="lefted first_cell">
                                ${display(row[l], l)}
                            </td>
                        % elif n == (len(labels) - 1):
                            <td class="last_cell">${display(row[l], l)}</td>
                        % else:
                            <td>${display(row[l], l)}</td>
                        % endif
                    % endfor
                </tr>
            % endfor
        </tbody>
    </table>
</%def>

