# Optional local Qwen evidence advisory tooling

Step 1 packages the optional adapter for offline review. No inference is
authorized here. The recovered adapter and test were imported with only their
private endpoint literal replaced by a neutral placeholder, under the explicit
coordinator decision. A separate change replaces that placeholder with a strictly
validated installation setting. Originals remain private; import and fixture
hashes and deviations are documented in the contract.

This tool is optional and reads explicitly selected public evidence. It never
publishes canonical evidence or supplies permission, factual verification,
review, architecture decisions or implementation authority. Its output always
carries `AI-assisted advisory — structurally validated, factually unverified`.

Run the local integration check from the repository root:

```sh
python3 -B tools/local-ai/qwen/offline_tests.py
```

This launcher blocks the reviewed network/process entry points before test discovery,
including native socket/fork entry points, multiprocessing start and new ctypes
library loads or `system` symbol resolution. It is not a security sandbox: cached
native function pointers, other native extensions and unreviewed entry points
are not blocked. The synthetic fixtures are byte-identical; the adapter/test changes are documented.
No dependencies are added. The CI change adds only this offline check to the
existing Python job. A failure of the optional tool's offline tests fails that
shared job for every pull request; remove the single step to disable that CI
dependency.

`prepare_advisory_input` accepts a list of selected records with exactly the
required keys `id`, `source_ids`, `access_status`, `camping_permission`, plus
the recovered optional descriptive/evidence fields. It copies IDs losslessly.
It rejects `restricted` access as unrepresentable. It accepts positive values
only as an explicit projection of already contract-checked canonical input;
it does not validate the evidence needed to publish such values. There is no
output conversion to the canonical schema. Do not pass whole canonical objects
or private evidence. The 3,072-byte guard is not a tokenizer measurement.

The single installation setting is `~/.config/ohvernight/qwen-endpoint`, outside
Git, containing the complete endpoint URL and optionally one trailing newline.
Tooling never creates this setting automatically. Configure it only under explicit
owner authorization, with owner-only permissions. The setting is fixed
per installation: no environment, CLI or runner endpoint override is exposed.
It requires the original HTTP scheme, a literal loopback or Tailscale CGNAT
address, TCP port 11434 and path `/api/chat`, without credentials, query or
fragment. Hostnames, public addresses and ordinary private LAN ranges fail.
Both setting files must be regular, non-symlink files owned by the current uid
with no group or other write permission. The opened file descriptor is checked
again; symlink following is refused. Unsafe endpoint files fail with
`ENDPOINT_SETTING_UNSAFE`; unsafe acknowledgements fail with
`EXPOSURE_REVIEW_UNSAFE_SETTING`. Missing/unreadable/invalid/in-repository settings fail before any terminal or
network request. The runner records only a non-secret endpoint label and does
not pass the URL in its command or environment. Redirects/proxies remain refused;
model `qwen3:8b` and its original parameters remain fixed. Deep JSON nesting
emits `rejected` with `JSON_RECURSION_LIMIT`; unexpected ordinary exceptions
emit `failed` with `UNEXPECTED_ADAPTER_ERROR`. Control-flow exceptions remain
unhandled for caller interruption. Missing account-database entries become
OSError and follow the CLI failure-event path.

The service has no API authentication, and its listener was last observed on a
wildcard interface. Live use remains gated on the owner's network exposure
review; permitted URL syntax does not establish isolation. Both the runner and standalone adapter CLI require
the owner to set a separate outside-Git file,
`~/.config/ohvernight/qwen-exposure-review.json`, after that review:

```json
{"owner_exposure_review_acknowledged": true, "reviewed_at": "YYYY-MM-DD"}
```

Replace the date placeholder with the actual review date. Missing, unreadable,
malformed, undated or inside-repository acknowledgements fail with
`EXPOSURE_REVIEW_REQUIRED` before launch; the CLI emits a rejected event before
reading the endpoint or constructing a request. Future dates fail. Agents must
never create the acknowledgement: only the owner does. No maximum age policy
is implemented; a 30-day maximum is proposed for owner approval, including an
invalidation rule for network configuration changes. Offline tests use synthetic files or mocked acknowledgements and need
no real owner setting. Acknowledgement does not authorize inference or Step 2.

`run_advisory` takes the resulting bytes and an injected execution interface.
There is no enabled concrete Orca execution backend in this draft. The standalone
adapter CLI is an executable live-inference entry point, independently gated on
the same owner acknowledgement and endpoint validation. It does not provide the
runner's byte guard, completion consumption or cleanup confirmation. A separately approved pilot must provide an inspected interface
using `orca terminal create --command`, exact-handle completion reads, and
independent confirmation of terminal closure and adapter-process exit. A create
receipt alone is insufficient. No retry, fallback or model switching is allowed.
The command builder clears the child environment and selects isolated Python
with bytecode disabled. Parent and child both resolve the POSIX account home
via `pwd.getpwuid(os.getuid()).pw_dir`, ignoring HOME. The POSIX main-thread runner additionally enforces a 150-second default deadline
and a separate five-second cleanup grace. A competing timer or non-main thread
is rejected; cleanup still runs without a timer in that case. This fallback
has no runner-enforced cleanup deadline, so the interface must bound its own
cleanup. Timer teardown blocks expirations while restoring the previous handler
and drains a pending expiration before restoring the signal mask. A missing completion, cleanup or
correlation fails. Unexpected completion keys are rejected. Output words are
nested under `adapter_vocabulary`, which is not a canonical Ohvernight status.

Default run storage is the user's cache, outside the repository. An explicit
`run_root` can select another outside-repository directory. Input and metadata
files have owner-only permissions (new root 0700, input and metadata created atomically with O_EXCL, 0600),
and metadata uses a fixed allowlist; raw
advisory output is returned to the caller without being written. Do not retain
credentials, environment files, private configurations or unrelated user data.
The proposed pilot default is 30-day local retention for raw prompt/result
artifacts. No recurring deletion automation is created. Metadata starts with
review disposition `unreviewed`; token count is null until exact offline Qwen
tokenization is available. The caller is responsible for public-input selection. Failures before directory
creation still return metadata, but write no runtime file. Broad pre-existing
roots fail rather than being chmodded.

Disable by skipping this optional advisory step. No production path imports it.
Rollback is removal of this directory, the single optional CI step, the contract
document, AGENTS.md verification command and its ignore entry. Normal builds, source retrieval and publication
continue to use the existing workflow. See
[the contract](../../../docs/agent-stack/qwen-research-adapter.md).
