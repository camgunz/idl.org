<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>
<%namespace name="account_box" file="account_box.mako"/>

<%def name="css()" filter="trim">
    ${utils.css_link("player_profiles.css")}
    ${utils.css_link("account_box.css")}
</%def>

<%def name="js()" filter="trim">
    ${utils.jquery_link()}
    ${utils.js_link("idl.js")}
</%def>

<%def name="main_panel()" filter="trim">
    <div class="box">
        <%include file="profiles_navbar.mako"/>
        <div class="box_body">
            <div id="player_profile">
                <%include file="player_profile.mako"/>
            </div> <!-- player profile -->
        </div> <!-- box body-->
    </div> <!-- box -->
</%def>

<%def name="side_panel()" filter="trim">
    <%include file="player_search_form.mako"/>
    <div id="account_box" class="box">
        <%include file="account_box.mako"/>
    </div>
</%def>

