<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="css()" filter="trim">
    ${utils.css_link("week_summary.css")}
    ${utils.css_link("ss_backgrounds.css")}
    ${utils.css_link("demos.css")}
</%def>

<%def name="js()" filter="trim">
    ${utils.js_link("tablesort.js")}
    ${utils.jquery_link()}
    ${utils.js_link("idl.js")}
</%def>

<%def name="display_name(name)" filter="trim">
    ${name[name.index(" - ") + 3:]}
</%def>

<%def name="main_panel()" filter="trim">
    <div class="box">
        <%include file="season_navbar.mako"/>
        <div class="box_body">
            <%include file="demo_list.mako"/>
        </div> <!-- box body -->
    </div> <!-- box -->
</%def>

<%def name="side_panel()" filter="trim">
    <%include file="season_select_form.mako"/>
    <%include file="week_anchor_box.mako"/>
</%def>

