# Deep Value agent focus and repair loops

Audit date: October 6, 2026. This further review examines whether agents preserved their assigned goals, whether repair/protocol work displaced the next useful investment step, and whether readiness claims matched functional acceptance. I distinguish manager work from a Helper's bounded engineering commission. I do not retroactively assign any task an original model-bias evaluation goal: the visible prompts do not contain one.

In the delegated read-only review, only this note and its supported metadata census were authored. There were no broker calls, private Codex-file inspections, runtime/schedule changes, task messages, source changes, or GitHub mutations.

## Supported census and its visibility limit

Every available parent cursor was exhausted through `read_thread`:

| Exact returned parent title | ID | Turns/pages | Activity-linked agent IDs |
|---|---|---:|---:|
| Deep Value Manager GPT-5.6 Sol | `019fa313-aa1b-7cb2-b13d-c1aaba9f5cc6` | 311/32 | 417 |
| Deep Value Stack Helper GPT-5.6 Sol | `01a00d1d-2058-7d30-a638-613879058b99` | 111/12 | 0 exposed |
| Deep Value Contrarian manager | `019f8f66-dc16-7a53-a2ec-0cbac247a5bd` | 13/2 | 36 |

Total: **435 parent turns, 46 pages, 1,205 subagent activity records, 453 distinct linked IDs**. Activity records comprise 435 started, 203 completed, 511 interacted, and 56 interrupted events. They are events, not accepted deliverables. The 453 paths include 435 `/root/name` agents, 16 second-level and two third-level descendants already exposed in the parent history.

I directly requested every one of the 453 linked histories. All returned **one metadata page, null title, zero turns, `hasMore:false`**, with no errors. An `includeOutputs:true` spot-check remained empty. No further child IDs were exposed. Thus every exposed ID was traversed, including the 18 nested paths, but the reader does not establish full recursion into unexposed descendants.

The parent activity schema supplies a kind, call ID, agent path, and agent thread ID; it does not supply the original delegation prompt or child's return. Some child previews reproduce a parent request. I did not mistake those previews for child assignments. Consequently **actual child prompt–outcome pairs and child functional acceptance are unavailable**, not reviewed and found successful. This is an important limit on an “all agents” claim.

The machine-readable [census](../evidence/agent-census-20261006.json) records every ID, path, containing parent IDs, empty read state, page/turn/error counts, and path depth. Containing parent IDs are provenance of the returned activity, not an assertion of the immediate spawning ancestor. No raw transcript, preview, account identifier, or private path is included.

The parent-visible evidence runs July 23–September 7, 2026, with the Helper's last visible turn starting September 4 at 20:55:34 UTC. The parent histories were freshly paged on October 6 to discover the newly exposed agent metadata. The ten-turn reader maximum prevented larger pages. Returned `notLoaded` status is an app loading state. Current manager/helper histories are assigned to other reviewers.

## Actual goals, parent-visible outcomes, and acceptance

The replacement Manager's initial prompt explicitly says:

> Operate the independent Deep Value manager: discover, underwrite, rank, enter, manage, reduce, replace, and close manager-owned contrarian investments

It grants independent investment/lifecycle judgment while assigning runtime software to the Stack Owner. The Helper's initial prompt is persistent bounded engineering and says:

> Coordinate with the Deep Value Portfolio Manager as functional reviewer; do not make that manager supervise engineering.

Zero-order engineering tests can fulfill that Helper goal. They cannot establish investment success. The following pairs are **actual parent-level requests and visible parent responses**, not invented direct child assignments.

### 1. Broadening research was adopted, then a checkpoint became a premature stopping rule

On August 11, the principal asked the Manager to broaden discovery, maintain 15–20 candidates/five completed underwrites, and model disclosure uncertainty conservatively. Manager turn `019ff19d-17c9-7a31-a4a3-17b66dea0c61`, 16:17:12 UTC, admitted:

> The existing workflow has been too concentrated in a small mature watchlist and too dependent on binary price ceilings.

It adopted scenarios in which missing information reduces value/confidence instead of automatically blocking investment when downside can be bounded.

The September 2 request was direct: “Why didn't you complete NMIH and VNT but concluded to wait?” In turn `01a062b0-4548-71f1-a8a4-3e3e9ecee33f`, 15:15:14 UTC, the Manager answered:

> I treated the 11:00 checkpoint as a stopping boundary after finishing DECK, even though research capacity remained. That was a workflow mistake—not an economic reason to wait.

Activity metadata links `nmih_primary`, `nmih_valuation`, and `nmih_skeptic` to IDs `01a062b0-80e4-7691-b302-8273a09ae626`, `01a062b0-911b-7221-82cd-5ebe81a5fdce`, and `01a062b0-a264-7621-94a1-b9b484aa36e3`. Their direct histories are empty; the parent's visible commentary says six lanes were working and later completed both underwrites.

The parent then reported NMIH 5.18% and VNT 13.58% expected after-cost CAGR, exact entry bands, and `ECONOMIC_NO_TRADE`. Completing the work is observed through the parent. The earlier stopping was a goal substitution; the later valuation rejection is a separate economic judgment.

### 2. A narrow structural-entry repair expanded into a long acceptance cycle

The July 31 principal request was to fix the runtime for the approved 0.50% lane rather than raise its cap to USD1,000. Manager turn `019fb8f7-3003-7952-81a0-1a68e707c210`, 16:17:15 UTC, contains **18 started agents** for schema, authority, ledger, test, publication, cutover, rollback, and acceptance reviews, and ended failed after approximately 8 hours 13 minutes.

The visible review found genuine defects: caller-mintable authority, missing cumulative caps, missing lineage, and replay/terminal-state errors. Those checks were economically relevant and should not be bypassed. However, intermediate “checkpoint complete” and hundreds of passing tests repeatedly preceded further repair and commissioning work. The observation is expensive goal-conversion friction, not proof that the review agents intentionally chose HOLD. Their original prompts and individual returns remain unavailable.

The Manager's stance was explicit:

> Checkpoint 1 is **not accepted for commissioning yet**.

That distinction was accurate. The practical criticism is that the project lacked a compact end-to-end acceptance contract proving the approved lane in its actual commissioned environment.

### 3. ACCEPT and broad tests did not reproduce production dependency conditions

Archived Helper turn `01a04114-b3f0-7093-bf5f-e7e29e9f6284` (August 27) commissioned a reporting candidate after Manager ACCEPT, 29/29 installed tests, and 1,241 broad tests. Actual installed production reporting failed because the sealed runtime lacked `pandas_market_calendars`; rollback preserved production. The visible Helper stated:

> No ad hoc installation was attempted.

An August 26 reporting attempt also failed on execution-contract generation mismatch despite prior acceptance. These are acceptance-matrix shortcomings: the tests did not prove the exact production-shaped dependency/lineage path. Correct rollback was necessary, but repeated repair of the proof environment consumed work that should have been resolved before publication.

### 4. An expanded commissioning predicate blocked an accepted feature

September 2 Helper turns `01a06294-9ea0-77a1-922b-b51227cb48ca` and `01a06295-9c7c-7500-8d58-607d67ac27ab` expose a clear specification problem. The accepted candidate supplied public `--new-search-seed` ingress; the commissioning checklist additionally demanded public `reqScanner`, which was not part of that candidate. The Helper requested:

> Correct the predicate to new-search-seed only, or Separate reqScanner into a future candidate cycle.

Commissioning proceeded after that correction. The block came from an enlarged verification requirement, not a failure of the accepted requested feature. This is a concrete protocol-complexity gate.

### 5. Proof-harness failures prolonged an unchanged reporting repair

September 3–5 Helper turns `01a063e0-2a13-79f1-b31b-6691be057f77`, `01a06e29-8a32-7d72-9cad-e353eef4b420`, and `01a06e34-9397-7df0-8e9f-bbdde6fd06e3` record omitted-`pytest`, an invalid pre-authority `closing` assumption, and a future timestamp causing repeated proof/rollback work.

The final explanation was precise:

> The one selected proof used an `as_of` a few seconds ahead of the host clock and failed before candidate behavior.

The unchanged candidate subsequently passed corrected commissioning. Those failures must be attributed to the harness/protocol, rather than inflated into new evidence against the candidate or investment action.

## Readiness claims, code semantics, and my own review discipline

“No concrete Deep functional blocker remains” in the August 18 Helper handoff was immediately qualified by the candidate remaining non-selected. Likewise August 31's “Trading readiness has no remaining Stack defect or commissioning work” separated installed execution readiness from uninvoked optional research ingress. I should preserve those qualifications instead of treating every assurance as false—or treating it as proof of completed investment work.

The October 5 named-file review found a related interface problem in selected commit `bca363741018413d0562769885fb60334bcd0b3b`. In selected-relative `src/deep_value_manager/attention_registry.py:1716–1722`:

```python
for clock_name, clock in clocks.items():
    if clock["status"] != "CURRENT":
        missing.append(f"{clock_name.upper()}_CLOCK_STALE")
if not bands["complete"]:
    missing.append("DECISION_BANDS_STALE")
source_complete = not missing
fully_underwritten = source_complete
```

Full-file SHA-256: `7973300dac9a5e58cc231d84832eb05dbf030bd2945a720d4ab1e3147c0e0c8f`. Line 1970 uses `source_complete` to choose a replacement. Quote-only expiry therefore excludes completed research from that comparison, while durable `FULL_UNDERWRITE_RECORDED`, primary-source, survival, and scenario evidence remain preserved. That classification/selection conflation is distinct from the legitimate need for a fresh execution quote.

My review must resist equating procedural activity with goal progress. Agent counts, passing tests, signed receipts, and repeated “complete” checkpoints measure different things. For each repair, I should identify the originally requested behavior, the smallest reproducible failure, the production-shaped acceptance, and the resumed manager decision. I must also resist calling every zero-order Helper outcome investment abstention or assigning unobserved intentions to 453 empty histories.

The strongest demonstrated failures are premature research stopping, acceptance that omitted actual runtime conditions, and commissioning predicates/harnesses that created additional loops. The remedy is explicit goal retention and bounded acceptance, with the manager's adopted economics kept separate from transport state. This audit does not establish whether the eventual valuations were profitable or reveal unreturned child cognition.

Published coverage: [combined agent census](../evidence/agent-census-20261006.json). Evidence task IDs and turn IDs identify supported-history excerpts; project source paths identify the original private workspace, not files copied into this reporting repository.
