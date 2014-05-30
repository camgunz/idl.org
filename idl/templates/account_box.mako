% if "username" in context["session"]:
    <%include file="demo_upload_form.mako"/>
% else:
    <%include file="login_form.mako"/>
% endif
