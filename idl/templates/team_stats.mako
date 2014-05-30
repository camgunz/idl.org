<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>
<%namespace name="stats" file="stats.mako"/>

<%def name="css()" filter="trim">
    ${utils.css_link("stats.css")}
</%def>

<%def name="js()" filter="trim">
    ${utils.js_link("tablesort.js")}
    ${utils.jquery_link()}
    ${utils.js_link("idl.js")}
</%def>

<%def name="main_panel()" filter="trim">
    <%
          labels = (
              'name',
              'frag_ratio',
              'flag_ratio',
              'pick_ratio',
              'frags',
              'frags_per_round',
              'touches',
              'touches_per_round',
              'captures',
              'captures_per_round',
              'picks',
              'picks_per_round',
              'pick_captures',
              'pick_captures_per_round',
          )
    %>

    <div class="box">
        <%include file="season_navbar.mako"/>
        <div class="box_body">
            <h3 class="box_body_header">Season Team Statistics</h3>
            <div class="player_stats">
                ${stats.table(
                      "player_stats",
                      "lightgreybg",
                      "lightbluebg",
                      "Team",
                      labels,
                      context["stats"]
                )}
            </div> <!-- player stats -->
        </div> <!-- box body -->
    </div> <!-- box -->
</%def>

<%def name="side_panel()" filter="trim">
    <%include file="season_select_form.mako"/>
</%def>

