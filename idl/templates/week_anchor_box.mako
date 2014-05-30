<div class="box">
    <h3 class="box_header">Weeks</h3>
    <div class="box_body">
        % for week in context["weeks"]:
            <% map = week.get_map_for_season(context["session"]["season"]) %>
            % if week.number > 1:
                <hr class="schedule_separator">
            % endif
            <div class="week_summary">
                % if map:
                    <a href="#week${week.number}"><h2>${week} - ${map.name}</h2></a>
                % else:
                    <a href="#week${week.number}"><h2>${week}</h2></a>
                % endif
                <img src="${week.get_map_screenshot_for_season(context["session"]["season"])}"/>
                <div class="matchups">
                    <table>
                        <%
                            games = week.get_games_for_league_and_season(
                                context["league"], context["session"]["season"]
                            )
                        %>
                        % if not games:
                            <tr>
                                <td class="centered" colspan="4">
                                    No Games Scheduled
                                </td>
                            </tr>
                        % else:
                            % for game in games:
                                <tr>
                                    <td>
                                        <a href="${url_for("game_results", game_id=game.id)}">${game.team_one.tag} vs ${game.team_two.tag}</a>
                                    </td>
                                    <td>
                                        <span class="smallcaps">
                                            ${game.rivalry}
                                        </span>
                                    </td>
                                </tr>
                            % endfor
                        % endif
                    </table>
                </div> <!-- matchups -->
            </div> <!-- week summary -->
        % endfor
    </div> <!-- box body -->
</div> <!-- box -->
