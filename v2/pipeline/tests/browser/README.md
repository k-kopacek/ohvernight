# PR A browser smoke check

`run.mjs` uses only Node's built-in HTTP and WebSocket APIs plus a local Chrome
DevTools Protocol connection. It starts its own local static server, blocks
every non-local request, loads both existing v2 pages, and fails on uncaught
errors, failed same-origin requests, horizontal overflow, or the removed
legacy download link.

Run from the repository root:

```sh
node v2/pipeline/tests/browser/run.mjs
```

Set `CHROME=/path/to/chrome` when Chrome is not in a standard location. The
check is intentionally limited to the two existing pages; the unified Explore
shell is PR B work.
