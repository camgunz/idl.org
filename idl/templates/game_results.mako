<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="css()" filter="trim">
    ${utils.css_link("ss_backgrounds.css")}
    ${utils.css_link("box_scores.css")}
    ${utils.css_link("game_results.css")}
</%def>

<%def name="js()" filter="trim">
    ${utils.jquery_link()}
    ${utils.js_link("idl.js")}
</%def>

<%def name="display_results(game, results, full_names=False)" filter="trim">
    ${full_names and game.team_one.name or game.team_one.tag} ${results[0]} -
    ${full_names and game.team_two.name or game.team_two.tag} ${results[1]}
</%def>

<%def name="display_stats(game, names, overview, stat_charts, frag_chart)"
      filter="trim">
    <%
        team_overviews = zip(
            (game.team_one.tag, game.team_two.tag),
            ('red', 'blue'),
            overview
        )
        red_team = [p.name for p in game.get_players_for_team(game.team_one)]
        blue_team = [p.name for p in game.get_players_for_team(game.team_two)]
        red_team = [n for n in names if n in red_team]
        blue_team = [n for n in names if n in blue_team]
        no_team = [n for n in names if n not in red_team and n not in blue_team]
        names = no_team + red_team + blue_team
    %>
    <table class="overview">
        <caption>Team Stats</caption>
        <tr>
            <th></th>
            <th>Frag</th>
            <th>Cap</th>
            <th>PCap</th>
            <th>Drop</th>
            <th>Touch</th>
            <th>Pick</th>
            <th>Frag %</th>
            <th>Cap %</th>
            <th>Pick %</th>
            <th>Stop %</th>
        </tr>
        % for team_tag, bg, stats in team_overviews:
            <tr class="${bg}_team">
                <td class="lefted ${bg}">${team_tag}</td>
                <td>${stats['frags']}</td>
                <td>${stats['flag_captures']}</td>
                <td>${stats['flag_pick_captures']}</td>
                <td>${stats['flag_drops']}</td>
                <td>${stats['flag_touches']}</td>
                <td>${stats['flag_picks']}</td>
                <td>${utils.ratio(stats['frags'], stats['deaths'])}</td>
                <td>
                    ${utils.ratio(
                          stats['flag_captures'], stats['flag_touches']
                    )}
                </td>
                <td>
                    ${utils.ratio(
                          stats['flag_pick_captures'], stats['flag_picks']
                    )}
                </td>
                <td>
                    ${utils.ratio(
                          stats['flag_drops'], stats['touches_allowed']
                    )}
                </td>
            </tr>
        % endfor
    </table>
    <table class="individual_stats">
        <caption>Player Stats</caption>
        <tr>
            <th></th>
            <th>Frag</th>
            <th>Cap</th>
            <th>PCap</th>
            <th>Drop</th>
            <th>Touch</th>
            <th>Pick</th>
            <th>Frag %</th>
            <th>Cap %</th>
            <th>Pick %</th>
        </tr>
        % for name in names:
            <%
                if name in red_team:
                    bg = "red_team"
                elif name in blue_team:
                    bg = "blue_team"
                else:
                    bg = ""
            %>
            <tr>
                <td class="lefted ${bg}">${name}</td>
                <td class="${bg}">${stat_charts["frags"].get(name, 0)}</td>
                <td class="${bg}">${stat_charts["captures"].get(name, 0)}</td>
                <td class="${bg}">${stat_charts["pick_captures"].get(name, 0)}</td>
                <td class="${bg}">${stat_charts["drops"].get(name, 0)}</td>
                <td class="${bg}">${stat_charts["touches"].get(name, 0)}</td>
                <td class="${bg}">${stat_charts["picks"].get(name, 0)}</td>
                <td class="${bg}">
                    ${utils.ratio(
                          stat_charts["frags"].get(name, 0),
                          stat_charts["deaths"].get(name, 0)
                    )}
                </td>
                <td class="${bg}">
                    ${utils.ratio(
                          stat_charts["captures"].get(name, 0),
                          stat_charts["touches"].get(name, 0)
                    )}
                </td>
                <td class="${bg}">
                    ${utils.ratio(
                          stat_charts["pick_captures"].get(name, 0),
                          stat_charts["picks"].get(name, 0)
                    )}
                </td>
            </tr>
        % endfor
    </table>
    <table class="matchups">
        <caption>Player Matchups</caption>
        <tr>
            <th></th>
            % for name in names:
                % if name in frag_chart:
                    <th>${name}</th>
                % endif
            % endfor
        </tr>
        % for p1 in names:
            <%
                if p1 not in frag_chart:
                    continue
                if p1 in red_team:
                    bg = "red_team"
                elif p1 in blue_team:
                    bg = "blue_team"
                else:
                    bg = ""
            %>
            <tr>
                <td class="lefted ${bg} max_width">${p1}</td>
                % for p2 in names:
                    <%
                        if p2 not in frag_chart:
                            continue
                        f1 = frag_chart[p1].get(p2, 0)
                        f2 = frag_chart[p2].get(p1, 0)
                    %>
                    % if p1 == p2:
                        <td class="${bg}">-</td>
                    % else:
                        <td class="${bg}">
                            ${utils.ratio(f1, f2, zero="-")}
                        </td>
                    % endif
                % endfor
            </tr>
        % endfor
    </table>
</%def>

<%def name="get_cap_timestamp(fc)" filter="trim">
    <%
        round_start = fc.round.start_time
        delta = fc.loss_time - fc.round.start_time
        minutes, seconds = (delta.seconds / 60, delta.seconds % 60)
    %>
    ${'%s:%s' % (unicode(minutes), unicode(seconds).zfill(2))}
</%def>

<%def name="display_flag_capture(round_number, fc)" filter="trim">
    <%
        round_team_colors = context["team_colors"][round_number-1]
        team_one = context["game"].team_one.tag
        team_two = context["game"].team_two.tag
        if round_team_colors[0] == 'red':
            t1_score = fc.red_team_score
            t2_score = fc.blue_team_score
        else:
            t1_score = fc.blue_team_score
            t2_score = fc.red_team_score
        if fc.player_team_color_name == round_team_colors[0]:
            scoring_team = team_one
            t1_score += 1
        else:
            scoring_team = team_two
            t2_score += 1
        team_color = fc
        if fc.alias.stored_player:
            flagger = fc.alias.stored_player.name
        else:
            flagger = fc.alias.name
    %>
    <div class="flag_capture">
        ${t1_score}-${t2_score} | ${get_cap_timestamp(fc)} - ${scoring_team} - ${flagger}
    </div>
</%def>

<%def name="main_panel()" filter="trim">
    <%
        game = context["game"]
        week = game.week
        season = game.season
    %>
    <div class="box">
        <h3 class="box_header">
            ${season} - ${week}: ${game.team_one.tag} vs. ${game.team_two.tag}
        </h3>
        <div class="box_body">
            <div class="background_screenshot round">
                <div class="screenshot">
                </div>
                <div class="content stats">
                    <h3 class="game_results">
                        ${display_results(
                              game, context["round_counts"], full_names=True
                        )}
                    </h3>
                    ${display_stats(
                          game,
                          context["names"],
                          context["game_overview"],
                          context["game_stats"],
                          context["game_frag_charts"]
                    )}
                </div> <!-- content stats -->
            </div> <!-- round -->
        </div> <!-- box body -->
    </div> <!-- box -->
    % for n, round in enumerate(context["game"].rounds):
        <div class="box">
            <a class="nolink" id="round${n + 1}">
                <h3 class="box_header">
                    Round ${n + 1}: 
                    ${display_results(
                          game, context["total_flag_capture_counts"][n]
                    )}
                    % if 5 in context["total_flag_capture_counts"][n]:
                        | ${get_cap_timestamp(flag_captures[n][-1])}
                    % else:
                        | 10:00
                    % endif
                </h3>
            </a>
            <div class="box_body">
                <div class="background_screenshot round">
                    <div class="content stats">
                        ${display_stats(
                              game,
                              context["names"],
                              context["round_overviews"][n],
                              context["round_stats"][n],
                              context["round_frag_charts"][n]
                        )}
                    </div> <!-- content stats -->
                </div> <!-- round -->
            </div> <!-- box body -->
        </div> <!-- box -->
    %endfor
</%def>

<%def name="side_panel()" filter="trim">
    <%
        import operator
        game = context["game"]
        week = game.week
        season = game.season
        screenshot = week.get_map_screenshot_for_season(season)
        demos = game.demos
    %>
    <div class="box">
        <h3 class="box_header">Demos</h3>
        <div class="box_body">
            <div class="game_demos">
                <table class="game_demos">
                    <tr>
                        <th class="centered">Team</th>
                        <th class="centered">Player</th>
                        <th class="centered">File</th>
                    </tr>
                    <%
                        seen_demo_urls = set()
                        key = operator.attrgetter('team')
                    %>
                    % if demos:
                        % for d in sorted(demos, key=key):
                            % if d.absolute_url not in seen_demo_urls:
                                <% seen_demo_urls.add(d.absolute_url) %>
                                <tr>
                                    <td class="centered">${d.team.tag}</td>
                                    <td>${d.player_name}</td>
                                    <td>
                                        <a href="${d.absolute_url}">Download</a>
                                    </td>
                                </tr>
                            % endif
                        % endfor
                    % else:
                        <tr>
                            <td class="centered" colspan="3">No Demos</td>
                        </tr>
                    % endif
                </table>
            </div> <!-- game demos -->
        </div> <!-- box body -->
    </div> <!-- box -->
    <div class="box">
        <h3 class="box_header">Rounds</h3>
        <div class="box_body">
            % for n, round in enumerate(game.rounds):
                <div class="score_entry">
                    <div class="box_score_screenshot">
                        <img src="${screenshot}">
                    </div> <!-- box score screenshot -->
                    <div class="box_score">
                        <div class="box_score_header">
                            <a href="#round${n + 1}"><h2>Round ${n + 1}</h2></a>
                        </div> <!-- box score header -->
                        <div class="box_score_content">
                            % if flag_captures[n]:
                                % for flag_touch in flag_captures[n]:
                                    % if flag_touch.resulted_in_score:
                                        ${display_flag_capture(n, flag_touch)}
                                    % endif
                                % endfor
                            % else:
                                <p>STALEMATE</p>
                            % endif
                        </div> <!-- box score content -->
                    </div> <!-- box score -->
                </div> <!-- score entry -->
                % if n < (len(game.rounds) - 1):
                    <hr class="score_entry_separator"/>
                % endif
            % endfor
        </div> <!-- box body -->
    </div> <!-- box -->
</%def>

