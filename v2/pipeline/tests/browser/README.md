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

Chrome startup polls the local DevTools endpoint for up to 60 seconds, with
bounded requests and immediate failure if Chrome exits. Startup failures report
the endpoint, elapsed time, attempts, last error/status, Chrome executable and
version, and process exit status. Every run closes the DevTools connection,
reaps Chrome (with a bounded SIGTERM grace period before SIGKILL), closes the
server connections, and removes its temporary profile.

Importing `run.mjs` does not start the harness. Its exported `waitFor` helper
accepts deadline, retry interval, request timeout, and process-state overrides
for the offline `browser-harness.test.cjs` tests included in the standard Node
test suite. Page assertions and their timing behavior are unchanged.

DevTools commands have a 20-second bound (including connection readiness).
A closed or failed connection rejects pending commands with their method names
and rejects later commands immediately. Page inspection stops on a connection
drop or Chrome exit, reporting Chrome's exit code/signal when it exits, then
runs the same cleanup. Offline tests exercise dropped connections, unanswered
commands, and handshake failure using a minimal local WebSocket endpoint.
