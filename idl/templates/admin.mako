<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>
<%namespace name="controls" file="admin_widgets.mako"/>

<%def name="css()" filter="trim">
    ${utils.css_link("admin.css")}
</%def>

<%def name="js()" filter="trim">
    ${utils.jquery_link()}
    ${utils.js_link("idl.js")}
</%def>

<%def name="main_panel()" filter="trim">
    <div class="box">
        <h3 class="box_header">IDL Administration Center</h3>
        <div class="box_body">
            <div id="admin_box">
                <div id="error">
                    % if not "is_admin" in context["session"]:
                        Please Login
                    % elif not context["session"]["is_admin"]:
                        Not Authorized
                    % endif
                    <hr/>
                </div> <!-- error -->
                <div id="success">
                    <hr/>
                </div> <!-- success -->
                <div id="admin_list"></div>
                <div id="admin_entry">
                    <div id="no_module_selected">
                        Please select a module from the list.
                    </div>
                </div>
            </div> <!-- admin box -->
        </div> <!-- box body -->
    </div> <!-- box -->
</%def>

<%def name="side_panel()" filter="trim">
    <div class="box">
        <h3 class="box_header">Modules</h3>
        % if context["session"].get("is_admin", False):
            <div id="modules">
                <ul id="modules_list" class="size3">
                    % for module, models in context["LAYOUT"]:
                        % if module == 'IDL Infrastructure':
                            <li class="admin_entry" onclick="adminList('Game Log');">Game Logs</li>
                        % endif
                        <li class="module_header">${module}</li>
                        % for model in models:
                            ${controls.admin_modules_widget(model.Admin.label)}
                        % endfor
                    % endfor
                </ul>
            </div> <!-- admin div -->
        % endif
    </div> <!-- box -->
</%def>

