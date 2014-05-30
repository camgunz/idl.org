<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="css()" filter="trim">
    ${utils.css_link("media.css")}
</%def>

<%def name="js()" filter="trim">
    ${utils.js_link("flowplayer-3.2.6.min.js")}
    ${utils.jquery_link()}
    ${utils.js_link("idl.js")}
    ${utils.js_link("media.js")}
</%def>

<%def name="flow_link(x)" filter="trim">
    ${utils.flash_link("/".join(("flowplayer", x)))}
</%def>

<%def name="ffmp3_link(x)" filter="trim">
    ${utils.flash_link("/".join(("ffmp3", x)))}
</%def>

<%def name="flowplayer()" filter="trim">
    <h3 class="box_header">IDL Live Video</h3>
    <div id="video">
        <a id="video_player" href="idlvideo"></a>
        <script>
            flowplayer("video_player", "${flow_link("flowplayer-3.2.7-0.swf")}", {
                plugins: {
                    rtmp: {
                        url: "${flow_link("flowplayer.rtmp-3.2.3.swf")}",
                        netConnectionUrl: "rtmp://totaltrash.org/rtmp/idlvideo"
                    },
                    clip: {
                        provider: "rtmp",
                        bufferLength: 1,
                        cuepointMultiplier: 1,
                        autoPlay: true,
                        live: true
                    }
                }
            });
        </script>
    </div>
</%def>

<%def name="ffmp3()" filter="trim">
    <object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="130" height="60" bgcolor="#FFFFFF">
        <param name="movie" value="${ffmp3_link("ffmp3-tiny.swf")}" />
        <param name="flashvars" value="url=http://totaltrash.org:8000/stream.ogg;&lang=en&codec=ogg&volume=50&traking=false&jsevents=true&title=IDL%20Radio&welcome=Loading..." />
    <param name="wmode" value="window" />
    <param name="allowscriptaccess" value="always" />
    <param name="scale" value="noscale" />
    <embed src="${ffmp3_link("ffmp3-tiny.swf")}" flashvars="url=http://totaltrash.org:8000/stream.ogg;&lang=en&codec=ogg&volume=50&traking=false&jsevents=true&title=IDL%20Radio&welcome=Loading..." width="130" scale="noscale" height="60" wmode="window" bgcolor="#FFFFFF" allowscriptaccess="always" type="application/x-shockwave-flash" />
    </object>
</%def>

<%def name="main_panel()" filter="trim">
    <div class="box">
        ${flowplayer()}
        <div id="radio">
        </div>
        <div class="box_footer">
        </div>
    </div>
</%def>

<%def name="side_panel()" filter="trim">
    ## Live (game or radio)
    ## Game video archives
    ## draft audio archives
    ## radio audio archives
</%def>

