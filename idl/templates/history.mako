<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="css()" filter="trim">
    ${utils.css_link("box_scores.css")}
</%def>

<%def name="js()" filter="trim">
    ${utils.jquery_link()}
    ${utils.js_link("idl.js")}
</%def>

<%def name="main_panel()" filter="trim">
    <div class="box">
        <%include file="info_navbar.mako"/>
        <div class="box_body">
            <h3 class="box_body_header">IDL History</h3>
            <p>
                Founded in 2006, the International Doom League is the largest
                and longest enduring Doom Capture-The-Flag league in the world.
                Over the years, IDL has built a reputation as the most
                professional, competitive, highest-level CTF event in the Doom
                community and shows no signs of slowing down.
            </p>
            <p>
                Whereas most gaming leagues utilize team signups, IDL is unique
                due to its player draft system, which encourages team parity
                while keeping each season fresh and exciting.
            </p>
            <p>
                IDL strives to gather as much statistical information as
                possible so that players can compete on many different levels:
                best defender, most efficient runner, best all-time record; the
                possibilities are nearly endless.
            </p>
            <p>
                To that end, IDL archives data on players, teams, rounds,
                games, seasons, and maps in the hopes of amassing the most
                perfect record of IDL's history possible.
            </p>
            <p>
                For more information, log onto
                <a href="irc://irc.quakenet.org/idl">#idl on QuakeNet</a>, or
                or visit the <a href="${url_for("forums")}">forums</a>.
            </p>
        </div> <!-- box body -->
    </div> <!-- box -->
</%def>

<%def name="side_panel()" filter="trim">
    <%include file="latest_games.mako"/>
</%def>

