<script type="text/javascript">
    % if context.get("error", None):
        window.top.window.${context["func"]}(${context["error"]})
    % else:
        window.top.window.${context["func"]}(null)
    % endif
</script>
