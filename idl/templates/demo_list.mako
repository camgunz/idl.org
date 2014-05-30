<%def name="display_game(g)" filter="trim">
    <% team_one, team_two = g.name[g.name.index(":") + 2:].split(" vs. ") %>
    <span class="red_team">${team_one}</span>
    vs.
    <span class="blue_team">${team_two}</span>
</%def>

% if not context["demos"]:
    % if not context["all_demos"]:
        <p id="nodemos">No demos have been uploaded yet.</p>
    % else:
        <p id="nodemos">Sorry, no demos matched your criteria.</p>
    % endif
    <% return %>
% endif

<%
    past_first_week = False
    def group(seq, size):
        cur = []
        for x in seq:
            cur.append(x)
            if len(cur) == size:
                yield cur
                del cur[:]
        if cur:
            yield [cur[0], None]
%>

<%def name="display_game_demos(game, demos)" filter="trim">
    <%
        red_team = game.team_one
        blue_team = game.team_two
        red_team_players = [p.name for p in game.get_players_for_team(red_team)]
        red_team_missing_players = [x for x in red_team_players]
        blue_team_players = [
            p.name for p in game.get_players_for_team(blue_team)
        ]
        blue_team_missing_players = [x for x in blue_team_players]
        red_team_demos = []
        blue_team_demos = []
        for demo in demos:
            name = demo.player.name
            if name in red_team_missing_players:
                red_team_demos.append((name, demo.absolute_url))
                red_team_missing_players.remove(name)
            elif name in blue_team_missing_players:
                blue_team_demos.append((name, demo.absolute_url))
                blue_team_missing_players.remove(name)
        for name in red_team_missing_players:
            red_team_demos.append((name, None))
        for name in blue_team_missing_players:
            blue_team_demos.append((name, None))
        max_demo_count = max((
            len(red_team_demos),
            len(blue_team_demos)
        ))
        while len(red_team_demos) < max_demo_count:
            red_team_demos.append(None)
        while len(blue_team_demos) < max_demo_count:
            blue_team_demos.append(None)
    %>
    <div class="table_row">
        <div class="table_cell header red_team">${red_team.tag}</div>
        <div class="table_cell header">vs</div>
        <div class="table_cell header blue_team">${blue_team.tag}</div>
        <div class="table_cell header spacer"></div>
        <div class="table_cell header"></div>
        <div class="table_cell header"></div>
        <div class="table_cell header"></div>
    </div>
    % for rd1, bd1 in zip(red_team_demos, blue_team_demos):
        <div class="table_row">
            <div class="table_cell red_player centered">
                % if rd1:
                    % if rd1[1]:
                        <a href="${rd1[1]}">${rd1[0]}</a>
                    % else:
                        <span class="missing">${rd1[0]}</span>
                    % endif
                % endif
            </div>
            <div class="table_cell"></div>
            <div class="table_cell blue_player centered">
                % if bd1:
                    % if bd1[1]:
                        <a href="${bd1[1]}">${bd1[0]}</a>
                    % else:
                        <span class="missing">${bd1[0]}</span>
                    % endif
                % endif
            </div>
            <div class="table_cell spacer"></div>
            <div class="table_cell red_player centered"></div>
            <div class="table_cell"></div>
            <div class="table_cell blue_player centered"></div>
        </div>
    % endfor
</%def>

<%def name="display_demos_for_games(both_games, both_games_demos)"
      filter="trim">
    <%
        game_one, game_two = both_games
        game_one_demos, game_two_demos = both_games_demos
        red_team_one = game_one.team_one
        blue_team_one = game_one.team_two
        red_team_two = game_two.team_one
        blue_team_two = game_two.team_two
        red_team_one_players = [p.name for p in game_one.get_players_for_team(red_team_one)]
        red_team_one_missing_players = [x for x in red_team_one_players]
        blue_team_one_players = [p.name for p in game_one.get_players_for_team(blue_team_one)]
        blue_team_one_missing_players = [x for x in blue_team_one_players]
        red_team_two_players = [p.name for p in game_two.get_players_for_team(red_team_two)]
        red_team_two_missing_players = [x for x in red_team_two_players]
        blue_team_two_players = [p.name for p in game_two.get_players_for_team(blue_team_two)]
        blue_team_two_missing_players = [x for x in blue_team_two_players]
        red_team_one_demos = []
        blue_team_one_demos = []
        red_team_two_demos = []
        blue_team_two_demos = []
        for demo in game_one_demos:
            name = demo.player.name
            if name in red_team_one_missing_players:
                red_team_one_demos.append((name, demo.absolute_url))
                red_team_one_missing_players.remove(name)
            elif name in blue_team_one_missing_players:
                blue_team_one_demos.append((name, demo.absolute_url))
                blue_team_one_missing_players.remove(name)
        for demo in game_two_demos:
            name = demo.player.name
            if name in red_team_two_missing_players:
                red_team_two_demos.append((name, demo.absolute_url))
                red_team_two_missing_players.remove(name)
            elif name in blue_team_two_missing_players:
                blue_team_two_demos.append((name, demo.absolute_url))
                blue_team_two_missing_players.remove(name)
        for name in red_team_one_missing_players:
            red_team_one_demos.append((name, None))
        for name in blue_team_one_missing_players:
            blue_team_one_demos.append((name, None))
        for name in red_team_two_missing_players:
            red_team_two_demos.append((name, None))
        for name in blue_team_two_missing_players:
            blue_team_two_demos.append((name, None))
        max_demo_count = max((
            len(red_team_one_demos),
            len(blue_team_one_demos),
            len(red_team_two_demos),
            len(blue_team_two_demos)
        ))
        while len(red_team_one_demos) < max_demo_count:
            red_team_one_demos.append(None)
        while len(blue_team_one_demos) < max_demo_count:
            blue_team_one_demos.append(None)
        while len(red_team_two_demos) < max_demo_count:
            red_team_two_demos.append(None)
        while len(blue_team_two_demos) < max_demo_count:
            blue_team_two_demos.append(None)
        zipped_demos = zip(
            red_team_one_demos,
            blue_team_one_demos,
            red_team_two_demos,
            blue_team_two_demos
        )
    %>
    <div class="table_row">
        <div class="table_cell red_team centered">${red_team_one.tag}</div>
        <div class="table_cell centered">vs</div>
        <div class="table_cell blue_team centered">${blue_team_one.tag}</div>
        <div class="table_cell spacer"></div>
        <div class="table_cell red_team centered">${red_team_two.tag}</div>
        <div class="table_cell centered">vs</div>
        <div class="table_cell blue_team centered">${blue_team_two.tag}</div>
    </div>
    % for rd1, bd1, rd2, bd2 in zipped_demos:
        <div class="table_row">
            <div class="table_cell red_player centered">
                % if rd1:
                    % if rd1[1]:
                        <a href="${rd1[1]}">${rd1[0]}</a>
                    % else:
                        <span class="missing">${rd1[0]}</span>
                    % endif
                % endif
            </div>
            <div class="table_cell"></div>
            <div class="table_cell blue_player centered">
                % if bd1:
                    % if bd1[1]:
                        <a href="${bd1[1]}">${bd1[0]}</a>
                    % else:
                        <span class="missing">${bd1[0]}</span>
                    % endif
                % endif
            </div>
            <div class="table_cell spacer"></div>
            <div class="table_cell red_player centered">
                % if rd2:
                    % if rd2[1]:
                        <a href="${rd2[1]}">${rd2[0]}</a>
                    % else:
                        <span class="missing">${rd2[0]}</span>
                    % endif
                % endif
            </div>
            <div class="table_cell"></div>
            <div class="table_cell blue_player centered">
                % if bd2:
                    % if bd2[1]:
                        <a href="${bd2[1]}">${bd2[0]}</a>
                    % else:
                        <span class="missing">${bd2[0]}</span>
                    % endif
                % endif
            </div>
        </div>
    % endfor
</%def>

<%
    season = context["session"]["season"]
    league = context["session"]["league"]
%>
## % for week, week_games in context["demos"]:
% for week in context["weeks"]:
    <%
        map = week.get_map_for_season(season)
        screenshot = week.get_map_screenshot_for_season(season)
        week_games = context["demos"][week].keys()
    %>
    % if past_first_week:
        <hr class="schedule_separator"/>
    % else:
        <% past_first_week = True %>
    % endif
    <div class="week background_screenshot">
        <div class="screenshot">
            % if screenshot:
                <img src="${screenshot}"/>
            % endif
        </div>
        <div class="content games">
            % if map:
                <a class="nolink" id="week${week.number}"><h2>Week ${week.number} - ${map.short_name}: ${map.name}</h2></a>
            % else:
                <a class="nolink" id="week${week.number}"><h2>${week}</h2></a>
            % endif
            <div class="demos">
                % for game1, game2 in group(week_games, 2):
                    % if game2:
                        ${display_demos_for_games((game1, game2), (game1.demos, game2.demos))}
                    % else:
                        ${display_game_demos(game1, game1.demos)}
                    % endif
                % endfor
            </div> <!-- demos -->
        </div> <!-- games -->
    </div> <!-- week -->
% endfor

