# MVUM sample fixture

`mvum-sample.json` contains seven records selected from the saved Package 4 public REST samples. The records are trimmed to source layer, identifiers, route label/name, symbol, and the motorcycle designation/date fields; geometry and unrelated attributes were dropped. No record was newly fetched for this prototype.

The source layers are Forest Service EDW `EDW_MVUM_01/MapServer/1` (roads) and `EDW_MVUM_01/MapServer/2` (trails). The saved response files are dated 2026-10-08 by their filesystem modification time; the REST payloads did not include an exact retrieval timestamp, so this fixture records the date only. The saved bounded responses and layer descriptions remain in the separate untracked Package 4 research directory.

The seven non-empty `motorcycle_datesopen` strings cover every distinct date-range value observed across both saved MVUM sample responses, including year-wrap and two comma-separated windows. The fixture is small test evidence, not a representative production dataset or a claim that the records join to current trail features.
