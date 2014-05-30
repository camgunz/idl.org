<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>
<%! from datetime import datetime %>

<%def name="css()" filter="trim">
    ${utils.css_link("box_scores.css")}
    ${utils.css_link("news.css")}
</%def>

<%def name="js()" filter="trim"></%def>

<%def name="display_time(seconds)" filter="trim">
    <%
        dt = datetime.fromtimestamp(seconds)
        mod = dt.day % 10
        if mod == 1:
            suffix = 'st'
        elif mod == 2:
            suffix = 'nd'
        elif mod == 3:
            suffix = 'rd'
        else:
            suffix = 'th'
    %>
    ${dt.strftime('%b. ') + dt.strftime('%dth %Y').lstrip('0')}
</%def>

<%def name="forum_link(topic, content)" filter="trim">
    <%
        forums_url = context["config"]["FORUMS_URL"]
        url = "%s/index.php?topic=%s.0" % (forums_url, topic)
    %>
    <a href="${url}">${content}</a>
</%def>

<%def name="main_panel()" filter="trim">
    <div id="news">
        % for post in context['posts']:
            <div class="box news_post">
                <h3 class="box_header">
                    ${post.subject}
                </h3> <!-- box header -->
                <div class="box_body">
                    ${post.render_html() | n, trim}
                </div> <!-- box body -->
                <div class="box_footer">
                    Posted by ${post.poster_name} on 
                    ${display_time(post.poster_time)} - 
                    ${forum_link(
                          post.id_topic,
                          '%s comments' % (post.topic.num_replies)
                    )}
                </div> <!-- box footer -->
            </div> <!-- box -->
        % endfor
    </div> <!-- news -->
</%def>

<%def name="side_panel()" filter="trim">
    <%include file="latest_games.mako"/>
</%def>

