# M3 performance baseline

Evidence for the architecture decision and the acceptance thresholds in
[../M3-unified-mobile-explore.md](../M3-unified-mobile-explore.md), section 16.

- `baseline.json` — raw results, measured on 2026-10-04 at `main` commit
  `3dc0fef` with headless Chrome 154 on macOS.
- `measure.mjs` — the script that produced them. Node 22 or later and a local
  Chrome; no npm dependency.

## Reproduce

From the repository root, at the commit being measured:

```sh
python3 -m http.server 8765 --bind 127.0.0.1 &
node docs/specs/M3-baseline/measure.mjs > /tmp/ohvernight-baseline.json
```

Set `CHROME=/path/to/chrome` if Chrome is not in a standard location, and
`BASE=http://host:port` to measure another server.

## Limits

- The local server sends no compression and adds no network delay, so byte
  counts are uncompressed and timings are parse-and-build time.
- `cpuThrottle: 4` is Chrome's CPU throttle, a rough stand-in for a mid-range
  phone. No real device was measured.
- Timings vary between machines and runs. Compare runs made on the same
  machine; do not gate CI on them.
- Basemap tiles are requested from USGS and Esri/OpenStreetMap by the current
  pages; they are excluded from the same-origin byte counts.
- The script targets the page structure at `3dc0fef`. It is a record of the
  baseline, not the M3 browser check, which is specified separately.
