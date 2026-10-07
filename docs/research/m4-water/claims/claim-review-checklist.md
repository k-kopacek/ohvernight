# Claim review checklist (M4-C)

The framework the owner and the coordinator use when a water recreation
record is proposed for `water-recreation.json`. Proposed by the coordinator;
it restates specification section 9 as checks and adds worked examples. A
dossier from Hermes is an input to this review, never a substitute for it.

## 1. The checklist

For each record (one water) and each of its activities:

| # | Check | How |
|---|---|---|
| 1 | The source is the operator or managing agency | The page is on the operator's or agency's own site. Not a dataset, map layer, news article, guidebook, forum or review site |
| 2 | The source refers to this water | The page names the water, and the name matches the canonical feature by more than the name alone: the operator, county and location agree. Two waters can share a name |
| 3 | The activity is supported independently | The sentence relied on is about this activity. It is not a sentence about another activity, a facility, a designation or stocking |
| 4 | The status follows the definitions | Allowed: offered with no condition beyond general law. Restricted: allowed only with conditions specific to this water. Prohibited: stated as not allowed. Unknown: none of these is established |
| 5 | The summary does not overstate | At most 160 characters, the reviewer's own words, no more permissive than the sentence, no advice, no "safe", no "great for" |
| 6 | A positive claim is current | The page is live on the review date and shows no notice suspending the activity. A dated notice is recorded |
| 7 | A restriction stays conservative | Where the page is ambiguous between restricted and prohibited, the record says prohibited or unknown, never the more permissive reading |
| 8 | Access is not inferred | Access is `unknown` unless the page states an access rule, in which case it is `restricted` with that sentence. Access is never `allowed` in M4. A trailhead, a road, public land or visitors do not establish access |
| 9 | Dates are captured | `last_checked_at` and `last_confirmed_at` are the date a person read the page; the page's own "last updated" date is noted if shown |
| 10 | The source link is captured | An HTTP(S) URL that opens the page relied on, not a home page or a search result |
| 11 | The maximum age is justified | 90 days by default. Shorter for seasonal rules, dated orders and anything the page says may change. The reason is written down |
| 12 | Conflicts are noted | If two official pages disagree, the record takes the more restrictive reading or stays unknown, and the conflict is written in the record's notes and raised with the owner |
| 13 | Boating and paddling are both considered | A sentence about "all boating" may support both, each with its own evidence object and summary. A sentence about motorboats does not cover paddlecraft, and the reverse |
| 14 | Nothing is derived from another record | A rule at one reservoir says nothing about the next one, even with the same operator |
| 15 | Seasonal rules are restricted, not toggled | A seasonal closure is a restricted claim whose summary states the season. The record is not flipped by date |

A record passes when every activity passes every applicable check. An
activity that fails any check is recorded as `unknown`. A record with four
unknown activities and unknown access is not written.

## 2. Worked examples

Each example is a pattern, not a production record. Quoted sentences were
read on the operators' pages by the coordinator on 2026-10-06 or 2026-10-07
unless marked as hypothetical.

### Valid: prohibited

Cheesman Lake, boating. Operator page (Denver Water) states: "Prohibited: All
boating and camping." Status `prohibited`. Summary: "All boating prohibited."
The same sentence supports paddling `prohibited`, as its own evidence object.

### Valid: prohibited by a dated order

Maroon Lake, paddling. Forest order WRNF-2022-03 prohibits "Entering or being
in Maroon Lake, including with any non-motor vehicles such as a kayak, canoe,
raft, or fishing float tubes." Status `prohibited`. The order runs to
15 November 2027 unless rescinded: `effective_to` is set, and the maximum age
is short enough to catch a rescission. The order does not address fishing
from the shore, so fishing is `unknown`.

### Valid: restricted

Rueter-Hess Reservoir, paddling. The operator page states reservations are
required and limits craft and days. Status `restricted`. Summary names the
conditions: "Reservation required; approved hand-launched craft only; set
days and hours."

### Valid: restricted, seasonal

Chatfield Lake, swimming. Operator page (CPW): "The swim beach is open
seasonally from Memorial Day through Labor Day." Status `restricted`.
Summary: "Designated swim beach only, Memorial Day to Labor Day."

### Valid: allowed

Hypothetical, because no reviewed water yet meets it: an operator page that
states "Fishing is allowed from the shoreline" with no place, season, permit
or gear condition specific to that water. Status `allowed`. A state fishing
licence is general law and is not a condition. If the page adds "on the east
shore only" the status is `restricted`.

### Valid: unknown

Grizzly Reservoir, every activity. No operator or agency page was found that
states what is allowed. Every activity `unknown`; no record is written; the
detail shows "Mapped water. Access and allowed activities are not
established."

### Invalid: inference from a boat ramp

"The CPW Fishing Atlas shows a boat ramp at this lake, so boating is
allowed." Rejected by checks 1, 3 and 4. A ramp is a facility: it exists. It
does not say which craft may launch, when, or whether the ramp is open.
Boating stays `unknown` until the operator's page says so.

### Invalid: inference from stocking or designation

"CPW stocked this lake in June" or "this reach is Gold Medal water, so
fishing is allowed." Rejected by checks 3 and 4. Stocking is an event and a
designation is a classification of the fishery. Neither states that the
public may fish there or can reach the bank.

### Invalid: inference from trail access

"A Forest Service trail leads to the lake, so access is allowed and swimming
is fine." Rejected by checks 3 and 8. A trail establishes a trail. Access is
`unknown`, or `restricted` if the page states a rule such as a permit or
reservation. Swimming is `unknown`.

### Invalid: community-sourced permission

"Several Reddit threads and AllTrails reviews say people paddleboard here."
Rejected by check 1. People doing something is not permission. This is a
community signal; M4 stores none, and no community signal can ever set a
claim.

### Invalid: one operator, another water

"Denver Water prohibits boating at Cheesman, so it must at Platte Canyon
Reservoir too." Rejected by checks 2 and 14.

### Invalid: summary overstates

Source: "Fishing: Allowed only on the Goose Creek Arm." Summary written as
"Fishing allowed." Rejected by check 5. Correct: status `restricted`,
summary "Fishing only on the Goose Creek Arm."

## 3. What the owner approves in the pull request

For every non-unknown claim: the water, the activity, the status word, the
summary, the URL, the sentence relied on (in the pull request description,
not in the data), the review date and the maximum age. The owner's approval
of the pull request is the approval of each claim in it.
