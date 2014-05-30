<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="css()" filter="trim">
    ${utils.css_link("box_scores.css")}
    ${utils.css_link("servers.css")}
</%def>

<%def name="js()" filter="trim">
    ${utils.jquery_link()}
    ${utils.js_link("idl.js")}
</%def>

<%def name="main_panel()" filter="trim">
    <div class="box">
        <%include file="info_navbar.mako"/>
        <div class="box_body">
            <h3 class="box_body_header">IDL Servers</h3>
            <div class="full_width centered">
                <div class="table">
                    <div class="table_row">
                        <div class="table_cell header">Server</div>
                        <div class="table_cell header">Password</div>
                    </div>
                    % for server in context["servers"]:
                        <div class="table_row">
                            <div class="table_cell">
                                <a href="${server.address}">${server.name}</a>
                            </div>
                            <div class="table_cell">
                                ${server.password or '-'}
                            </div>
                        </div>
                    % endfor
                </div> <!-- table -->
            </div> <!-- full width -->
        </div> <!-- box body -->
    </div> <!-- box -->
</%def>

<%def name="side_panel()" filter="trim">
    <%include file="latest_games.mako"/>
</%def>

