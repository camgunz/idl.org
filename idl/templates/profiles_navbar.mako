<%namespace name="utils" file="utils.mako"/>

${utils.lower_navbar((
      ("players", url_for("random_player_profile")),
      ("maps", url_for("map_profiles")),
      ("player stats", url_for("all_time_player_stats"))
))}

