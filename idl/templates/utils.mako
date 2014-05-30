<%def name="static_link(x)" filter="trim">
    ${url_for("static", filename=x)}
</%def>

<%def name="image_link(x)" filter="trim">
    ${static_link("/".join(("images", x)))}
</%def>

<%def name="css_link(x)" filter="trim">
    <link rel="stylesheet"
          type="text/css"
          href="${static_link("/".join(("styles", x)))}" />
</%def>

<%def name="js_link(x)" filter="trim">
    <script type="text/javascript" src="${static_link("/".join(("js", x)))}">
    </script>
</%def>

<%def name="jquery_link()" filter="trim">
    <script
     type="text/javascript"
     src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js">
    </script>
</%def>

<%def name="flash_link(x)" filter="trim">
    ${static_link("/".join(("flash", x)))}
</%def>

<%def name="navbar_link(upper_or_lower, title, href)" filter="trim">
    <%
        name = " ".join([x.capitalize() for x in title.split()])
        active = False
        if upper_or_lower == "upper":
            if context["section"] == title:
                active = True
        elif upper_or_lower == "lower":
            if context["subsection"] == title:
                active = True
    %>
    <li>
    % if active:
        <a title="${name | h}" href="${href}" class="active">
    % else:
        <a title="${name | h}" href="${href}">
    % endif
            <span>${name | h}</span>
        </a>
    </li>
</%def>

<%def name="upper_navbar(labels_and_urls)" filter="trim">
    <div id="upper_navbar" class="navbar">
        <ul class="clearfix">
            % for label, url in labels_and_urls:
                ${navbar_link("upper", label, url)}
            % endfor
        </ul>
    </div>
</%def>

<%def name="lower_navbar(labels_and_urls)" filter="trim">
    <div id="lower_navbar" class="navbar">
        <ul class="clearfix">
            % for label, url in labels_and_urls:
                ${navbar_link("lower", label, url)}
            % endfor
        </ul>
    </div>
</%def>

<%def name="ratio(x, y, factor=100, percentage=True, zero=None)" filter="trim">
    <%
        import decimal
        decimal.setcontext(decimal.ExtendedContext)
        decimal.prec = 4
    %>

    % if x == 0:
        % if zero:
            ${zero}
        % elif percentage:
            0%
        % else:
            0
        % endif
    % elif y == 0:
        % if percentage:
            &#8734;%
        % else:
            &#8734;
        % endif
    % else:
        % if percentage:
            ${"%.3f" % ((decimal.Decimal(x) / decimal.Decimal(y)) * factor)}%
        % else:
            ${"%.3f" % ((decimal.Decimal(x) / decimal.Decimal(y)) * factor)}
        % endif
    % endif
</%def>

<%def name="format_seconds(s)" filter="trim">
    <%
        days = ''.join((str(int(s) / 86400), "d"))
        remaining = int(s) % 86400
        hours = ''.join((str(remaining / 3600), "h"))
        remaining = remaining % 3600
        minutes = ''.join((str(remaining / 60), "m"))
        seconds = ''.join((str(remaining % 60), "s"))
        times = (days, hours, minutes, seconds)
        formatted_time = ' '.join((x for x in times if not x.startswith("0")))
    %>
    ${formatted_time}
</%def>

