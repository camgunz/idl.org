<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="css()" filter="trim">
    ${utils.css_link("box_scores.css")}
    ${utils.css_link("rules.css")}
</%def>

<%def name="js()" filter="trim">
    ${utils.jquery_link()}
    ${utils.js_link("idl.js")}
</%def>

<%def name="main_panel()" filter="trim">
    <div class="box">
        <%include file="info_navbar.mako"/>
        <div class="box_body">
            <h3 class="box_body_header rules">Official IDL Rules</h3>
            <h4 class="rules">The IDL Administration</h4>
            <p class="rules">
                The IDL Administration is comprised of one commissioner and
                a board of five IDL community members.  Throughout these rules,
                this collection of six officers are collectively referred to as
                "the IDL administration", each board member and commissioner
                being an "IDL administrator", "IDL admin", or simply
                "administrator" or "admin".  All admins have RCON to IDL
                servers and are IRC channel operators, but save for the
                commissioner and board head have no inherent policy enforcement
                authority.
            </p>
            <h5 class="rules">The Commissioner</h5>
            <p class="rules">
                The IDL Commissioner's office is a one person office whose
                duties are to enforce IDL policy.
            </p>
            <h5 class="rules">Commissioner Selection</h5>
            <p class="rules">
                The commissioner can appoint a successor at the time of
                resignation.  Should no successor be chosen, the board must
                select a new commissioner via unanimous vote.
            </p>
            <h5 class="rules">Commissioner Removal</h5>
            <p class="rules">
                The commissioner can resign at any time.  The board can remove
                a commissioner with a unanimous vote.
            </p>
            <h5 class="rules">The Board</h5>
            <p class="rules">
                The IDL Board is a group of five IDL community members - four
                board members and one board head - whose responsibility is to
                set IDL policy to suit the league and its players.  It is
                neither the responsibility nor the privilege of regular board
                members to enforce IDL policy, this is left to the board head
                and commissioner.
            </p>
            <h5 class="rules">Board Member Selection</h5>
            <p class="rules">
                Board members are selected through a nomination and
                confirmation process.  The commissioner nominates candidates,
                and the board must confirm the nomination with a 3/5 majority.
                New members fill the previous members' seats.  For example,
                should the board head resign, their replacement becomes the new
                board head.
            </p>
            <h5 class="rules">Board Member Removal</h5>
            <p class="rules">
                Board members can resign at any time.  Board members may be
                removed through the removal process:
            </p>
            <ul>
                <li>The member to be removed is notified.</li>
                <li>The other board members vote on removal.</li>
                <li>If a 4/4 unanimous vote is obtained, removal succeeds.</li>
                <li>
                    Otherwise if a 3/4 majority is obtained, removal succeeds
                    unless the commissioner vetoes.
                </li>
                <li>
                    The commissioner's veto can be overridden by a unanimous
                    vote, otherwise removal fails.
                </li>
            </ul>
            <h5 class="rules">Board Member Promotion &amp; Demotion</h5>
            <p class="rules">
                Promotion of a normal board member to board head, or demotion
                of the board head to a normal board member must be done via the
                nomination/confirmation process.  The member in question cannot
                vote during this time, thus confirmation requires a 3/4
                majority.
            </p>
            <h5 class="rules">Acting In <i>Bona Fide</i></h5>
            <p class="rules">
                Administrators must act honestly and in <i>bona fide</i>.  The
                test is a subjective one; administrators must act in good
                faith, in what they - not the rest of the board - consider best
                for the league.  However, administrators may still be held to
                have failed in this duty where they fail to direct their minds
                to the question of whether in fact a transaction was in the
                best interests of the league.
            </p>
            <h5 class="rules">Competing With The League</h5>
            <p class="rules">
                IDL administrators may not act as administrators of competing
                leagues.
            </p>
            <h4 class="rules">Legislation</h4>
            <h5 class="rules">Voting Procedure</h5>
            <p class="rules">
                In order to make changes to the IDL rules, the board must vote
                on each proposition.  Votes can be called in two ways, either
                through the commissioner sending an issue to the board, or the
                board head calling a vote.  Votes pass with a 3/5 majority,
                after which the commissioner can exercise his veto power.
                Should the veto be employed, the board can override the veto
                with a 4/5 majority.
            </p>
            <p class="rules">
                Board members can abstain from voting, but this action does not
                change the amount of votes required for passage.
            </p>
            <h5 class="rules">Restrictions</h5>
            <p class="rules">
                The board may not pass any proposition to be enforced
                retroactively.
            </p>
            <h4 class="rules">League Composition</h4>
            <h5 class="rules">Structure</h5>
            <p class="rules">
                The IDL is currently a single group league consisting of eight
                teams. Teams are composed of one captain and three players. As
                the head of their teams, captains have the power (and often the
                responsibility as the rules require) to:
            </p>
            <ul>
                <li>Dismiss players</li>
                <li>Submit team availability for games</li>
                <li>Trade with other teams</li>
                <li>Name their teams</li>
            </ul>
            <h5 class="rules">Captain Selection</h5>
            <p class="rules">
                The IDL administration selects and randomly assigns captains to
                teams.  Once assigned, the captain retains that team until
                removed.
            </p>
            <h5 class="rules">Captain Removal</h5>
            <p class="rules">
                Captains can resign at any time, however they're strongly
                discouraged from doing so during a season. A captain can be
                dismissed by the administration's majority vote for serious
                objective reasons, such as damaging the quality of the league,
                at anytime. A possible commissioner's veto has to be overruled
                by a 4/5 majority.
            </p>
            <h5 class="rules">Team Name Selection</h5>
            <p class="rules">
                Captains have the opportunity to name or rename their teams
                each season.  New captains have this opportunity after
                assignment unless assignment occurs during the regular or post
                seasons.  Names are subject to board review, with a 4/5
                majority required to reject a name.  The board may only
                evaluate names on objective bases such as obscenity; personal
                like or dislike shall not determine a board member's approval
                or disapproval.  Should a team's captain be unable or unwilling
                to select an acceptable name, the administration will select a
                name for that team.
            </p>
            <h4 class="rules">Player Dismissal</h4>
            <h5 class="rules">Cheating</h5>
            <p class="rules">
                Players caught cheating during IDL games will be banned from
                all IDL servers and activities for the entirety of the season.
                Their application for future seasons will be heavily reviewed.
                The games in which that player played will all be overturned in
                favor of the opposing team.  Games that player's team lost will
                remain as they were.
            </p>
            <h5 class="rules">Chronic Absence</h5>
            <p class="rules">
                The league can decide to dismiss players for chronic absence.
                Chronic absence is evaluated on a case-by-case basis.
            </p>
            <h5 class="rules">Replacement</h5>
            <p class="rules">
                Should a player withdraw or be dismissed from the league, the
                captain of that player's team has seventy-two hours to replace
                the player from free agency, after which the IDL administration
                will choose instead.  Such replacement does not count as a
                trade.  Replacement is not required (nor is it possible) during
                the postseason.
            </p>
            <h4 class="rules">End of Season Dismissal</h4>
            <p class="rules">
                Each team's players are automatically dismissed at the end of
                that team's season, save for captains.
            </p>
            <h4 class="rules">Invitation</h4>
            <p class="rules">
                After captains are assigned, players register during a sign-up
                period determined by the commisioner. Registration can take
                form of an open forum post or a message to a member of the IDL
                administration. After the sign-up period, the administration
                confirms the IDL roster. Removal of a registered player has to
                be confirmed by a majority vote. Excluding captains, all
                players on the IDL roster are then considered free agents.
            </p>
            <h4 class="rules">Draft</h4>
            <p class="rules">
                Draft order for captains who were captains in the previous
                season is determined by the following criteria:
            </p>
            <ol>
                <li>Ascending previous regular season record</li>
                <li>MasterBowl runner-up</li>
                <li>MasterBowl champions</li>
            </ol>
            <p class="rules">
                Should two or more teams have identical records, the following
                procedures will be used to determine draft order:
            </p>
            <ol>
                <li>
                    Non-playoff teams pick before teams that earned playoff
                    berths
                </li>
                <li>
                    Playoff teams are chosen in the order in which they lost
                    during the playoffs
                </li>
                <li>
                    Outcome of the head-to-head matches, the loser teams pick
                    first
                </li>
                <li>Strength of schedule</li>
                <li>Flags for</li>
                <li>Flags against</li>
                <li>Number of infractions against match rules</li>
                <li>Coin toss</li>
            </ol>
            <p class="rules">
                Draft order for captains who were not captains in the previous
                season but have been captains before is determined by their
                total captaining record.
            </p>
            <p class="rules">
                Draft order for captains who have never captained a team is
                randomly determined.  Once these random draft positions have
                been assigned, they will be modified as follows:
            </p>
            <ul>
                <li>
                    If assigned position one, two or three, the position is
                    set to four, five or six, respectively, pushing other
                    captains upwards.
                </li>
                <li>
                    If assigned position ten, eleven or twelve, the position is
                    set to seven, eight or nine, respectively, pushing other
                    captains downwards.
                </li>
            </ul>
            <p class="rules">
                Once draft order is determined, captains must choose their
                draft positions.  This is done following the draft order; the
                captain of the team with the first pick can choose draft
                position one through twelve, the captain of the team with the
                second pick can choose draft position one through twelve save
                the position the first captain chose, and so on.
            </p>
            <p class="rules">
                Each draft round reverses the picking order; the team with
                first pick in the first round has the twelfth pick in the
                second round, second pick has eleventh pick, and so on.
            </p>
            <p class="rules">
                Draft positions may not be traded.
            </p>
            <h4 class="rules">Playoff Homefield Selection</h4>
            <p class="rules">
                A playoff match's map is the top-seeded team's chosen
                homefield.  For example, TBA and MAD are in the semifinal game,
                TBA is ranked 8th and MAD is ranked 4th.  That game will be
                played using MAD's homefield map.
            </p>
            <p>
                Each team chooses a playoff homefield map and an optional
                fallback map from that season's IDL WAD in the reverse of draft
                order, and the following restrictions apply:
            </p>
            <ul>
                <li>Teams cannot choose that season's MasterBowl map.</li>
                <li>
                    Teams cannot choose a fallback map that was previously
                    selected that season by a different team.
                </li>
            </ul>
            <p class="rules">
                The fallback map becomes a team's homefield if their primary
                map pick has been chosen by a lower ranked team that has
                qualified for the playoffs.
            </p>
            <p class="rules">
                Homefields must be selected before the conclusion of Week 6 of
                regular season play.  Homefield selection position can be
                traded.
            </p>
            <h4 class="rules">Season Gameplay</h4>
            <p class="rules">
                The IDL has four seasons:
            </p>
            <dl>
                <dt>Preseason</dt>
                <dd>
                    The period of time between the end of the draft and the
                    first regular season week.
                </dd>
                <dt>Regular Season</dt>
                <dd>A seven week period where games are played weekly.
                    Determines the seeding for the playoff season and the next
                    season's draft order (in most cases).
                </dd>
                <dt>Playoff Season or Postseason</dt>
                <dd>
                    A three week period where games are played weekly (Wildcard
                    Playoffs, Semifinals, and the MasterBowl
                    respectively).  Determines that season's champion and, in
                    some cases, draft order.
                </dd>
                <dt>Off Season or Offseason</dt>
                <dd>
                    The period of time between the end of playoff season and
                    the draft.
                </dd>
            </dl>
            <h5 class="rules">Playoff Season</h5>
            <p class="rules">
                Playoffs consist of three rounds: Wildcard, Semifinals, and the
                MasterBowl.  The top five teams of the league qualify for
                playoffs.  The top ranked team faces the winner of the Wildcard
                round.
            </p>
            <p class="rules">
                Should ties occur between two or more teams, they will be
                broken using the following procedures:
            </p>
            <ol>
                <li>
                    Head-to-head (a mini-ladder consisting of head-to-head
                    matches of the tied teams)
                </li>
                <li>Best total won-lost-tied percentage</li>
                <li>Strength of victory</li>
                <li>Flags for</li>
                <li>Flags against</li>
                <li>Number of infractions against match rules</li>
                <li>Coin toss</li>
            </ol>
            <p class="rules">
                Only one team advances to the playoffs in any tie-breaking
                step. Remaining tied teams revert to the first step of the
                tie-breakers.
            </p>
            <h4 class="rules">Gameplay</h4>
            <h5 class="rules">Game Structure</h5>
            <p class="rules">
                Each IDL game is played in a best-of-three fashion. A standard
                IDL round is 3 vs. 3 at ten minutes each, with a five flag
                limit. When the time or flag limit is reached, the team with
                the most flags scored is the winner of the round. If the amount
                of flags scored is equal, that round is a tie. If no team wins
                both regular rounds, a third tie-breaker round is played.
                During the regular season, the result of this round ties up the
                outcome of the game based on rounds won.  During the
                postseason, such tie-breaking rounds are played until one of
                the teams wins two rounds total. 
            </p>
            <h5 class="rules">Team Color Assignments</h5>
            <p class="rules">
                Teams are assigned specific colors for each game.  This is
                determined by the order in which team names are displayed on
                the IDL site.  For example, if a game is listed as BSK vs. SUC,
                BSK is the red team and SUC is the blue team.  The assignments
                are determined randomly.
            </p>
            <h5 class="rules">Game Location</h5>
            <p class="rules">
                All games must be played on official IDL servers, which are
                listed on the IDL site. Games played on other servers will not
                be recognized. The server hosting the game must be agreed upon
                at least twenty-four hours before the game is scheduled to take
                place, and all rounds of said game must be played on the same
                server.  In the event of server disputes, or should no
                discussion take place, IDL Chicago will be used. Should the
                hosting server become unavailable during a scheduled game time,
                that game will be postponed.
            </p>
            <h5 class="rules">Game Rosters</h5>
            <p class="rules">
                Excepting power play penalties, teams are required to field
                three players.  If they are unable to do so, the IDL will
                forfeit that team.  If neither team is able to field three
                players, they will both forfeit.
            </p>
            <p class="rules">
                Captains are free to substitute players in at will, however,
                the limit of three players per team must not be exceeded at any
                time.  Should a team ever have more than three players playing
                in the game at the same time (joining the game on a team),
                regardless of circumstances that team will forfeit the round
                with their stats being set to zero.
            </p>
            <h5 class="rules">Server Crashes</h5>
            <p class="rules">
                Server crashes are handled at the league's discretion and on a
                case-by-case basis.  However, these are guidelines the league
                generally follows.
            </p>
            <p class="rules">
                In the event of a server crash, games are replayed from the
                last benchmark.  Scores and statistics up until the last
                benchmark will be carried over and recorded respectively.
                Other information (flag possession, player positions, etc.) as
                well as all events occurring after the benchmark will be
                discarded.  Each game has eight benchmarks:
            </p>
            <ol>
                <li>0:00</li>
                <li>2:00</li>
                <li>3:00</li>
                <li>4:00</li>
                <li>5:00</li>
                <li>6:00</li>
                <li>7:00</li>
                <li>8:00</li>
            </ol>
            <p class="rules">
                Should a team feel that something extraordinary happened very
                close to a benchmark, they can appeal to the commissioner to
                have it included in the game replay.  For example, if a player
                is imminently about to score, a team can have the commissioner
                or review the demo to ensure there was no possibility of the
                player not scoring (within the realm of normalcy), and award
                the flag capture.
            </p>
            <h4 class="rules">Trading</h4>
            <p class="rules">
                A trade is an exchange between either two teams or one team and
                the free agency.  If between two teams, one team gives one
                player to another team and receives one other player from the
                same team.  If between one team and the free agency, the team
                gives one player to the free agency and takes one other player
                from the free agency.  In either case, both player transfers
                happen at the same time and only under both captains' (or the
                captain's) consent.
            </p>
            <p class="rules">Trading during the preseason is unlimited.</p>
            <p class="rules">Trading during the postseason is not allowed.</p>
            <p class="rules">
                Trading is allowed during the regular season up until Week 5 on
                Wednesday, 11:59:59pm, subject to the following:
            </p>
            <ul>
                <li>
                    All trades must be commissioner approved and will be
                    recorded publicly.
                </li>
                <li>
                    Each team is allowed a maximum of three trades during the
                    regular season.
                </li>
                <li>
                    If two teams trade and neither has played their game, that
                    trade becomes effective immediately for both teams.
                    Otherwise the trade is not effective until Monday
                    12:00:00am of the next week.
                </li>
                <li>
                    Trades made during Week 5 become effective Thursday
                    12:00:00am or until both teams have played their games,
                    whichever is latest.
                </li>
            </ul>
            <p class="rules">
                Each team may trade any number of times per week, but is
                allowed a maximum of three trades during the regular season.
            </p>
            <p class="rules">
                Once a player has been in the roster of two different teams,
                they cannot return to the roster of the original team for the
                rest of the season.
            </p>
            <p class="rules">
                Whenever a team trades a player to the free agency, a
                forty-eight hour cold period where that player cannot be
                instantly traded for begins.  During this period, teams can
                make a bid for the player.  If more than one bid is made, the
                player will go to the team with the lowest win-tie-loss record
                of the current season.  If ties occur, they will be resolved
                using the following procedures:
            </p>
            <ol>
                <li>
                    Head-to-head (best won-lost-tied percentage in games
                    between the teams)
                </li>
                <li>Strength of victory</li>
                <li>Strength of schedule</li>
                <li>
                    Regular season frag average multiplied by regular season
                    flag average
                </li>
                <li>Coin toss</li>
            </ol>
            <p class="rules">
                If a team is unable to field three players for a match, that
                team must use a player from free agency for the duration of the
                match.  This does not count as a trade.
            </p>
            <p class="rules">
                Should a team use a particular free agent twice, that team will
                be forced to make a trade for said free agent using any player
                currently on its roster.  This counts as a trade.
            </p>
            <h5 class="rules">Waiver Wire</h5>
            <p class="rules">
                The waiver wire opens at the close of the trade deadline. Teams
                can drop any of their players during this time, however, the
                dropped player will be placed on the waiver wire until the
                following Monday at 11:59:59pm, henceforth referred to as the
                waiver period. During the waiver period, any team may make a
                blind claim for the player. When such a claim is made, teams
                are told only that a claim was made, not which team made the
                claim. At the end of the waiver period, the player is either
                acquired by a claiming team or passed into free agency.
                Tie-breaking procedure is used to determine claim precedence,
                however, once a team acquires a player through a claim they are
                sent to the end of the order. If no team makes a claim within
                the waiver period, the player becomes a free agent. Any team
                that wins a claim must take the player onto their roster.
            </p>
            <h5 class="rules">Postseason Roster Changes</h5>
            <p class="rules">
                Teams are not permitted to make any roster changes during the
                postseason.
            </p>
            <h4 class="rules">Demos</h4>
            <p class="rules">
                Each player that plays in a round, no matter the length of
                time, is required to submit a demo either by Wednesday of the
                following week, or before their team's next game, whichever
                comes first.  The penalties for not submitting a demo are as
                follows:
            </p>
            <ul>
                <li>First Infraction: Three minute power play.</li>
                <li>
                    Second Infraction: Player is suspended for one round of
                    play.
                </li>
                <li>Third Infraction: Player is ejected from the league.</li>
            </ul>
            <h4 class="rules">Scheduling</h4>
            <p class="rules">
                Captains are required to send their team's weekly availability
                to the commissioner by Tuesday 11:59:59pm.  The commissioner
                will then select an appropriate game time where both teams are
                available.  In the event that schedules do not overlap, the
                commissioner will design a solution on a case-by-case basis.
                Should teams fail to send their availability in on time, they
                will be punished as follows:
            </p>
            <ul>
                <li>
                    First &amp; Second Infractions: Three minute power play.
                </li>
                <li>
                    Third &amp; Subsequent Infractions: One round man
                    advantage, with no relief even if flags are scored.
                </li>
            </ul>
            <p class="rules">
                Non-captain players cannot schedule times with the
                commissioner, nor can teams schedule times between themselves;
                captains submit availability to the commissioner, and the
                commissioner assigns the game time.
            </p>
            <h5 class="rules">Schedule Changes</h5>
            <p class="rules">
                In the event that a player's or team's availability changes
                after a game time is assigned, the commissioner can rule
                whether or not to move the game time to another available time
                based upon previously submitted availability.
            </p>
            <h4 class="rules">Miscellaneous</h4>
            <h5 class="rules">Power Play</h5>
            <p class="rules">
                Players, not teams are penalized with a power play.  The
                penalty cannot be transferred to a different player, and if
                traded the player will serve the penalty on whichever team they
                ultimately play their game.  Captains cannot substitute
                non-offending players to compensate for the power play; teams
                must play down a player for every penalty.
            </p>
            <p class="rules">
                For example, Whopper and Alvis of the Knortic Fnords both fail
                to upload their demo for Week 4.  During Week 5, KNF must play
                1v3 until three minutes elapse or their opponents score, and
                Whopper and Alvis must sit during this time.
            </p>
            <h5 class="rules">Time Zone</h5>
            <p class="rules">
                All times, unless otherwise noted, are in EST/EDT.  The
                official IDL forums are configured to report times in EST/EDT,
                so no adjustment is necessary unless players have changed their
                forum profiles.
            </p>
            <h5 class="rules">Versions of Odamex Client and Server Programs</h5>
            <p class="rules">
                The official IDL servers run version 0.6.X of the Odamex
                server.  The IDL recommends running the latest stable version
                of the Odamex client.  Consequences resulting from the use of
                other client versions are the responsibility of the player, not
                the IDL.
            </p>
        </div> <!-- box body -->
    </div> <!-- box -->
</%def>

<%def name="side_panel()" filter="trim">
    <%include file="latest_games.mako"/>
</%def>

