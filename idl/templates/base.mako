<%namespace name="utils" file="utils.mako"/>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    ${utils.css_link("styles.css")}
    ${utils.css_link("global.css")}
    ${utils.css_link("navbar.css")}
    ${utils.css_link("box.css")}
    ## ${utils.css_link("lifted-box.css")}
    ${next.css() | trim}
    ${utils.css_link("main.css")}
    ## ${utils.css_link("lifted-main.css")}
    <script type="text/javascript">
        var static_url = "${url_for("static", filename="")}"
        var _static_url_length = static_url.length - 1;
        if(static_url.indexOf("/", _static_url_length) !== -1) {
            static_url = static_url.substr(0, _static_url_length);
        }
    </script>
    ${next.js() | trim}
    <title>International Doom League</title>
</head>
<body>
    <div id="outer_body">
        <div id="body">
            ${utils.upper_navbar((
                ("home", url_for("home")),
                ("media", url_for("media")),
                ("profiles", url_for("random_player_profile")),
                ("season", url_for("standings")),
                ("info", url_for("history")),
                ("wiki", context["config"]["WIKI_URL"]),
                ("forums", context["config"]["FORUMS_URL"])
            ))}
            <div id="panels">
                <div id="main_panel">
                    ${next.main_panel() | trim}
                </div> <!-- main panel -->
                <div id="side_panel">
                    ${next.side_panel() | trim}
                </div> <!-- side panel -->
            </div> <!-- panels -->
            <div id="footer" class="centered rounded">
                <div>
                    <div>&copy; 2011 International Doom League</div>
                    <div><a href="${url_for("credits")}">Credits &amp; Attribution</a></div>
                </div>
            </div> <!-- footer -->
        </div> <!-- div body -->
    </div> <!-- div outer body-->
</body>
</html>

