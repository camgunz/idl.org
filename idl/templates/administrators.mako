<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="css()" filter="trim">
    ${utils.css_link("box_scores.css")}
    ${utils.css_link("administrators.css")}
</%def>

<%def name="js()" filter="trim">
    ${utils.jquery_link()}
    ${utils.js_link("idl.js")}
</%def>

<%def name="main_panel()" filter="trim">
    <%
        special_admin_positions = (
            "Commissioner", "Head of the Board", "Site Admin"
        )
    %>
    <div class="box">
        <%include file="info_navbar.mako"/>
        <div class="box_body">
            <h3 class="box_body_header">IDL Administrators</h3>
            <div class="full_width centered">
                <div class="table">
                    <div class="table_row">
                        <div class="table_cell header">Title</div>
                        <div class="table_cell header">Office Holder</div>
                    </div>
                    % for admin in context["administrators"]:
                        % if admin.position == "Commissioner":
                            <div class="table_row">
                                <div class="table_cell">${admin.position}:</div>
                                <div class="table_cell">${admin.name}</div>
                            </div>
                        % endif
                    % endfor
                    % for admin in context["administrators"]:
                        % if admin.position == "Head of the Board":
                            <div class="table_row">
                                <div class="table_cell">${admin.position}:</div>
                                <div class="table_cell">${admin.name}</div>
                            </div>
                        % endif
                    % endfor
                    % for admin in context["administrators"]:
                        % if admin.position not in special_admin_positions:
                            <div class="table_row">
                                <div class="table_cell">${admin.position}:</div>
                                <div class="table_cell">${admin.name}</div>
                            </div>
                        % endif
                    % endfor
                    % for admin in context["administrators"]:
                        % if admin.position == "Site Admin":
                            <div class="table_row">
                                <div class="table_cell">${admin.position}:</div>
                                <div class="table_cell">${admin.name}</div>
                            </div>
                        % endif
                    % endfor
                </div> <!-- table -->
            </div> <!-- full width -->
        </div> <!-- box body -->
    </div> <!-- box -->
</%def>

<%def name="side_panel()" filter="trim">
    <%include file="latest_games.mako"/>
</%def>

