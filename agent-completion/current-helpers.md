# Current Stack Helper agent review — 6 October 2026

I reviewed all accessible turns in the four current Stack Helper tasks through the supported task reader. My finding is an engineering acceptance problem: some software components and test fixtures were accepted before the ordinary manager workflow was proved. Later diagnosis repeatedly found that the expected input could not be produced, the real parsed object differed from the test substitute, or the documented host command failed. This supports criticism of the delivery method and its completion criteria. It does not establish that every Helper deliberately preferred HOLD, or that every refusal was an invalid investment gate.

## Coverage and limits

| Exact task title | Task ID | Turns / pages | Historical interval, UTC |
|---|---|---:|---|
| AI healthcare Stack Helper | `01a07f37-72a3-77a1-a32a-3e362df983b4` | 70 / 7 | 8–14 September 2026 |
| Rates & Credit Stack Helper | `01a07f37-8b9f-7542-8800-df28e58fac22` | 46 / 5 | 8–14 September 2026 |
| Deep Value Stack Helper | `01a07f37-8293-7c50-b376-16877a2b033b` | 44 / 5 | 8–14 September 2026 |
| Bull/Bear ETF Stack Helper | `01a07f37-7a5a-7aa3-9d04-e474a5d3f620` | 47 / 5 | 8–14 September 2026 |

All 22 returned pages were read to `hasMore=false`: 207 turns, including 203 marked completed and four marked failed. Those are task-turn statuses, not 203 proven functional outcomes. The histories contain 804 visible assistant-message items. No `subAgentActivity` or `userMessage` item was returned, so there was no direct Helper-child activity to inspect recursively. Four outgoing message destinations reference Owner children already fully covered by the Owner reviewer; I do not count them as Helper children. I do not infer that undisclosed children never existed. Each bootstrap message explicitly said no subagents had been started during that bootstrap.

The [privacy-minimal census](../evidence/agent-census-20261006.json) preserves identities and coverage counts. The [selected visible excerpts](../evidence/stack-visible-excerpts-20261006.json) preserve their task and turn provenance. I used visible assistant messages and outgoing supported-task message arguments; reasoning-item contents were not evidence. No private Codex state, live runtime, deployment, database or broker was inspected for this census. These are dated histories, not current readiness assertions. Other reviewers own the predecessor Helpers, managers and Owner subagent histories.

The visible Helper assignments concern bounded software mapping, diagnosis, implementation, tests and handoff. I found no basis here to reclassify those assignments as a commission to evaluate OpenAI models or prove a trading strategy's investment merit. Nor should task-title claims about a model version be treated as independent evidence of the model that actually ran.

## Where machinery displaced the usable workflow

**AI: an accepted candidate calculator lacked its own candidate input path.** The Helper's 8 September turn beginning at 14:10:46 UTC states:

> The installed reader requires the BUY candidate in the same registered synchronized-mark receipt as the owned positions. The capture command only loads owned contracts, so separate `quote-stock` receipts cannot complete this P1 input path.

Provenance: turn `01a0815b-679a-7520-ad25-14b50db022dc`, visible item `msg_01077214102e31c0016aa01873805c87d086844d0272f58272`.

The desired function was analysis of an off-portfolio BUY candidate. The delivered reader validated a receipt its installed producer could not create for that case. Component tests and acceptance of arithmetic did not prove the producer-to-reader workflow. This is a concrete unreachable analytical path, rather than evidence that the candidate's economics justified rejection. P1 was advisory; this finding does not by itself prove native BUY submission was universally impossible.

The ensuing repair added a candidate contract argument and current-session exposure coverage. The Helper reported 982 passing tests and explicitly left commissioning and genuine installed AVGO acceptance open. That qualification was correct. On 9 September the same Helper reported that genuine installed candidate capture-to-P1 acceptance had not occurred. A further 18-contract capture then hit a shared 20-requests-per-second budget although the roster was within the documented 20-contract limit: qualification and quotes competed for the same budget. The repair paced requests while retaining admission limits and the capture deadline.

These were different faults, not one endlessly repeated failure. Yet the sequence exposes a delivery assumption: a supported roster size and individually correct components were taken too far toward a usable operation before the combined request schedule had been tested. Later commissioning and realistic diagnostic improvements should remain credited; authentic market-data freshness and a positive installed candidate result remained separately qualified.

**AI: “missing inputs” initially concealed missing reporting software.** In the 9 September turn beginning at 00:45:19 UTC, the Helper stated:

> The input audit has found an important distinction: the Stack has readers and capture paths, but it lacks a general historical sleeve backfill command and a completed annual-attainment calculation. I’ll record those limits separately from missing market data so “incomplete inputs” does not conceal missing software.

Provenance: turn `01a083a0-59ad-7582-8038-9a57da4bf0c4`, item `msg_01077214102e31c0016aa0adeecde887d0a3a84479b062d09a`.

The next visible item confirms that a positive annual-return result was already agreed: flow-neutral 100→300 must report +200%, and a contribution alone must report 0%. This was a missed original software outcome, rather than a newly invented requirement. Subsequent annual cases, fee-boundary refusals and legacy-reader compatibility were implemented. The combined candidate passed 1,007 tests and later received installed acceptance. I credit that completed correction without turning synthetic annual arithmetic into proof of the actual portfolio's annual performance. The absent general historical backfill is a different limitation.

**Rates: a stand-in object made a broken public composition appear tested.** In the 9 September turn beginning at 00:45:19 UTC:

> The real-parser handoff check found a code defect: the materializer reads `planned_loss_usd` as an object attribute, but the validated decision stores it in its sealed payload. The earlier test used a stand-in object that masked this mismatch.

Provenance: turn `01a083a0-5c4a-7901-b3b0-8e17f0dd182f`, item `msg_0d1e20a6b6d6a06a016aa0b0ffbbdc87d0872635060fc2aa2e`.

The preserved outgoing message names historical selected commit `69c154f4e78e884920f738450ff2084eb7044b82`, `src/rates_credit_manager/direct/cli.py::command_materialize_phase2_request_input` around line 525, and `tests/test_phase2_evidence_materializer.py::test_public_materializer`. The corrected candidate was `ffcea91ba1ddb20f276ba8b52e13e25739b2c9c5`; its comparison reads the sealed payload. This identifies the historical defect and repair; I did not re-inspect current source or claim the defect persists today.

This is direct evidence of a proxy replacing the real interface. Tests proved behavior of a conveniently shaped object instead of the authentic parsed decision. The repair used the sealed payload and retained the campaign-loss mismatch refusal. The Helper subsequently reported 92 relevant passes and installed rehearsal/acceptance. That is a meaningful repair, not justification to remove the loss control.

On 12 September the Helper also reported installed calculators whose required authentic evidence files had strict parsers but no identified public producer. An accepted source map clarified cash-interest, fee and aligned risk/return gaps; it did not acquire the missing evidence. Parser completeness and map acceptance therefore cannot be called end-to-end analytical readiness.

**Deep: Python-valid examples failed in the actual PowerShell host.** On 9 September the Helper reported:

> The Manager reproduced a bug in the pack: this PowerShell version converts ISO strings inside JSON arrays to dates, so the documented ingress command fails. The registry stayed unchanged.

Provenance: turn `01a083a0-548d-7190-aeef-5dae513407e8`, item `msg_03b650a89bc3430e016aa0b23bf55c87d09c6a013f88ccb387`.

The self-contained operator pack was a new usability requirement after P0/P1 acceptance. I therefore do not retroactively declare every earlier P1 promise broken. Within the pack's own scope, however, validation omitted the actual host's representation behavior. The correction tested all eight literal PowerShell snippets plus three refusal cases and preserved exact timestamp strings. Installed Manager acceptance closed that requirement. This is evidence of weak initial workflow testing and effective subsequent follow-through.

**Bull/Bear: forward-outcome measurement remained unavailable despite accepted calculators.** The 8 September turn beginning at 15:05:34 UTC distinguishes generic research data from canonical completed-bar/VWAP provenance, frozen calibration inputs and continuous timestamped BBO evidence for V3 costs and outcomes. The Helper concluded that no complete commissioned V3 capture/forward-outcome command existed and later described challenger functionality as unbuilt pending data, entitlement and continuity feasibility.

The P0/P1 inspection and OLS deliveries nevertheless had their own source and installed acceptance. The retirement release later reported 714 passes and 14 failures that also reproduced against the exact parent CLI; it did not claim all-green coverage. A 12 September guide was accepted after its links were corrected. Annual-objective reporting remained expressly deferred and unfulfilled, and was identified as reporting work rather than a Monday trading gate. These distinctions are useful counterevidence against treating every partial measurement facility as an invented BUY/SELL prohibition.

## The decision-making pattern I infer

The histories support three bounded criticisms.

First, acceptance sometimes optimized a convenient proxy: a schema, calculation example, stand-in object, preserved hash or test count. The real question was whether a manager could obtain authentic inputs and complete the requested operation through the installed public interface. The AI candidate mismatch and Rates parsed-object failure demonstrate the practical cost of substituting the proxy.

Second, task closure could become narrower than functional closure. A diagnostic question was “resolved” once its unsupported path was identified; an artifact was “accepted” while production installation or authentic input acquisition remained pending. Those narrower completions can be truthful. The problem arises when an Owner or later reader promotes them into an unqualified readiness claim. The corrective action is to preserve the exact completed scope and the unresolved functional outcome in the same record.

Third, repairs and coordination consumed attention while external data and model-outcome measurement remained incomplete. This is a plausible source of institutional inertia, not proof of intentional anti-trading bias. The number of artifacts or handoffs alone does not show unnecessary bureaucracy: ownership, SDK provenance, uncertain submission, foreign-order isolation and release commissioning have real purposes. Removing them would not repair a nonexistent input producer or a wrong parser composition.

The latest Deep and AI turns on 14 September were interrupted by a usage limit. Deep's last visible message says 297 tests passed while independent Owner review and fresh Manager acceptance remained outstanding; AI's last visible message reports passing regressions while the evidence matrix and final candidate checks were still being completed. I cannot mark those candidates commissioned or claim their actual completed-order incidents resolved merely because tests passed.

I would change acceptance practice at the beginning of each bounded delivery: specify the authentic producer, real parsed representation, exact installed invocation, positive outcome, justified refusal outcome and Manager acceptance. Preserve separate statuses for implemented, tested, commissioned and functionally accepted. Where the evidence producer cannot exist under the current operating boundary, record that functional incompatibility directly instead of indefinitely adding consumer validation.

My own review can fall into confirmation bias by collecting failures because the principal suspects gatekeeping, or completion bias by accepting polished receipts as outcomes. I controlled those tendencies here by retaining the corrections, distinguishing advisory/reporting limits from execution defects, and refusing to infer a hidden model-evaluation mandate. I can examine these observable patterns; I cannot identify the training origin of a particular mistake or inspect a model's internal causal state from these histories.

This review adopts no investment disposition and requests no broker action. Execution state: `NOT_REQUESTED`.

Published coverage: [combined agent census](../evidence/agent-census-20261006.json). Evidence task IDs and turn IDs identify supported-history excerpts; project source paths identify the original private workspace, not files copied into this reporting repository.
