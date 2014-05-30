<%namespace name="utils" file="utils.mako"/>

<h3 class="box_header">Welcome ${context["session"]["username"]}!</h3>
<div class="box_body">
    <form action="${url_for("demo_upload")}" method="POST"
          enctype="multipart/form-data"
          target="demo_data" id="demo_upload"
          onsubmit="demoUploadStarted();">
        <fieldset>
            <legend>Upload a Demo</legend>
            % if games:
                <select id="game" name="game">
                    % for game in games:
                        <option value="${game.id}">${game.name[7:]}</option>
                    % endfor
                </select>
                <br/>
                <div class="file_input">
                    <input type="file" id="demo" class="file" name="demo" />
                    <br/>
                    <button id="submit_demo" type="submit">Upload Demo</button>
                </div>
                <div id="error">
                </div> <!-- error -->
                <div id="success">
                </div> <!-- success -->
                <div id="uploading">
                    <img src="${utils.image_link("uploading.gif")}"/>
                    <span id="demo_upload_status">Uploading...</span>
                </div>
                <iframe id="demo_data" class="file_upload" name="demo_data"
                        src="#"></iframe>
            % else:
                <label>No games</label>
            % endif
        </fieldset>
    </form>
</div>
<div class="box_footer" id="logout_and_admin">
    % if context["session"]["is_admin"]:
        <a class="logout" href="${url_for("admin")}">Admin</a>
    % endif
    <a class="logout" href="${url_for("logout")}">Logout</a>
    <script type="text/javascript">
        document.getElementById("demo_upload").target = "demo_data";
    </script>
</div>

