<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="css()" filter="trim">
    ${utils.css_link("week_summary.css")}
    ${utils.css_link("ss_backgrounds.css")}
    ${utils.css_link("schedules.css")}
</%def>

<%def name="js()" filter="trim">
    ${utils.jquery_link()}
    ${utils.js_link("idl.js")}
</%def>

<%def name="display_stars(game)" filter="trim">
    <%
        red_team = [p.name for p in game.get_players_for_team(game.team_one)]
        blue_team = [p.name for p in game.get_players_for_team(game.team_two)]
        stars = game.stars
    %>
    <td class="star">
        % for i, name in enumerate(stars["flag_count"]["names"]):
            % if i:
                ,<br/>
            % endif
            % if name in red_team:
                <span class="red_team">${name}</span>
            % elif name in blue_team:
                <span class="blue_team">${name}</span>
            % else:
                <span>${name}</span>
            % endif
        % endfor
    </td>
    <td class="star">${stars["flag_count"]["stat"]}</td>
    <td class="star">
        % for i, name in enumerate(stars["frag_count"]["names"]):
            % if i:
                ,<br/>
            % endif
            % if name in red_team:
                <span class="red_team">${name}</span>
            % elif name in blue_team:
                <span class="blue_team">${name}</span>
            % else:
                <span>${name}</span>
            % endif
        % endfor
    </td>
    <td class="star">${stars["frag_count"]["stat"]}</td>
</%def>

<%def name="display_week_games(week, games)" filter="trim">
    <%

        import decimal
        decimal.setcontext(decimal.ExtendedContext)
        decimal.prec = 4

        from datetime import datetime

        def dates_equal(d1, d2):
            if not isinstance(d1, datetime) and not isinstance(d2, datetime):
                return True
            elif not isinstance(d1, datetime) or not isinstance(d2, datetime):
                return False
            if d1.year != d2.year or d1.month != d2.month or d1.day != d2.day:
                return False
            return True
    %>
    % if not games:
        <tr>
            <th class="centered" colspan="12">No Games</th>
        </tr>
    % else:
        <%
            current_date = games[0].scheduled_for
            if not current_date:
                current_date_string = "TBD"
            else:
                current_date_string = current_date.strftime("%a, %b %d").upper()
        %>
        <tr>
            <th class="lefted" colspan="7">${current_date_string}</th>
            <th>RNDS</th>
            <th colspan="2">TOP RUNNERS</th>
            <th colspan="2">TOP FRAGGERS</th>
        </tr>
        % for game in games:
            <%
                round_counts = game.round_counts
                team_one = game.team_one
                team_two = game.team_two
                t1_stats = team_one.get_regular_season_info(context["session"]["season"])
                t2_stats = team_two.get_regular_season_info(context["session"]["season"])
            %>
            % if not dates_equal(game.scheduled_for, current_date):
                <%
                    current_date = game.scheduled_for
                    if not current_date:
                        current_date_string = "TBD"
                    else:
                        current_date_string = current_date.strftime("%a, %b %d")
                        current_date_string = current_date_string.upper()
                %>
                <th class="lefted" colspan="12">${current_date_string}</th>
            % endif
            <tr>
            % if game.forfeiting_team:
                % if game.forfeiting_team == team_one:
                    <td class="red_team">
                        <span class="strike">${team_one.tag}</span>
                    </td>
                    <td class="red_team">-</td>
                    <td>vs</td>
                    <td class="blue_team">${team_two.tag}</td>
                    <td class="blue_team">-</td>
                % else:
                    <td class="red_team">${team_one.tag}</td>
                    <td class="red_team">-</td>
                    <td>vs</td>
                    <td class="blue_team">
                        <span class="strike">${team_two.tag}</span>
                    </td>
                    <td class="blue_team">-</td>
                % endif
                <td><span class="smallcaps">${game.rivalry}</span></td>
                <td>-</td>
                <td>-</td>
                <td colspan="2">-</td>
                <td colspan="2">-</td>
            % elif game.has_been_played:
                <td class="red_team">${team_one.tag}</td>
                <td class="red_team">${round_counts[0]}</td>
                <td>vs</td>
                <td class="blue_team">${team_two.tag}</td>
                <td class="blue_team">${round_counts[1]}</td>
                <td><span class="smallcaps">${game.rivalry}</span></td>
                <td>
                    <a href="${url_for('game_results', game_id=game.id)}">FINAL</a>
                </td>
                <td>${len(game.rounds)}</td>
                ${display_stars(game)}
            % else:
                <td class="red_team">${team_one.tag}</td>
                <td class="red_team">${t1_stats["win_percentage"]}</td>
                <td>vs</td>
                <td class="blue_team">${team_two.tag}</td>
                <td class="blue_team">${t2_stats["win_percentage"]}</td>
                <td><span class="smallcaps">${game.rivalry}</span></td>
                % if game.scheduled_for:
                    <td>${game.scheduled_for.strftime("%I:%M%p").upper().lstrip('0')}</td>
                % else:
                    <td>-</td>
                % endif
                <td>-</td>
                <td colspan="2">-</td>
                <td colspan="2">-</td>
            % endif
            </tr>
        % endfor
    % endif
</%def>

<%def name="main_panel()" filter="trim">
    <div class="box">
        <%include file="season_navbar.mako"/>
        <div class="box_body">
            % if context["schedule_type"] == "regular_season":
                <h3 class="box_body_header">Schedule / <a href="/season/playoffs">Playoffs</a></h3>
            % else:
            <h3 class="box_body_header"><a href="/schedule">Schedule</a> / Playoffs</h3>
            % endif
            % for week in context["weeks"]:
                <%
                    season = context["session"]["season"]
                    league = context["league"]
                    map = week.get_map_for_season(season)
                    games = week.get_games_for_league_and_season(league, season)
                %>
                % if week.number > 1:
                    <hr class="schedule_separator" />
                % endif
                <div class="schedule_week background_screenshot">
                    <div class="screenshot">
                        <img src="${week.get_map_screenshot_for_season(context["session"]["season"])}"/>
                    </div>
                    <div class="content week_table">
                        % if map:
                            <a class="nolink" id="week${week.number}"><h2>Week ${week.number} - ${map.short_name}: ${map.name}</h2></a>
                        % else:
                            <a class="nolink" id="week${week.number}"><h2>${week.name}</h2></a>
                        % endif
                        <table class="game_results">
                            ${display_week_games(week, games)}
                        </table>
                    </div> <!-- week table -->
                </div> <!-- schedule week -->
            % endfor
        </div> <!-- box body -->
    </div> <!-- box -->
</%def>

<%def name="side_panel()" filter="trim">
    <%include file="season_select_form.mako"/>
    <%include file="week_anchor_box.mako"/>
</%def>

