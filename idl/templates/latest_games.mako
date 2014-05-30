<div class="box">
    <a href="/schedule" class="box_header_link"><h3 class="box_header">Latest Games</h3></a>
    <div class="box_body">
        % for game in context["games"]:
            <%
                screenshot_url = game.map_screenshot
                scores = game.total_flag_captures_by_round_and_team
            %>
            <div class="score_entry">
                <img src="${screenshot_url}"/>
                <div class="box_scores">
                    <a href="${url_for("game_results", game_id=game.id)}"><h2>${game.map.name}</h2></a>
                    <table class="box_scores">
                        <tr class="red_team">
                            <td>${game.team_one}</td>
                            % for round_scores in scores:
                            <td>${len(round_scores[0])}</td>
                            % endfor
                        </tr>
                        <tr class="blue_team">
                            <td>${game.team_two}</td>
                            % for round_scores in scores:
                            <td>${len(round_scores[1])}</td>
                            % endfor
                        </tr>
                    </table>
                </div> <!-- box scores -->
                <hr class="score_entry_separator" />
            </div> <!-- latest game -->
        % endfor
    </div> <!-- box body -->
</div> <!-- box -->
