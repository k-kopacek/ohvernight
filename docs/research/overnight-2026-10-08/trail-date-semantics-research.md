DRAFT - UNREVIEWED RESEARCH

# USFS TrailNFS_Publish date-range fields: what they mean

Mission: Hermes research plane, bounded. Retrieval times are UTC, 2026-10-08 (22:11Z to 22:14Z). Budget used: 2 web searches, about 7 retrievals. No git state changed, nothing else modified.

## Bottom line

Does a trip date outside the ACCEPTED range mean the use is not allowed?   NO (as a reading of the dataset definitions), with the limit that the documentation also never says the use IS allowed.

- The dataset defines ACCPT as "use is allowed, but not managed or restricted" (see table). The date range lists when that "allowed, not managed" status applies. It is not defined as the full window of legal use.
- A date outside the ACCPT range can fall inside the MANAGED range (the primary use season), inside DISC or RESTRICTED, or in a gap where no field says anything. Only the RESTRICTED range is defined as a restriction.
- The app's "Outside published use dates" test, based on ACCPT alone, is therefore a misreading. A summer motorcycle trail with MANAGED 05/01-11/30 and ACCPT 12/01-03/14 is correctly the opposite of what the app says.
- The Motor Vehicle Use Map (MVUM) is the legally controlling instrument for motorized use. The dataset itself is not (see Section 3).

What the data does not answer (UNKNOWN): how a gap date (covered by none of the five fields) should be treated; whether a missing field means "not applicable", "not recorded" or "no season data"; how the publisher intends date ranges that wrap year end to be parsed (see Section 2).

## 1. Fields (motorcycle shown; same pattern for every activity prefix)

Source: FGDC metadata for S_USA.TrailNFS_Publish, USDA Forest Service, Enterprise Data Warehouse, pubdate 2025-05-14, metadata date 2024-07-24.
URL: https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml (retrieved 2026-10-08T22:11Z)

Live layer (the service fetch_trails.py uses): https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublishWithDataStatus_01/MapServer/0 (retrieved 2026-10-08T22:11Z). The published field names are lower-case in the JSON (motorcycle_managed, etc.) and match the metadata.

| Source field | Publisher definition (attrdef, quoted) | Value-domain text (quoted) | What a range means | Confidence |
|---|---|---|---|---|
| MOTORCYCLE_MANAGED | "Indicates TERRA trails that are designed and managed to accommodate motorcycle use year-round or seasonally" | "Date range for which motorcycle use is managed" | Season in which the agency intends and manages the trail for the use (management intent, Managed Use concept). | High that it is management intent, not a permit. |
| MOTORCYCLE_ACCPT | "Indicates TERRA trails where motorcycle use is allowed, but not managed or restricted seasonally or year-round." | "Date range for which motorcycle use is accepted." | Dates when use is allowed but not managed for. Not a complete list of allowed dates. | High on wording; the wording is terse. |
| MOTORCYCLE_DISC | "Indicates TERRA trails where motorcycle use is discouraged, but not managed or restricted seasonally or year-round." | "Date range for which motorcycle use is discouraged." | Dates when use is discouraged (not prohibited). | High |
| MOTORCYCLE_ACCPT_DISC | "Indicates TERRA trails where motorcycle use is allowed or discouraged, but not managed or restricted seasonally or year-round." | "Date range for which motorcycle use is accepted or discouraged." | One combined field. The metadata gives no way to tell accepted from discouraged inside it; use the separate _ACCPT and _DISC fields for that, where populated. | High that it is combined; UNKNOWN how to split. |
| MOTORCYCLE_RESTRICTED | "Indicates TERRA trails where motorcycle use is restricted year-round" | "Date range for which motorcycle use is restricted." | The only field defined as a restriction. Note the definition says "year-round" but the value text says "date range"; live records carry partial-year ranges (see Section 5). The metadata does not define "restricted" (prohibited vs limited). | Medium |

Also relevant: ALLOWED_TERRA_USE: "Indicates uses on TERRA Trails that are legally allowed on the trail ... Formed by concatenating the value for each allowable use" (code 4 = Motorcycle, 1 Hiker, 2 Pack and Saddle, 3 Bicycle, 5 ATV, 6 4WD>50"). This is the only field in the dictionary labelled "legally allowed", and it has no dates. A blank is "Not recorded". N/A means "Not populated for this Attribute Subset".

The manager of the dataset is Forest-by-Forest: the same metadata lists ATTRIBUTESUBSET TRAILNFS_MGMT as the level that "adds Access and Travel Management data for motorized and non-motorized uses (managed, accepted, prohibited uses)". These fields only exist for TRAILNFS_MGMT records.

## 2. Date formats and empty values

- Format: the TrailNFS_Publish metadata for the activity fields does not state a format. The e-bike entries in the same file say "Format is MM/DD." (e.g. E_BIKE_CLASS1_ACCPT, citing the "NRM ATM Data Dictionary", an internal USFS site not reachable). The TMO form in Trail Fundamentals labels the fields "From Date (mm/dd)" and "To Date (mm/dd)". So MM/DD-MM/DD is the documented pattern.
- Year-end wrap (12/01-03/14): UNKNOWN. No retrieved text states how a range whose end is earlier than its start is read. A wrap reading (Dec 1 through Mar 14) is the natural interpretation and matches live records (see Section 5), but it is inference, not a publisher statement.
- "01/01-12/31" is evidently a full-year range; the documentation does not say so explicitly. Trailing spaces occur in live values ("12/01-03/14 "). Multiple ranges in one value: UNKNOWN (none seen in the sample).
- Empty value: the domain values read "<blank>: Not recorded" and "N/A: Not populated for this Attribute Subset". A blank therefore means not recorded, not "none" or "not allowed". The app's own comment in fetch_trails.py ("Missing is unknown, never allowed") agrees.

## 3. What the attributes are: permission, intent or restriction

Trail Fundamentals and Trail Management Objectives, USDA Forest Service, MTDC 1623-3801, updated September 2016 (cites FSH 2309.18 sec. 14.3).
URL: https://www.fs.usda.gov/recreation/programs/trail-management/documents/trailfundamentals/1623-3801_TrailFdml+TMO_Sec508_11-14-16_150dpi.pdf (retrieved 2026-10-08T22:13Z)

- "Managed Use is a mode of travel that is actively managed and appropriate on a trail, based on its design and management. 1. Managed Use indicates management intent to accommodate a specific use."
- "The Managed Uses for a trail are usually a small subset of all the allowed uses on the trail, that is, uses that are allowed unless specifically prohibited."
- The TMO form's "Travel Management Strategies" block (FSM 2353.19) has columns Managed Use, Accept, Discourage, Eliminate and Prohibited Use, each with From/To dates (mm/dd). This is the origin of the managed / accepted / discouraged / restricted four-way split. The dataset's four categories map to these TMO strategies, which is management intent, not enforcement text. (Interpretation: the form layout as extracted is garbled; the column names are from the extract, the mapping to the dataset is my inference. Confidence medium.)
- The guide's own disclaimer: "This report does not constitute a standard, specification, or regulation."

Legal instrument for motorized use:
- Layer description of TrailNFS_Publish (and the metadata abstract): "When a Forest chooses to provide the highest attribute subset, TrailNFS_Mgmt, these attributes must be consistent with the Forest's published Motorized Vehicle Use Map (MVUM)." (sic: the publisher wrote "Motorized".) This is a consistency requirement, not a statement that the layer is the legal source.
- Forest Service Manual 7730, as shown in search snippet only (not fully retrieved): "Once designations are complete and reflected on a motor vehicle use map, motor vehicle use inconsistent with those designations is prohibited (36 CFR 261.13)." URL: https://www.usda.gov/sites/default/files/guidance-documents/ForestService.Manual%207700%207730%20Transportation%20System%20Operation%20and%20Maintenance.pdf. Needs a full read by Claude.
- Forest page (Gifford Pinchot NF, one forest, illustrative only): MVUM "is used by law enforcement and Forest staff to enforce which roads are legally open"; roads/trails are "designated by type of motor vehicle allowed and the allowable season of use". URL: https://www.fs.usda.gov/r06/giffordpinchot/maps-guides/motor-vehicle-use-map-mvum (snippet only).
- The sibling EDW layer for MVUM designations is S_USA.Trail_MVUM (EDW_MVUM_01 service), which carries explicit open-date fields (e.g. MOTORCYCLE_DATESOPEN, "Dates route is open for motorcycle travel"). Its metadata: "Any reference to Open or Dates Open refers strictly to when it is legal to use that motor vehicle on the trail." URL: https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.Trail_MVUM.xml (retrieved 2026-10-08T22:12Z); service: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_MVUM_01/MapServer. By contrast, TrailNFS_Publish uses no word like "legal" for its date fields.

Verdict: the date fields in TrailNFS_Publish are management intent / travel-management strategy (MANAGED, ACCPT, DISC) plus a restriction field. They are not the legal permission instrument. Legal permission for motorized use is the MVUM (36 CFR 212.56 designation; 261.13 prohibition).

## 4. Publisher caveats

- TrailNFS_Publish use constraint (metadata, quoted): "The USDA Forest Service makes no claims, promises, or guarantees about the accuracy, completeness, or adequacy of the content; and expressly disclaims liability for errors and omissions."
- Coverage: "Because the data readiness varies between Forests, each Forest will approve which level of attribute subset are published". "When fully realized, it will describe..." i.e. the layer is explicitly incomplete.
- Trail_MVUM use constraint (the sibling layer): "These geospatial data and related maps or graphics are not legal documents and are not intended to be used as such." Same layer: open dates describe legality, "not ... when the conditions would be appropriate for that use" (snow, mud).
- No trip-planning guidance for the date fields was found. Whether the agency intends them for trip decisions: UNKNOWN. Trail Fundamentals says the Forest Service "assumes no responsibility for the interpretation or use of this information by anyone except its own employees."

## 5. Bounded live sample (Pike-San Isabel area; one query, 8 records, retrieved 2026-10-08T22:12Z)

Query: trail_name containing RAMPART or DEVILS HEAD on the layer above, no geometry. Records are samples only, not a coverage statement and not verified against any MVUM.

| trail_name (no.) | motorcycle_managed | _accpt | _accpt_disc | _restricted | allowed_terra_use |
|---|---|---|---|---|---|
| DEVILS HEAD 60 (6660) | 05/15-10/31 | blank | 11/01-12/15 | blank | 4321 |
| RAMPARTS LOOP (166) | 05/01-11/30 | blank | blank | 12/01-04/30 | 4321 |
| DEVILS HEAD SPUR (0679.A) | blank | 12/01-03/14 | 12/01-03/14 | blank | 54321 |
| RAMPART MTN. (643) | blank | blank | blank | 01/01-12/31 | 21 |
| RAMPART RESERVOIR (700) | blank | blank | blank | 01/01-12/31 | 321 |
| DEVILS HEAD (611) | blank | blank | blank | 01/01-12/31 | 21 |

Reading: on the two records with a managed season (summer, through 11/30 or 10/31), the managed range is the summer and the accepted/discouraged or restricted range is the complementary off-season, which fits the definitions in Section 1. Ramparts Loop shows a restriction range (12/01-04/30) as the complement of its managed season, so RESTRICTED does carry partial-year ranges despite the "year-round" wording. Devils Head Spur (0679.A) has ACCPT 12/01-03/14 and no managed field: a winter-only window with no summer statement at all. For that segment the layer is silent for the rest of the year (UNKNOWN), and ALLOWED_TERRA_USE includes 4 (motorcycle) with no dates. I did not find a Rampart Range record in this sample whose summer dates are covered by a field; the user's observation (many motorcycle segments with only "12/01-03/14" ACCPT) is consistent with the Devils Head Spur row but was not counted across the forest.
Segments with only an ACCPT_DISC and ACCPT identical: ACCPT_DISC appears to be a union that duplicates ACCPT here.

## 6. Recommendations for Claude (research input, not a decision)

1. Do not display "outside published use dates" from ACCPT alone. Treat MANAGED, ACCPT, DISC and ACCPT_DISC as management-intent strings; show them verbatim with their publisher labels.
2. If a use-date check is kept, treat only RESTRICTED as a restriction and only when the trip date is inside it; treat any other date as UNKNOWN, not "not allowed" and not "allowed".
3. Keep ALLOWED_TERRA_USE ("legally allowed") as a separate undated field; the app already stores it.
4. For motorized legality, evaluate S_USA.Trail_MVUM (EDW_MVUM_01) date-open fields and link the forest's MVUM, labelled "not a legal document". Whether that layer is licensed and fit for the app's pipeline is a separate review.
5. Re-read: FSM 7730, FSH 2309.18 sec. 14.3 and FSM 2353.19 (the handbook PDF URL returned a 404 page; not retrieved); and obtain the NRM ATM Data Dictionary (internal site, unreachable) for the definitive format and wrap rules. Contacting Pike-San Isabel NF or the EDW data-steward address (SM.FS.data@usda.gov) with the clarifying questions below is an owner decision; no contact was made.

Proposed clarification questions: (a) For TrailNFS_Mgmt, is a date outside every range unrestricted, unknown, or unavailable? (b) Is an end date earlier than the start date a year-end wrap? (c) How do ACCPT_DISC and the separate ACCPT/DISC fields relate? (d) Is RESTRICTED a prohibition, and is it consistent with MVUM seasonal closures?

## Sources and retrieval

1. EDW FGDC metadata S_USA.TrailNFS_Publish, USDA Forest Service Enterprise Data Warehouse, https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml, 2026-10-08T22:11Z. Primary, decisive.
2. ArcGIS REST layer EDW_TrailNFSPublishWithDataStatus_01/MapServer/0 (layer JSON description and a query), USDA Forest Service, 2026-10-08T22:11Z and 22:12Z. Primary.
3. Trail Fundamentals and Trail Management Objectives (MTDC 1623-3801, 2016), USDA Forest Service, 2026-10-08T22:13Z. Primary, guidance.
4. EDW FGDC metadata S_USA.Trail_MVUM, USDA Forest Service, 2026-10-08T22:12Z. Primary, sibling layer.
5. FSM 7730 PDF (usda.gov) and Gifford Pinchot NF MVUM page: search snippets only, not fully retrieved.
6. Failed: FSH 2309.18 PDF (stelprdb5403600.pdf) returned a 404 HTML page, so FSH 2309.18 text was taken only via Trail Fundamentals.
