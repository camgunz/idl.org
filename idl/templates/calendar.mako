<%namespace name="controls" file="admin_widgets.mako"/>
${controls.base_calendar(
    context["dt"],
    context["mclass"],
    context["eid"],
    context["eclass"],
    context["deid"],
    context["hidden"]
)}
