<hr/>
<h3>Search Results:</h3>
% for player in context["players"]:
    <% name = player.name %>
    <div class="player_profile_search_result">
        <a href="${url_for("player_profile", player_name=name)}">${name}</a>
    </div>
% endfor
