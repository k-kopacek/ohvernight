# Community and review signals

Whether public community sources can enrich water discovery, and what their
terms allow. Detail and quoted terms: Hermes
[track D](hermes/track-d-community-signals.md). The coordinator has not
re-read the terms pages; treat every row as Hermes's reading on 2026-10-06.

## Finding

Most sources with useful recreation chatter do not permit what a static,
open-source site would need to do with them: retrieve automatically, store,
and publish a derived summary.

| Source | Useful signal | Automated retrieval and stored summaries | Proposed use |
|---|---|---|---|
| Reddit | Activity mentions, conditions, crowding | API licence is revocable and limited to displaying content; modification beyond formatting not permitted | Link out only |
| Google Places | Reviews, popularity | Content may not be cached or stored, and may not be used with a non-Google map | Avoid |
| Yelp | Reviews at commercial places | 24-hour storage limit; geocodes not to be used in open-source maps | Avoid |
| Tripadvisor | Reviews | Systematic extraction needs written approval; content must not be indexable | Link out only |
| AllTrails | Trail conditions, parking, crowding | Automated searches, scraping and mining prohibited | Link out only |
| Fishbrain | Catch reports, species | Robots, scrapers, copying and third-party apps prohibited without consent | Link out only |
| Hipcamp | Listings near water | Automated scraping prohibited | Link out only |
| Paddling.com | Trip reports | Personal, non-commercial viewing only | Link out only |
| American Whitewater | Reach difficulty and flow | Terms page not found | Do not automate until terms are obtained |
| iNaturalist | Wildlife observations | API is "not data scraping"; content mostly CC BY-NC | Not needed for M4 |
| OpenStreetMap | Community tags for ramps, access, names | ODbL; use an extract | Comparison only |
| Wikidata | Identifiers and aliases | CC0 | Possible identity aid |
| USGS stream gauges | Current flow and stage | Public domain; not a community source | A separate "current gauge reading" idea, not M4 |

## Consequence for M4

There is no community source that is both useful for recreation sentiment and
clearly usable for automated, stored summaries. A community-signal pipeline
in M4 would be built on sources whose terms prohibit it or on sources with
little recreation content.

What remains possible without breaching terms:

- A link from a water feature's detail to a search on a community site, with
  no content retrieved or stored.
- A community observation entered by a person, as the existing unverified
  leads already are, with the contract's rule that it carries no
  verification method and establishes nothing about access.

## If community signals are added later

Minimum record, from Hermes with the contract's field rules applied: source
name; canonical URL; source's own id; matched water feature id and how it was
matched; date of the observation and date retrieved; the kind of signal
(fishing mention, paddling mention, swimming mention, crowding, parking,
condition); a short paraphrase, not copied text; the number of independent
observations where meaningful; the terms URL read; and any deletion or
refresh deadline. Hermes also suggests a `confidence` field; the data
contract has retired confidence fields and one should not be added.

A community signal never sets a claim's status, and is displayed apart from
official information.
