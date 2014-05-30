<%namespace file="admin_widgets.mako" name="controls"/>
${controls.admin_list(
    context["module"],
    context["admin_entries"],
    "adminGet",
    context.get("model", None),
    context.get("entry", None)
)}
