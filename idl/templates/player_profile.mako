<%namespace name="utils" file="utils.mako"/>

<% profile = context["profile"] %>

<div class="doomguy_background">
    <img src="${utils.image_link("doomguy-color.png")}"/>
</div>
<div class="player_stats">
    <h2>${context["player"].name}</h2>
    <table class="player_stats">
        <tr>
            <td>Rounds Played:</td>
            <td>${profile["round_count"]}</td>
        </tr>
        <tr>
            <td>Record:</td>
            <td>${profile["record"]} (${profile["pct"]})</td>
        </tr>
        <tr>
            <td>Total Frags:</td>
            <td>${profile["frags"]}</td>
        </tr>
        <tr>
            <td>Frags / Round:</td>
            <td>${utils.ratio(profile["frags"], profile["round_count"], 1, False)}</td>
        </tr>
        <tr>
            <td>Total Flags:</td>
            <td>${profile["flag_captures"]}</td>
        </tr>
        <tr>
            <td>Flags / Round:</td>
            <td>${utils.ratio(profile["flag_captures"], profile["round_count"], 1, False)}</td>
        </tr>
        <tr>
            <td>Frag %:</td>
            <td>${utils.ratio(profile["frags"], profile["deaths"])}</td>
        </tr>
        <tr>
            <td>Flag %:</td>
            <td>${utils.ratio(profile["flag_captures"], profile["flag_touches"])}</td>
        </tr>
    </table>
</div>
