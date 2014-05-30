<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="css()" filter="trim">
    ${utils.css_link("box_scores.css")}
    ${utils.css_link("credits.css")}
</%def>

<%def name="js()" filter="trim">
    ${utils.jquery_link()}
    ${utils.js_link("idl.js")}
</%def>

<%def name="main_panel()" filter="trim">
    <div class="box">
        <%include file="info_navbar.mako"/>
        <div class="box_body">
            <h3 class="box_body_header">Credits &amp; Attribution</h3>
            <div class="full_width centered">
                <div class="table">
                    <div class="table_row">
                        <div class="table_cell header">Name</div>
                        <div class="table_cell header">Contributions</div>
                    </div>
                    % for contributor in context["contributors"]:
                        <div class="table_row">
                            % if contributor.link:
                                <div class="table_cell">
                                    <a href="${contributor.link}">${contributor.name}</a>
                                </div>
                            % else:
                                <div class="table_cell">
                                    ${contributor.name}
                                </div>
                            % endif
                            <div class="table_cell">
                                ${contributor.contribution}
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

