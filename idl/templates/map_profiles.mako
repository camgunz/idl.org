<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="css()" filter="trim">
    ${utils.css_link("box_scores.css")}
    ${utils.css_link("map_profiles.css")}
</%def>

<%def name="js()" filter="trim">
</%def>

<%def name="display_map_stats(s)" filter="trim">
    <%
        import decimal
        decimal.setcontext(decimal.ExtendedContext)
        decimal.prec = 4

        def divide(x, y, cap=None):
            result = decimal.Decimal(x) / decimal.Decimal(y)
            if cap is not None and result > cap:
                return cap
            return result
    %>
    <table class="map_stats">
        <tr>
            <td>Rounds Played:</td>
            <td>${s["round_count"]}</td>
        </tr>
        <tr>
            <td>Average Duration:</td>
            <td>
                % if s["total_round_duration"] < 600 or s["timed_round_count"] == 0:
                    unknown
                % else:
                    ${utils.format_seconds(divide(
                        s["total_round_duration"], s["timed_round_count"],
                        cap=600
                    ))}
                % endif
            </td>
        </tr>
        <tr>
            <td>Frags / Round:</td>
            <td>
                ${"%.3f" % (divide(
                    s["total_frags"], s["round_count"]
                ))}
            </td>
        </tr>
        <tr>
            <td>Suicides / Round:</td>
            <td>
                ${"%.3f" % (divide(
                    s["total_suicides"], s["round_count"]
                ))}
            </td>
        </tr>
        <tr>
            <td>Touches / Round:</td>
            <td>
                ${"%.3f" % (divide(
                    s["total_flag_touches"], s["round_count"]
                ))}
            </td>
        </tr>
        <tr>
            <td>Picks / Round:</td>
            <td>
                ${"%.3f" % (divide(
                    s["total_flag_picks"], s["round_count"]
                ))}
            </td>
        </tr>
        <tr>
            <td>Captures / Round:</td>
            <td>
                ${"%.3f" % (divide(
                    s["total_flag_captures"], s["round_count"]
                ))}
            </td>
        </tr>
        <tr>
            <td>Pick Captures / Round:</td>
            <td>
                ${"%.3f" % (divide(
                    s["total_flag_pick_captures"], s["round_count"]
                ))}
            </td>
        </tr>
        <tr>
            <td>Flag %:</td>
            <td>
                ${utils.ratio(
                    s["total_flag_captures"], s["total_flag_touches"]
                )}
            </td>
        </tr>
        <tr>
            <td>Pick %:</td>
            <td>
                ${utils.ratio(
                    s["total_flag_pick_captures"], s["total_flag_picks"]
                )}
            </td>
        </tr>
        <tr>
            <td>Average Capture Time:</td>
            <td>
                ${utils.format_seconds(divide(
                    s["total_flag_run_time"], s["timed_flag_captures"]
                ))}
            </td>
        </tr>
    </table>
</%def>

<%def name="main_panel()" filter="trim">
    <div class="box">
        <%include file="profiles_navbar.mako"/>
        <div class="box_body">
            <%
                screenshot = context["map"].screenshot[0].absolute_url
                s = context["stats"]
            %>
            <div class="screenshot">
                <img class="screenshot" src="${screenshot}"/>
            </div>
            <h3 class="map_label">${context["map"].name}</h3>
            <div class="map_stats">
                % if context["stats"]:
                    ${display_map_stats(context["stats"])}
                % else:
                    No Stats
                % endif
            </div> <!-- map stats -->
            ## <h3 class="wad_label">${context["map"].wad.full_name}</h3>
        </div> <!-- box body -->
    </div> <!-- box -->
</%def>

<%def name="side_panel()" filter="trim">
    <div class="box">
        <h3 class="box_header">WADs</h3>
        <div class="box_body">
            % for wad in context["wads"]:
                <% wn = wad.name %>
                <div>
                    <a href="${url_for("wads", wad_name=wn)}">${wn}</a>
                </div>
            % endfor
        </div> <!-- box body -->
    </div> <!-- box -->
    <div class="box">
        <h3 class="box_header">Maps</h3>
        <div class="box_body">
            % for map in context["maps"]:
                <%
                    wn = map.wad.name
                    mn = map.number
                    mm = map.name
                %>
                <div>
                    <a href="${url_for("maps", wad_name=wn, map_number=mn)}">
                        ${mm}
                    </a>
                </div>
            % endfor
        </div> <!-- box body -->
    </div> <!-- box -->
</%def>

