<%namespace name="utils" file="utils.mako"/>

${utils.lower_navbar((
      ("history", url_for("history")),
      ("rules", url_for("rules")),
      ("administrators", url_for("administrators")),
      ("servers", url_for("servers")),
      ("credits", url_for("credits"))
))}
