<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="css()" filter="trim">
    ${utils.css_link("box_scores.css")}
    ${utils.css_link("standings.css")}
</%def>

<%def name="js()" filter="trim">
    ${utils.js_link("tablesort.js")}
    ${utils.jquery_link()}
    ${utils.js_link("idl.js")}
</%def>

<%def name="display_roster(team)">
    <%
        captain = team.get_captain_for_season(context["session"]["season"])
        players = team.get_players_for_season(context["session"]["season"])
        if captain is None:
            if len(players) < 1:
                captain = None
                players = []
            else:
                captain = players[0]
                players = players[1:]
        else:
            players = [x for x in players if x != captain]
    %>
    ${", ".join([x.name for x in [captain] + players if x])}
</%def>

<%def name="team_row(team, conference, division, background)">
    <%
        team_stats = team.get_regular_season_info(context["session"]["season"])
        wins = team_stats["wins"]
        losses = team_stats["losses"]
        ties = team_stats["ties"]
        streak = team_stats["streak"]
        pct = team_stats["win_percentage"]
        conf_record = team.get_conference_record(context["session"]["season"], conference, division)
        div_record = team.get_division_record(context["session"]["season"], division)
    %>
    <tr class="${background}">
        <td class="lefted" width="370">
            <div class="standings_team_name">
                %if team.clinched_homefield_for_season(context["session"]["season"]):
                    ${team.name} (${team.tag}) (z)
                %elif team.clinched_division_for_season(context["session"]["season"]):
                    ${team.name} (${team.tag}) (y)
                %elif team.clinched_playoffs_for_season(context["session"]["season"]):
                    ${team.name} (${team.tag}) (x)
                %else:
                    ${team.name} (${team.tag})
                %endif
            </div>
            <div class="standings_team_members">
                ${display_roster(team)}
            </div>
        </td>
        <td class="centered" width="35">${wins}</td>
        <td class="centered" width="30">${losses}</td>
        <td class="centered" width="30">${ties}</td>
        <td class="centered" width="50">${pct}%</td>
        <td class="centered" width="60">${streak}</td>
        <td class="centered" width="50">
            ${u"-".join([str(x) for x in div_record])}
        </td>
        <td class="centered" width="65">
            ${u"-".join([str(x) for x in conf_record])}
        </td>
    </tr>
</%def>

<%def name="main_panel()" filter="trim">
<%
    def make_gen(x):
        while True:
            for y in x:
                yield y
    backgrounds = make_gen(("idc", "wdc"))
%>

<div class="box">
    <%include file="season_navbar.mako"/>
    <div class="box_body">
        % for conf in context["conferences"]:
            <%
                background = backgrounds.next()
                cls="sortable-numeric favour-reverse"
            %>
            <h3 class="box_body_header">${conf.name}</h3>
            % for div in context["conferences"][conf]:
                <table border="0" align="center" cellpadding="0" cellspacing="0"
                       class="sortable-onload-4 no-arrow standings">
                    <thead>
                        <tr>
                            <th class="sortable-text centered" width="370">
                                ${conf.short_name} ${div.name}
                            </th>
                            <th class="${cls}" width="35">W</th>
                            <th class="${cls}" width="30">L</th>
                            <th class="${cls}" width="30">T</th>
                            <th class="${cls}" width="50">PCT</th>
                            <th class="sortable-text" width="60">STRK</th>
                            <th class="sortable-text" width="50">DIV</th>
                            <th class="sortable-text" width="65">CONF</th>
                        </tr>
                    </thead>
                    <tbody>
                        % for team in context["conferences"][conf][div]:
                            ${team_row(team, conf, div, background)}
                        % endfor
                    </tbody>
                </table>
            % endfor
        % endfor
    </div> <!-- box body -->
    <div class="box_footer" id="explanation">
        <div>Standings are updated with the completion of each game</div>
        <div>x - Clinched playoff berth | y - Clinched division title | z - Clinched homefield advantage</div>
    </div> <!-- box footer -->
</div> <!-- box -->
</%def>

<%def name="side_panel()" filter="trim">
    <%include file="season_select_form.mako"/>
    <%include file="latest_games.mako"/>
</%def>

