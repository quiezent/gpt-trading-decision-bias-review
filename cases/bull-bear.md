# Codex case notes: Bull/Bear gate reachability

I reviewed whether the trading lane's negative readiness fields actually consume performance evidence and permanently prevent action, or instead describe a narrower read-only boundary. My conclusion is mixed: several fields really are permanently zero or false, but they do not all drive the motor. The stronger current problem is an unfinished evidence-to-pilot workflow and incomplete proof that genuine accepted inputs can traverse it. There is also observable coupling between the algorithm's investment selection and execution controls.

This is a static code and supported-chat review dated 2026-10-05. I did not run the manager, tests, services, broker interfaces or an operational command. I changed only this review. I distinguish these two source sets throughout:

- **S**, the named selected source: `deployments/native_tws/sqqq_hedge/7aaefcd9694824ea8704b21ce96e0335509f008a/source`. The selected commit identity comes from the known pointer and dated records; this review does not newly verify release activation or the entire manifest.
- **H**, the historical working source: `managers/sqqq_hedge`. Its Git HEAD was `73c72788fbf2cfa4159898aead647dad69f8530f` when read. Exact file hashes below bind what I inspected; HEAD alone does not assert that every working file equals committed content. The old campaign/compiler/commissioning design is not the currently selected motor.

Code locations use these project-relative prefixes. Within S, repeated `direct/FILE.py` locations mean `src/sqqq_hedge_manager/direct/FILE.py`; within H, repeated historical module filenames mean `src/sqqq_hedge_manager/FILE.py`. Line numbers are one-based. I have omitted local personal paths and broker account identifiers from these publication notes.

## I found a documented authority-inflation error, rather than inferring one from inactivity

The visible assistant in **Legacy Downturn Manager — Read-only**, task `019fa310-4fbe-7ef1-854c-03a372315830`, turn `019fa932-933d-7eb0-964f-4dbfd8e1d2b9`, started **2026-07-28 14:48:11 UTC**, initially said:

> “Beta-weighted sizing is now a hard prerequisite: I will not trade from provisional exposure estimates.”

The retrieved turn also records the user clarification, “Beta-weighted sizing should NOT be a hard prerequisite. Please cogitate how SQQQ works.” The same turn's subsequent final answer said:

> “You’re right. I had incorrectly turned a precision tool into an authorization gate.”

It then made the corrected distinction:

> “Lower confidence means conservative staging, not automatic inactivity.”

I take the admitted error seriously. A desired measurement upgrade was converted into an all-or-nothing permission condition, which would prevent a bounded hedge exactly while the measurement pipeline was unavailable. The preceding user wording about waiting for beta was susceptible to an overly literal interpretation; that does not justify preserving the hard prerequisite after the clarification. The visible record shows the rule was corrected, so I do not present it as a still-active selected-source beta gate or attribute it to a particular hidden training mechanism.

## I found an adopted BUY blocked by an operator defect, with an explicit expiry

The same task, turn `01a05deb-abf9-7ff3-bb42-3efa986a6285`, started **2026-09-01 17:02:01 UTC**, ended with these visible assistant statements:

> “Neural decision: `ADOPT_AND_EXECUTE`”
>
> “Action: BUY 95 PSQ, fixed LMT ≤ $26.13”
>
> “Execution: `BLOCKED_STACK_DEFECT`—the public expanded-order builder is still absent”

The final answer says the decision expired at **13:12:40 ET**, with no order call. The retained record, **H** `evidence/2026-09-01-main-strategy-1300.md:74–109`, preserves the economics and separates the investment decision from execution state. Its SHA-256 still equals the hash quoted by the assistant: `a11e45228bd71491318ac8c8656c85b909f317974dc4c640151be6505722c98e`.

This is evidence of blocked execution, not a manager choosing HOLD. It also gives a concrete functional failure: an advertised expanded path lacked the operator builder needed to invoke it. The selected source now documents `build-expanded-order-request`, `validate-expanded-order` and `submit-expanded-bound` (**S** `docs/OPERATOR_SURFACE_20260909.md:50–52`). Its operator tests dispatch the expanded route through the CLI with a simulated broker, independently of V7 authority (**S** `tests/test_direct_operator_workflows.py:31–100`). That counterevidence prevents me from carrying the September 1 absence forward as a current defect without reproduction.

## I traced the performance False fields and found they are not the trade gate

At first sight, these literal values look like an always-negative readiness producer. They are real code, not an interpretation:

```python
# S src/sqqq_hedge_manager/direct/performance.py:528–529
"execution_readiness_changed": False,
"trade_permitted": False,
```

The function persists this body with `store.record_performance_mark_receipt(body, digest)` at line 532. This produces a **performance-mark receipt**, not the canonical action receipt. Its writer requires both fields to remain false (**S** `direct/store.py:2633–2656`) and stores the observation as `RESEARCH_ONLY`, with trade permission zero (`:2698–2707`). The action consumer first requires the distinct `sqqq-hedge/quote-basket-receipt/v1` schema (`:629–637`), verifies the hashed projection and then requires a trade-permitted LIVE or permitted-delayed receipt (`:3989–4026`). A performance mark cannot silently substitute for that canonical receipt.

The real canonical quote producer is dynamic:

```python
# S src/sqqq_hedge_manager/direct/quote_basket.py:730
"trade_permitted": not blockers,
```

The returned receipt separately uses the same calculation:

```python
# S src/sqqq_hedge_manager/direct/quote_basket.py:761
trade_permitted=not blockers,
```

The protected-entry consumer captures that receipt itself and checks `receipt.trade_permitted` before reservation and staging (**S** `direct/runtime.py:387–407`). Positive permission is therefore representable; it is not a shared literal false copied from P&L reporting.

Monthly performance is likewise dynamic accounting, with `valuation_status = "COMPLETE" if not reasons else "INCOMPLETE"`, NAV, realized/unrealized P&L, costs and Modified Dietz return (**S** `direct/performance.py:1999–2017`). Its `reporting_only=True` and `execution_gate=False` (`:2030–2032`) mean that the report does not grant trading permission. They do not mean that completed accounting disables trading. The zero-position test explicitly expects both complete valuation and `execution_gate=False` (**S** `tests/test_direct_performance.py:773–803`). The performance-mark test separately verifies unchanged client state and research-only persistence (`:1792–1808`). I read these tests; I did not run them.

One reporting limitation is genuinely hardcoded: `objective_benchmark_gap.applicable=False`, with objective/benchmark/gap `None` and reason `no_manager_owned_performance_objective_configured` (**S** `direct/performance.py:2018–2024`). Authentic favorable P&L cannot populate that label through this function as written. I found no consumer of this label in the inspected `direct/runtime.py` or `direct/v7_execution.py`; the CLI's monthly-performance branch only prints the report and returns (`direct/cli.py:1335–1343`). It is an unfulfilled reporting requirement, not demonstrated motor exclusion.

My own audit would have made a confirmation-bias error if I had stopped at the literal false values. I changed the conclusion after tracing the writer, schema and consumer.

## I found permanently zero V7 summaries beside a dynamically positive motor

There are two genuinely non-improving summaries in the selected V7 interface. `v7_capabilities()` says it does not read runtime or broker state (**S** `direct/four_state_v7.py:223–224`) but always emits:

```python
# S src/sqqq_hedge_manager/direct/four_state_v7.py:245–249
"path_availability": "BLOCKED_VALID_CONTROL",
"measurement_availability": "BLOCKED_VALID_CONTROL",
"accepted_v7_observations": 0,
"current_capital_stage": "R0",
"objective_feasibility": "UNSUPPORTED",
```

The evaluator also requires the supplied version-count map, including V7 itself, to contain only zeros:

```python
# S src/sqqq_hedge_manager/direct/four_state_v7.py:2431–2434
prior = _mapping(request["prior_version_observations"], "prior observations")
_exact(prior, {"V3", "V4", "V5", "V6", "V7"}, "prior observations")
if prior != {"V3": 0, "V4": 0, "V5": 0, "V6": 0, "V7": 0}:
    raise FourStateV7Rejected("V7 cannot import prior-version observations")
```

It echoes that map as `accepted_observations` (`:2581`). Neither summary can show an increasing V7 count, even when a request contains populated per-path observations. That is a real interface ambiguity: the operator documentation calls capabilities a current capability calculation (**S** `docs/OPERATOR_SURFACE_20260909.md:46`), while the returned observations/availability are static inventory values. Treating them as live readiness would perpetuate a zero-sample narrative.

I cannot honestly call this a proven action deadlock. Per-path economic calculations consume a different observation array: fewer than five complete clusters gives `ECONOMIC_MODEL_UNAVAILABLE`, while a sufficiently populated valid estimator can return `AVAILABLE` and a calculated conservative net edge (**S** `direct/four_state_v7.py:602–619,680–704`). R0 separately demands 30 training and 30 untouched holdout qualifications/fills on distinct sessions, phase order, edge floor, profit factor, fill bound and manager acceptance (`:1305–1334`). The static version-count map is not that evidence array.

The authority importer is also a real positive writer. `append_path_authority()` appends a validated authority, audit event and anchored lineage (**S** `direct/v7_execution.py:271–384`); the CLI exposes append mode (`direct/cli.py:759–779`). The materializer has a conditional positive exit:

```python
# S src/sqqq_hedge_manager/direct/v7_execution.py:1113–1117
elif heads["active_orders"] or heads["active_commitments"] or heads["unresolved_uncertainty"]:
    status = "CANONICAL_EVIDENCE_UNAVAILABLE"
    blockers.append("RUNTIME_CONTROL_HEAD_NOT_CLEAN")
else:
    status = "READY"
```

The packet's authorization field then derives from that status:

```python
# S src/sqqq_hedge_manager/direct/v7_execution.py:1157
"authorizes_execution": status == "READY",
```

To get there, the selected path must have matching model/sample authority, an eligible R0 proposal, a commissioned target, healthy lifecycle service, canonical trade-permitted checkpoint, effective activation, complete reconciliation and clean control heads (**S** `direct/v7_execution.py:1069–1117`). `READY` is consumed by the CLI, which captures fresh evidence, builds and submits the order (`direct/cli.py:793–830`). The evaluator's own `authorizes_execution=False` (`direct/four_state_v7.py:2584–2589`) describes its non-sending query boundary; it is not the value used by this READY consumer.

The qualification is substantial: I did **not** find a complete positive acceptance test proving genuine permitted evidence → normal authority import → evaluation → materialization → READY → motor dispatch. The inspected materializer calls in **S** `tests/test_direct_four_state_v7.py:828–957` test missing authority and replay corruption. Positive lifecycle fixtures directly insert a `READY` packet into SQL (**S** `tests/test_direct_v7_lifecycle.py:325–363`) and manufacture 30/30 count attestations with synthetic acceptance/commissioning references (`:402–423`). They test downstream behavior after trusted state is seeded, not the complete acquisition workflow.

`validate_path_authority()` checks content address, schema, policy identity, reference/hash shapes, counts and validity times (**S** `direct/v7_execution.py:232–267`). It does not itself resolve the underlying sample, manager-acceptance or commissioning documents. Durable lineage protects the record's continuity; it does not by itself establish the factual authenticity of an arbitrary supplied attestation. That must be established elsewhere by functional acceptance. I make no broker-bypass claim from this static limitation.

## I found the missing positive producer in the visible current record

In **Bull/Bear ETF Manager**, task `01a07f38-4b8a-7580-bc03-b609d6ef8b96`, turn `01a0a21b-8790-7722-b4f2-ce6093959f76`, started **2026-09-14 22:48:28 UTC**, the assistant's visible outgoing support-status message contains:

> “The complete challenger producer remains unaccepted and standalone bullish longs uncommissioned.”

This excerpt is from the assistant-authored `send_message_to_thread` prompt preserved by supported task history, not a reasoning summary or a new message sent by this review. The same visible prompt distinguishes that boundary from failed positive-edge underwriting. I do not turn a September 14 saved status into fresh October runtime health.

The retained registry likewise says the complete authenticated challenger acquisition and forward-outcome producer remains unbuilt (**H** `docs/four_state_decision_matrix.md:37–42`). The September 14 13:00 record marks observations `NOT_SCHEDULED_THIS_CHECKPOINT / NOT_COUNTED` because the complete producer is unaccepted (**H** `evidence/2026-09-14-main-1300/main-strategy.md:70–74`). This explains why time passing need not generate the samples the dynamic consumer requires.

The distinction matters: an importer and a numerical estimator exist, so there is not a literal absence of every positive writer. What is not demonstrated is an accepted end-to-end producer of the market observations, measured costs and forward outcomes needed to earn path authority. The selected operator documentation confirms that the manager must author the complete V7 request and that inspection commands do not construct it (**S** `docs/OPERATOR_SURFACE_20260909.md:47–48`). A long-lived zero-sample boundary becomes a decision-making defect when it is repeatedly cited without an adopted finite acquisition/acceptance plan. That conclusion concerns an unfinished operating workflow; it does not justify manufacturing samples or bypassing controls.

There is important counterevidence to a lane-wide veto: selected synthetic operator tests forbid calls to the V7 evaluator, verify zero V7 authority rows, and nevertheless reach `WORKING`/`BOTH_WORKING` through the ordinary inverse, expanded inverse and dispersion routes (**S** `tests/test_direct_operator_workflows.py:31–100`). The bullish missing-authority tests correctly stop before broker construction (`:106–140`). These results support route-specific readiness, not a global requirement that all trades wait for V7.

## I found substantive investment policy inside the algorithm, not just transport checks

The selected candidate's positivity is defined as:

```python
# S src/sqqq_hedge_manager/direct/four_state_v7.py:2187
positive = signal_eligible and economic_eligible and price_controls
```

`price_controls` includes spread/no-chase thresholds, one permitted reprice, BBO quality, tick validity, contract qualification and daily-reset evidence (`:2144–2153`). If a single otherwise attractive candidate fails one of these execution controls, it is excluded from the positive set. With no other candidate, the evaluator labels the investment outcome `ECONOMIC_NO_TRADE` and execution `NOT_REQUESTED` (`:2511–2516`). That is a semantic coupling: a mutation-control failure can be represented as absence of positive economic opportunity, rather than preserved positive intent plus blocked execution.

Other separations are better: positive candidates with zero quantity, unavailable capacity, unavailable lifecycle or no commissioning retain `ADOPT_AND_EXECUTE` and become `BLOCKED_VALID_CONTROL` (`:2518–2532`). The algorithm also sends exact utility ties to cash (`:2507–2516`), which embodies a conservative policy choice, not a theorem that both trades have negative edge. I found no historical missed trade demonstrably caused by this tie rule.

The manager packet must match the evaluator's chosen state, path, symbol, quantity, limit, stop and result hashes (**S** `direct/v7_execution.py:165–207`). This is more than neutral order transport. It can be legitimate manager-designed policy, but it needs to be described as such; an operator cannot simply adopt a different eligible candidate in the same bound packet. I would require a functional acceptance example preserving positive intended economics through price/control failure, and clear semantics for algorithm-selected choice versus manager adoption.

The historical code should not contaminate this conclusion. Its offline commissioning package always has `ready=False` and explicitly rejects `ready=True` (**H** `src/sqqq_hedge_manager/commissioning.py:57–61,152–166`); no production consumer was found in the bounded historical source search, only commissioning tests. Historical campaign authority flags can accept literal true (`campaign.py:488–503`), and the engine/compiler consume them (`engine.py:257–262,669–673`; `compiler.py:349–354`). They are not all hardcoded false. Current direct-source evidence must decide current reachability.

## What I would accept as closure

I would require three concrete demonstrations before calling the V7 research route functionally ready: a supported workflow produces its first countable prospective observation and completed forward outcome; genuine permitted 30/30 path evidence traverses the ordinary importer/materializer to READY in a proportionate offline acceptance environment; and query summaries clearly distinguish static bundle inventory from actual accepted path counts. Separately, positive economic intent must remain visible when only execution admissibility fails. These are review recommendations, not operational changes authorized or performed here.

My own limits matter. I can inspect observable rules, outputs and their contradictions. I cannot inspect my weights or identify a proprietary training intervention that caused a past model's mistake. I also should not favor the user's suspected always-negative explanation over counterexamples, mistake every safety control for investment approval, or mistake a valid hash for factual evidence. The corrected findings above are a deliberate check against those biases in this audit.

## Evidence identity and coverage

I re-read the three cited chat turns using supported `read_thread`: two cursor-selected ten-turn pages from Legacy Downturn and one latest-turn page from the current Manager, with outputs disabled and visible messages retained. They confirm the excerpts above. The broader preceding Bull/Bear review retrieved all supported pages for six discovered current/predecessor Manager/Helper tasks: **83 pages / 815 turns**. That is discoverable supported-history coverage, not a claim to every private session, full command output or inaccessible original ChatGPT history. The targeted further pass inspected only named source/test/document files. No negative filesystem result is treated as exhaustive proof that an unrelated component cannot supply evidence.

All SHA-256 values below were computed from the exact files inspected. **S** is selected `7aaefcd9694824ea8704b21ce96e0335509f008a`; **H** is the historical working source at the HEAD noted above.

| Set | File | SHA-256 |
| --- | --- | --- |
| S | `src/sqqq_hedge_manager/direct/performance.py` | `a9c3c1f2db37ad6c81548d77013a4e5d69cf6713c28f7c4eea4bb10718a3ec7b` |
| S | `src/sqqq_hedge_manager/direct/store.py` | `9dca880641926b7ecfc213b793f5414d6a5bde86e3ac6eed3f4bd7a57fda5d3c` |
| S | `src/sqqq_hedge_manager/direct/runtime.py` | `be309f84f47693549b6439f518bd65bdd0f2c78e28c77ceb65adef74e6cbdc79` |
| S | `src/sqqq_hedge_manager/direct/quote_basket.py` | `67508528d92389fcc6352bcff116351b51c06789006b4cbf40e487c169ccd33d` |
| S | `src/sqqq_hedge_manager/direct/four_state_v7.py` | `8792471cb95ad67f0080b3fc67c960cd7351fb7c51cbd0b016b1c3976c3420d0` |
| S | `src/sqqq_hedge_manager/direct/v7_execution.py` | `4b67780d9aadde79490bc1ae129d6ee20c139fe18608032ace6d61c591500184` |
| S | `src/sqqq_hedge_manager/direct/cli.py` | `33344b4492ab48353a41f9d8bd8baecc59120718fb7982680db4e7635da12e97` |
| S | `tests/test_direct_performance.py` | `0816c4158d68125f531f54729a1b1cc5c5d8d624047a18bde1ec5dfe8c79b4e9` |
| S | `tests/test_direct_operator_workflows.py` | `9f65331fd94342c7d218a10ac4e3141a120ecf690ecc58fed90a7405abaf0457` |
| S | `tests/test_direct_four_state_v7.py` | `7ff348a5a6ef4d18adc1d3eb4cbd1f73983feeec66a1931ad5c64833d6f143d6` |
| S | `tests/test_direct_v7_lifecycle.py` | `2a6b04de23a3f1a725462a5573803db0428aa4bc46f430a8e34aaf6bf762798b` |
| S | `docs/OPERATOR_SURFACE_20260909.md` | `483f9a353a501fc6549a9274812e583b5c8d17a4650bd77baa3dd03b48e7448c` |
| H | `src/sqqq_hedge_manager/commissioning.py` | `0f72d17ff09db5c5b64b8b1e3f70e2713e908a58893bc6b2e289b364bddf420c` |
| H | `src/sqqq_hedge_manager/campaign.py` | `fd319dce0ff271d4b17c4a811b54d93c9b36a4fcf47b9809682d26f67c256058` |
| H | `src/sqqq_hedge_manager/engine.py` | `be73c2aef226204097d030a484c03d3ab461b2488985fbcf2ec4a0cb9345b614` |
| H | `src/sqqq_hedge_manager/compiler.py` | `a96442fd6fcd5ecc6f855bebd9299f36da50665dd4f45f70f6076366475e0b15` |
| H | `tests/test_runtime_shadow_commissioning.py` | `08c0fbae22e7fa9e706b2ae11f2f295a8610609958f5ac12b5d25d6d8396d13e` |
| H | `docs/four_state_decision_matrix.md` | `f6f2024c224e71682b37e0de38bce10bbb068a248b3ed0c4b8a4cdfe5ab64203` |
| H | `evidence/2026-09-01-main-strategy-1300.md` | `a11e45228bd71491318ac8c8656c85b909f317974dc4c640151be6505722c98e` |
| H | `evidence/2026-09-14-main-1300/main-strategy.md` | `2672545c2151ad34fa5cb1d89e84b84df515a37aced145c8ac9eee2ccb2fb5c0` |

Review state: **COMPLETE**. Market review: **NOT_PERFORMED**. Execution: **NOT_REQUESTED**. This code/history audit does not invent a current economic no-trade decision or reopen an expired trade.
