<%namespace name="utils" file="utils.mako"/>

${utils.lower_navbar((
      ("standings", url_for("standings")),
      ("schedule", url_for("schedule")),
      ("leaders", url_for("season_leaders")),
      ("players", url_for("season_player_stats")),
      ("teams", url_for("season_team_stats")),
      ("demos", url_for("demos"))
))}
