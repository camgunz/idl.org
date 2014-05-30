<div class="box">
    <h3 class="box_header">Season Jump</h3>
    <div class="box_body">
        <div id="season_select_form" class="form">
            <label>Select a season:</label>
            <select id="season_id" name="season">
                <option value="${context["session"]["season"].id}">${context["session"]["season"].season.capitalize()} ${context["session"]["season"].year}</option>
                % for season in reversed(context["seasons"]):
                    % if season != context["session"]["season"]:
                        <option value="${season.id}">${season.season.capitalize()} ${season.year}</option>
                    % endif
                % endfor
            </select><br/>
        </div>
    </div>
</div>

