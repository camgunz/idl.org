<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>
<%namespace name="stats" file="stats.mako"/>

<%def name="css()" filter="trim">
    ${utils.css_link("leaderboards.css")}
</%def>

<%def name="js()" filter="trim">
    ${utils.jquery_link()}
    ${utils.js_link("idl.js")}
</%def>

<%def name="main_panel()" filter="trim">
    <%
        labels_to_headers_groups = (
            (
                ("captures_per_round",      "Flag Captures per Round"),
                ("pick_captures_per_round", "Flag Pick Captures per Round")
            ),
            (
                ("touches_per_round",       "Flag Touches per Round"),
                ("picks_per_round",         "Flag Picks per Round")
            ),
            (
                ("flag_ratio",              "Flag Ratio"),
                ("pick_ratio",              "Flag Pick Ratio")
            ),
            (
                ("touches",                 "Flag Touches"),
                ("picks",                   "Flag Picks")
            ),
            (
                ("captures",                "Flag Captures"),
                ("pick_captures",           "Flag Pick Captures")
            ),
            (
                ("frags_per_round",         "Frags per Round"),
                ("returns_per_round",       "Flag Returns per Round")
            ),
            (
                ("frag_ratio",              "Frag Ratio"),
                ("return_ratio",            "Flag Return Ratio")
            ),
            (
                ("frags",              "Frags"),
                ("returns",            "Flag Returns"),
            )
        )
        leaders = context["leaders"]
    %>
    <div class="box">
        <%include file="season_navbar.mako"/>
        <div class="box_body">
            <h3 class="box_body_header">Regular Season Leaders</h3>
            <div class="stat_content">
                % for labels_to_headers in labels_to_headers_groups:
                    <div class="stat_row">
                        % for label, header in labels_to_headers:
                            <div class="stat_box">
                                <div>
                                    <h4 class="centered">
                                        <a href="${url_for("season_player_stats", order_by=label)}"
                                           alt="Show all ${header}"
                                        >${header}</a>
                                    </h4>
                                </div>
                                <hr class="stat_heading_separator"/>
                                <table class="stat_leaders">
                                    % for name, stat in leaders[label][:8]:
                                        <tr>
                                            <td class="lefted">${name}</td>
                                            <td class="righted">
                                                ${stats.display(stat, label)}
                                            </td>
                                        </tr>
                                    % endfor
                                </table>
                            </div>
                        % endfor
                    </div>
                % endfor
            </div> <!-- stat content -->
        </div> <!-- box body -->
    </div> <!-- box -->
</%def>

<%def name="side_panel()" filter="trim">
    <%include file="season_select_form.mako"/>
</%def>

