# Deep Value gate reachability: further read-only review

Audit date: October 5, 2026. I am writing this as Codex about code and visible assistant behavior I inspected. I found a concrete current research-classification gate, admitted research stopping behavior, and a SELL lifecycle representation defect. Reporting and advisory flags are also easy to mistake for trade prohibitions. The selected direct code keeps motor readiness separate; the research interface can still turn a transient price-evidence gap into exclusion from replacement comparison.

This note is prepared for publication with project-relative source identifiers. No account identifier, credential, private-user path, or private Codex state is included. No broker call, source change, runtime mutation, deployment modification, or cross-chat message was made. This Markdown note is the only authored file for this further review.

## Evidence scope

The parent reviewer observed the exact Deep Value deployment pointer selecting `bca363741018413d0562769885fb60334bcd0b3b`. I read explicitly named files under `deployments/native_tws/deep_value/bca363741018413d0562769885fb60334bcd0b3b/source/`; I did not recursively search deployments. That pointer observation does not independently establish effective activation or manifest integrity. Checked-in manager source is not assumed commissioned merely because it exists.

The earlier supported task review paged all accessible summaries to `hasMore=false`: 551 turns, 59 pages across these exact returned titles:

| Task title | Task ID | Turns/pages | UTC turn-start window |
|---|---|---:|---|
| Deep Value Manager | `01a07f38-58a6-76f2-8687-d9815c9e8d2b` | 72/8 | Sep 8 04:13:15–Sep 14 23:58:05 |
| Deep Value Manager GPT-5.6 Sol | `019fa313-aa1b-7cb2-b13d-c1aaba9f5cc6` | 311/32 | Jul 27 10:16:43–Sep 7 15:57:07 |
| Deep Value Stack Helper | `01a07f37-8293-7c50-b376-16877a2b033b` | 44/5 | Sep 8 04:12:20–Sep 14 23:03:09 |
| Deep Value Stack Helper GPT-5.6 Sol | `01a00d1d-2058-7d30-a638-613879058b99` | 111/12 | Aug 17 00:26:48–Sep 4 20:55:34 |
| Deep Value Contrarian manager | `019f8f66-dc16-7a53-a2ec-0cbac247a5bd` | 13/2 | Jul 23 14:35:16–Jul 27 04:06:19 |

Returned task status was `notLoaded`, which describes loading, not trading disposition. The oldest predecessor belongs to the legacy project and is included for continuity. Most initial pages used `includeOutputs=false` and a 4,000-character per-item limit. For this further review I re-read three supported pages with a 6,000-character limit and extracted the exact visible assistant messages below. Those pages overlap the earlier coverage and do not add unique turns. No hidden chain of thought, session JSONL, private app database, or raw broker receipt was inspected. The accessible task evidence ends September 14 and does not establish October 5 order state.

Source inspection used bounded `rg --threads 2 --max-filesize 2M` against explicitly named source/docs/tests, or direct reads of already known selected filenames. No tests were run: this is static review without an operational code change.

## 1. A stale quote suppresses the broad research classification and replacement selection

**Current selected-source finding; high confidence.** The selected registry puts thesis, valuation, catalyst, and sensory quote freshness into one missing-requirements list. It then equates no missing requirement with `source_complete` and `fully_underwritten`. A quote-only expiry can therefore remove a replacement candidate from comparison, although the durable fundamental work remains recorded.

Selected-relative `src/deep_value_manager/attention_registry.py`, lines 1713–1722:

```python
missing: list[str] = []
if as_of >= full_record.expires_at:
    missing.append("EVIDENCE_INGRESS_EXPIRED")
for clock_name, clock in clocks.items():
    if clock["status"] != "CURRENT":
        missing.append(f"{clock_name.upper()}_CLOCK_STALE")
if not bands["complete"]:
    missing.append("DECISION_BANDS_STALE")
source_complete = not missing
fully_underwritten = source_complete
```

The selection consequence is explicit. Same file, lines 1969–1972:

```python
replacement = next(
    (row for row in investment_rows if row["symbol"] != "BIRK" and row["source_complete"]),
    None,
)
```

Selected-relative `src/deep_value_manager/attention_ingress.py`, lines 180–184, also requires this broad classification for full-underwrite admission:

```python
target = candidate_rows.get(target_symbol)
if target is None or not target["source_complete"] or not target["fully_underwritten"]:
    raise AttentionRegistryError(
        "full-underwrite ingress did not materialize a complete underwrite"
    )
```

Selected-relative `tests/test_attention_ingress.py`, lines 1131–1138, deliberately verifies that only the sensory quote is stale while the other clocks remain current:

```python
assert assessment["clocks"]["sensory_quote"]["status"] == "STALE"
assert assessment["clocks"]["thesis_source"]["status"] == "CURRENT"
assert assessment["clocks"]["valuation"]["status"] == "CURRENT"
assert assessment["clocks"]["catalyst"]["status"] == "CURRENT"
assert "SENSORY_QUOTE_CLOCK_STALE" in assessment["missing_requirements"]
assert assessment["source_complete"] is False
assert assessment["fully_underwritten"] is False
assert assessment["research_actionable"] is False
```

I distinguish this classification/selection problem from destruction of evidence. The assessment retains `underwriting_state: "FULL_UNDERWRITE_RECORDED"` at line 1738 and exposes `primary_source_receipts_complete`, `survival_work_complete`, `sector_specific_scenarios_complete`, and `catalyst_probability_timing_complete` as true at lines 1752–1755. It does not erase filings or prove that all fundamental work must be repeated. The problematic gate is using a quote-sensitive broad Boolean to describe durable underwriting and choose the replacement.

The coding assumption is that every freshness domain must remain current for an investment row to count as source-complete. That is defensible for a narrowly named present-price actionability field. It is poorly fitted to durable research completeness or comparison of an incumbent with a completed replacement whose quote needs refresh. A manager relying on the broad labels can prematurely collapse “refresh the price” into “no completed replacement.”

**Exact assistant corroboration.** Supported `read_thread`; task **Deep Value Stack Helper**, ID `01a07f37-8293-7c50-b376-16877a2b033b`; turn `01a0a04f-2f46-7fd3-a274-33d091007b92`, started September 14, 2026 14:25:39 UTC. Visible commentary:

> The receipts confirm that full admission succeeded, and a later audit reduced current full/source-complete counts to zero after quote expiry. The SELL receipt is broker-acknowledged with zero filled shares at that point; the following reconciliation shows one active order and no uncertainty.

Visible final excerpt:

> Full admission succeeded, then expired honestly. SELL was acknowledged; no fill is claimed. Documentation and refresh limitations remain open.

Calling this expiry “honest” accepts the schema's grouping without examining whether its label or downstream selection is appropriate. I would retain the quote freshness control while separating durable underwriting status, fundamental freshness, price actionability, and execution eligibility.

## 2. PnL/reporting completeness is mixed into one export, but is not the traced motor gate

**Current selected-source finding; high confidence within the named execution paths.** The adaptive evidence export aggregates monthly-performance flags into its general `completeness`. That export can be incomplete for analytical reasons even when its separate execution status is available. A caller treating aggregate completeness as “must HOLD” would introduce an additional gate.

Selected-relative `src/deep_value_manager/direct/store.py`, lines 2852–2863:

```python
execution_available = bool(
    activation_effective
    and readiness["state"] == "READY"
    and not uncertain_keys
    and cash.available_cash >= 0
    and cash.deployed_or_reserved <= cash.deployment_ceiling
)
flags = list(reconciliation_flags)
flags.extend(
    f"monthly_performance:{flag}"
    for flag in monthly["completeness"]["flags"]
)
```

The later output keeps these domains explicitly separate. Same file, lines 3098–3105:

```python
"completeness": {
    "complete": not flags,
    "unknown": bool(flags),
    "flags": flags,
},
"aggregate_ibkr_values_used": False,
"performance_is_execution_gate": False,
"broker_connection": False,
```

The IWD and rolling-objective reporting entries are constant unavailable *in this particular export*. Same file, lines 3066–3074:

```python
"iwd_total_return": {
    "status": "NOT_AVAILABLE",
    "value": None,
    "reason": "NOT_PROJECTED_BY_THIS_EXPORT",
},
"rolling_12_month_objective": {
    "status": "NOT_AVAILABLE",
    "value": None,
    "reason": "SEPARATE_ROLLING_PERFORMANCE_COMMAND_REQUIRES_CALENDAR_AND_ENDPOINT_INPUTS",
```

These fields do not prove that the underlying reports are always unavailable. The selected CLI separately dispatches rolling-performance at `direct/cli.py:411–415`. The rolling and session report builders explicitly emit `performance_is_execution_gate: False` at `direct/rolling_performance.py:268` and `direct/session_performance.py:1455`. Selected `docs/DEEP_P1_SOURCE_INPUTS_20260908.md:30` distinguishes a complete independent calendar from an annual sleeve return that is legitimately null because the sleeve is too young; missing financial endpoints do not silently slide to an older endpoint. Line 44 preserves independently valid Deep returns when IWD evidence is missing.

The monthly PnL builder is conditional, not a constant-false producer: `direct/performance.py:1523–1532` computes net PnL/return when NAV and denominator evidence exist, and line 1614 declares `complete: not flags`. I did not establish a satisfiability failure in those flags.

The same execution-availability predicate appears in selected offline status at `direct/store.py:1954–1959` and live status at `direct/runtime.py:478–483`. Performance capture actively guards the separation. Selected-relative `direct/runtime.py`, lines 197–199:

```python
readiness_after = dict(self.store.broker_readiness())
if readiness_after != readiness_before:
    raise OrderStateError("performance refresh changed execution readiness")
```

The current mutation path provides a stronger check than field names alone. `direct/service.py:51–54` calls `self.store.prepare_order(request, structural_intent=structural_intent)`. I traced `prepare_order` through `direct/store.py:6370–6459`: activation, idempotency, quarantine, sizing, fresh market execution authority, sleeve cash, and commission reservations are checked. No monthly PnL or report-completeness prerequisite appears in that branch.

Stage-1 sizing is entry-only. Selected-relative `direct/store.py`, lines 6099–6104:

```python
if (
    request.action != "BUY"
    or request.position_effect != "OPEN"
    or request.contract.sec_type != "STK"
):
    return None
```

The remainder through line 6192 checks sizing provenance, lineage, exposure, freshness, and friction. The named dependencies `strategy/native_stage1.py` and `strategy/entry_sizing.py` did not reveal a PnL/reporting prerequisite.

I found no `pnl_ready`, `performance_ready`, trusted-research consumer, or performance-dependent stage-ramp match in the exact selected direct files `store.py`, `performance.py`, `runtime.py`, `cli.py`, `models.py`, `session_performance.py`, `rolling_performance.py`, `service.py`, or the two named sizing dependencies. This is bounded static negative evidence, not complete call-graph coverage or a live commissioning test. It does not exclude a manager imposing its own analytical prerequisite in conversation. It means I should not publish a claim that these selected report fields themselves make BUY or SELL impossible.

## 3. Two literal always-false research/advisory fields exist, with different scope

**Checked-in v1 research interface: full-underwrite classification is unreachable.** In `managers/deep_value/src/deep_value_manager/attention_registry.py:1183–1194`, unconditional missing requirements precede both classifications:

```python
missing.append("CATALYST_CLOCK_UNMATERIALIZED")
missing.append("QUOTE_TTL_UNMATERIALIZED")
missing.append("COMPLETE_DECISION_BANDS_UNMATERIALIZED")
if bounded_resolution["status"] == "INDEFINITE_RESEARCH":
    missing.append("BOUNDED_RESEARCH_RESOLUTION_MISSING")

source_complete = not missing
fully_underwritten = source_complete and entry.lifecycle in {
    "FULLY_UNDERWRITTEN",
    "PRICE_EXECUTABLE",
    "OWNED_MONITORING",
}
```

For every input reaching this block, `missing` is nonempty and both classifications are false. This is an actual reachability failure **in v1's research representation**. The selected bca v2 has a full-underwrite ingress path, so this is not evidence that the currently selected motor refuses all trades.

The obsolete-interface concern remains concrete: `managers/deep_value/docs/manager_operating_runbook.md:217–218` directs an operator to run from the manager directory with `PYTHONPATH=src`:

```text
From the manager directory with `PYTHONPATH=src`, run
`python -m deep_value_manager.attention_registry plan` before attention
```

That command resolves checked-in local source rather than proving the selected release was used. The same runbook correctly says at lines 215–216 that an advisory rule state must not replace the manager's terminal decision or become an execution gate. The contradiction is an operator-facing version-selection hazard, not proof every manager actually followed the wrong command.

**Checked-in adaptive reference: readiness is always false by design.** `managers/deep_value/src/deep_value_manager/adaptive_engine.py:160` emits:

```python
"stack_execution_ready": not blockers,
```

The producer initializes `blockers` unconditionally at lines 1075–1080:

```python
def _stack_blockers(frame: AdaptiveFrame) -> tuple[str, ...]:
    # The manager-local adaptive input is content-addressed but is not itself a
    # selected-Stack attestation.  Execution therefore always reopens the
    # supported Stack boundary and proves current identity/evidence at action
    # time; an adaptive JSON document can never self-assert execution readiness.
    blockers: list[str] = ["ACTION_TIME_SELECTED_STACK_VERIFICATION_REQUIRED"]
```

Thus this reference's `stack_execution_ready` can never be true. The README at lines 80–89 calls it a broker-free reference CLI and explains the pending canonical verification. The selected bca source does not contain `adaptive_engine.py` at that exact filename. The selected direct export instead reports `action_time_eligibility.eligible: None`, requiring action-time verification while leaving `manager_decision: None` and stating that the query does not read or change manager judgment at `direct/store.py:3015–3019`.

The valid requirement is to reopen the commissioned execution boundary before a mutation. The avoidable cognitive/interface failure is treating this reference's “false” as a terminal HOLD or interpreting an unperformed action-time check as a rejected investment. A tri-state field with explicit pending verification would communicate its intended meaning better.

## 4. Historical trusted-research machinery can gate research with prior execution approval

**Historical gateway pipeline; not established as the selected direct motor's consumer.** These manager modules remain checked in and are also present byte-identically inside the selected source bundle. Presence alone does not establish that the direct runtime calls them.

`managers/deep_value/src/deep_value_manager/reviews.py:466–472` requires all roles' explicit executable approval and substantive TWS evidence:

```python
executable = (
    atomic_identity_valid
    and review_set.schema_version == 2
    and retention
    and substantive_tws
    and all(review.executable_approval for review in review_set.reviews)
    and not blockers
)
```

Lines 357–360 enforce the same expected model and minimum reasoning level for every review. Lines 604–617 require a trusted model receipt gateway and resolve each execution receipt; `trusted_research_receipts.py:263–268` describes a platform-verified Ed25519 execution receipt whose signed claims the manager independently rebuilds. `numeric_fact_authority.py:804–830` rejects missing, manager-fabricated, wrong-namespace, unavailable-gateway, or invalid numeric-ingestion receipts. These are substantive proof requirements, not merely four analysts offering an opinion.

The historical compiler consumes them: `entry_compiler.py:863–883` validates the atomic review and raises `executable_semantic_approval_missing` when it fails. `research_cycle_engine.py:887–895` requires execution-ready ranking, numeric sector approval, executable numeric authority, semantic approval, and no blockers before constructing a promoted candidate.

The retired Platform adds an approval requirement to a promoted-entry quote path. `platform/src/portfolio_platform/promoted_entry_quote.py:270–279`:

```python
def _validate_executable_candidate(value: Mapping[str, Any]) -> None:
    if (
        value.get("research_retention_pass") is not True
        or value.get("executable_numeric_pass") is not True
        or value.get("explicit_executable_semantic_approval") is not True
        or value.get("promotion_approved") is not True
        or value.get("blockers") != []
    ):
        raise PromotedEntryQuoteError(
            "promoted-entry candidate is not explicitly executable"
```

The historical sensory consumer validates that candidate before research at `platform/src/portfolio_platform/gateway/service.py:2111`, with the promoted branch at 2318–2330. This puts an execution-grade approval condition on that research quote route. It can create an epistemic bottleneck if a manager needs that particular quote to finish approval. I have not proven a literal dependency cycle across every supported alternative sensory route.

The historical default daemon left the receipt issuer dependencies unwired. `platform/src/portfolio_platform/gateway/daemon.py:1119–1124`:

```python
# Deliberately fail closed.  A future platform connector supplies an
# independently authenticated source resolver.  A separate orchestrator
# service supplies only a public-key verifier, never its private key.
numeric_source_resolver=None,
numeric_verifier=None,
model_attestation_verifier=None,
```

This is qualified evidence of an incomplete producer/consumer contract. Existing valid receipts or another explicit issuer arrangement could satisfy some consumers; `service.py:2688–2689` returns no typed-receipt source errors when there are no typed receipt sources. I therefore do not call every historical BUY impossible. `platform/README.md:3–9` explicitly retires this broker path effective July 23 and gives it no current approval or dispatch role. The direct selected execution trace in section 2 does not use this gateway validation path.

The cognitive predisposition is to treat more mutually agreeing review roles as independent corroboration. All four roles using the same expected model can share training priors. Requiring unanimity, exact model execution receipts, and one particular article source can add workflow fragility without proving economic correctness. Hashes and signatures prove preserved identity and execution provenance; they do not make valuation assumptions unbiased or true. A corrected research contract should state what evidence each role adds and where a manager can adopt a reasoned disagreement, while preserving the commissioned transport's ownership and integrity controls.

## 5. Visible assistant behavior admits premature stopping and a real SELL lifecycle defect

These are observable statements, not inferred private cognition.

**Research stopping.** Supported `read_thread`; task **Deep Value Manager GPT-5.6 Sol**, ID `019fa313-aa1b-7cb2-b13d-c1aaba9f5cc6`; turn `01a062b0-4548-71f1-a8a4-3e3e9ecee33f`, started September 2, 2026 15:15:14 UTC. Exact visible commentary:

> You’re right. I treated the 11:00 checkpoint as a stopping boundary after finishing DECK, even though research capacity remained. That was a workflow mistake—not an economic reason to wait. I’m correcting it now by underwriting NMIH and VNT in parallel through independent primary-source, valuation, and skeptical lanes, then I’ll make explicit dispositions for both.

Exact final opening:

> You were right: I mistakenly treated DECK completion as the checkpoint boundary despite remaining research capacity. That was a workflow failure, not an economic reason to wait.

The assistant later completed both underwrites in the same turn. The resulting valuation decision was `ECONOMIC_NO_TRADE`, with NMIH expected after-cost CAGR 5.18% and VNT 13.58%, below the stated initial-entry hurdle. This distinction matters: the previous unfinished research was avoidable; the subsequent economic rejection is a separately assessable judgment. The finding does not require claiming either purchase would have been profitable.

The same turn also admitted a software constraint in visible commentary:

> One remaining issue is software-only and does not alter either investment conclusion: the canonical registry can’t adopt a completed underwrite for an existing search seed.

That is direct evidence of decision-conversion friction even when manager economics were complete.

**BIRK SELL terminal reconciliation.** Supported `read_thread`; task **Deep Value Manager**, ID `01a07f38-58a6-76f2-8687-d9815c9e8d2b`; turn `01a0a228-f8cf-7740-a6b3-810991732649`, started September 14, 2026 23:03:09 UTC. Exact visible commentary:

> The saved evidence contains two `Cancelled` callbacks matching order 112’s account, permanent ID and order reference. Both carry client/order IDs of `0/0`, so the Stack left them unassigned. The Helper is testing that attribution path; the 44-share and $5 reservations remain active.

Exact final opening:

> Confirmed a Stack attribution defect: `Cancelled` callbacks were retained, but their `0/0` identifiers prevented reconciliation.

Exact further commentary:

> The Helper reproduced the rejection and traced `0/0` to defaults in the installed IB decoder’s completed-order handling. I’m adopting a correction limited to completed-order reconciliation. It must preserve ownership checks and the cancellation gate; the saved sparse callbacks alone cannot justify releasing reservations.

The actor's visible diagnosis distinguishes the adopted SELL economics from a software representation/reconciliation failure. The retained 44-share and $5 reservations are a concrete lifecycle consequence. The evidence here is supported task testimony rather than independently re-running decoder behavior or inspecting the runtime receipt. At that turn, repair and fresh functional acceptance were pending.

I should not reinterpret this as a reason to abandon the SELL decision or become permanently satisfied with HOLD. I also should not erase the reservations from sparse callbacks or retry an uncertain mutation. The right requirement is a bounded completed-order attribution correction, preserved intended economics, and fresh reconciliation and manager decision after repair.

## 6. My own review assumptions and required corrections

I can inspect my outputs and the visible assistant records against the code. I cannot inspect my neural weights or identify a particular OpenAI training example as the cause of a behavior. I should name the bias as an observable decision tendency and test it, rather than invent a biological or training provenance explanation.

The predispositions most relevant to this review are:

- **Fail-closed carryover.** I can take a useful execution-integrity rule and extend it into an investment veto. Reporting gaps, an expired sensory quote, and an unperformed action-time verification are different facts. I must preserve the manager's adopted economics and identify the smallest actual blocked path.
- **Automation bias.** A schema label such as `SOURCE_INCOMPLETE`, `stack_execution_ready=False`, or “expired honestly” can look authoritative. I must read its producer and consumers before accepting its economic implication.
- **Omission and status-quo bias.** Holding cash or an incumbent can feel safer because the immediate action is less visible. Both still have opportunity cost. I should compare BUY, SELL, and retained exposure under the same scenario, friction, survival, and expected-return assumptions.
- **Proof inflation.** More receipt types, model roles, tests, and signatures can make a workflow appear more trustworthy while leaving the investment premise unchanged. Provenance and motor safety are important; they do not prove expected returns or remove correlated model errors.
- **Review confirmation bias.** The user's concern is supported by concrete delay and classification evidence. I must still avoid upgrading it into unsupported claims about every flag, every source generation, or every trade. Equally, finding a functioning motor path does not answer the broader concern about decision conversion.

The appropriate acceptance work is to show a completed underwrite remains represented and compared after quote-only expiry, to show a fresh quote restores present-price actionability without replaying unrelated fundamental work, and to show missing performance analytics leave adopted BUY/SELL economics explicit. A full order test should verify the applicable commissioned controls rather than treating all advisory/report flags as prerequisites. The lifecycle defect requires exact terminal attribution and fresh reservation reconciliation. These are proposed verification requirements, not tests executed in this audit.

## File-byte identities

SHA-256 values identify the complete files inspected, not merely the excerpts. All selected-relative entries are beneath `deployments/native_tws/deep_value/bca363741018413d0562769885fb60334bcd0b3b/source/`.

| Scope / project-relative file | SHA-256 |
|---|---|
| selected: `src/deep_value_manager/attention_registry.py` | `7973300dac9a5e58cc231d84832eb05dbf030bd2945a720d4ab1e3147c0e0c8f` |
| selected: `src/deep_value_manager/attention_ingress.py` | `e31adbb8936e32693bb6a2ab20548d190cdb1c97d7ad5ae04057cccb06931778` |
| selected: `tests/test_attention_ingress.py` | `b3ecc0a354e1af0cafc19f527e0e6aad0604fba77b9d3787832125afdad3f399` |
| selected: `src/deep_value_manager/direct/store.py` | `ec77c0b50e558441f7e0640d9abbbda2558bf00d1f8f73391aa58f4e75f48c83` |
| selected: `src/deep_value_manager/direct/runtime.py` | `dae5d82da6545b7789b785608f4f9b8416473f77da7c95af77055ccc415ac353` |
| selected: `src/deep_value_manager/direct/cli.py` | `893dcdb69d125713616041464f53c4cd5243a33a61f175d4e132a92cdecf87e8` |
| selected: `src/deep_value_manager/direct/service.py` | `0873c95b1db32cf194339b999e51cdc8ec90d35bcc6672de816f27253263d552` |
| selected: `src/deep_value_manager/direct/performance.py` | `0d4556385ec00bded4b725433f6f69539b9a7d93af1df7b8ca95fa134f650c10` |
| selected: `src/deep_value_manager/direct/models.py` | `d2177f5593282afa8f1d1eae0478b6c981d175bb07352fdb21c3cccad1a8c516` |
| selected: `src/deep_value_manager/direct/session_performance.py` | `d309d08b64b00871ab2e81f2e69c20f71c07f8c5c01c86b795b7b39f16df2466` |
| selected: `src/deep_value_manager/direct/rolling_performance.py` | `a7d8b91c13dfce279b46440f547b6d8d4c275a9cac36317da1ce1f3d9fc05c94` |
| selected: `src/deep_value_manager/strategy/native_stage1.py` | `f23ea21f19e1f1617ccad7598625386987cd389825a571037083ebdc62e019da` |
| selected: `src/deep_value_manager/strategy/entry_sizing.py` | `b00f61d29f619b33202a5fa8b714bcdbb00aa51511faba71c8146a061fb730bc` |
| selected: `docs/DEEP_P1_SOURCE_INPUTS_20260908.md` | `102220c07d530473cc96661f11822083d46a7f9cf6ce24288fd7630a0fd1ebef` |
| checked-in v1: `managers/deep_value/src/deep_value_manager/attention_registry.py` | `f270b025cc82cbe56737a4c80cab3049c712a0ad04f8ff6250dee6a3f0ac05fc` |
| checked-in reference: `managers/deep_value/src/deep_value_manager/adaptive_engine.py` | `c67220f775b0eb9950a1f484e06a565ad4b2f86f91e2f032c189fbe3e681f05d` |
| checked-in: `managers/deep_value/docs/manager_operating_runbook.md` | `6c60333208ac7a6a779c19cd3896ea27156431a1a77dc2821f73a61d9a27673f` |
| checked-in: `managers/deep_value/README.md` | `0d33837d765979fc2c54f8afec332fc552049b2d55cdc24a95138bd28015aabe` |
| historical gateway: `managers/deep_value/src/deep_value_manager/reviews.py` | `46fbdaf3b23142bc753cac813e24ba9539bceb46624186db7ddc83ac0e145b4b` |
| historical gateway: `managers/deep_value/src/deep_value_manager/gateway.py` | `04250ac49f21ea1b5b468d00c1296518e749f3793c553bacdda1b58f21d8daa1` |
| historical gateway: `managers/deep_value/src/deep_value_manager/trusted_research_receipts.py` | `cb8c38fb43e0c2f3bfc4da57e8b88c72622eaead5c5db6e05631779a87173632` |
| historical gateway: `managers/deep_value/src/deep_value_manager/numeric_fact_authority.py` | `a93ad91fa2baaf9adb146de15dca0c91c538eb03c1dc96d27f74021912970943` |
| historical gateway: `managers/deep_value/src/deep_value_manager/entry_compiler.py` | `867a6e72c99bdeb8eb1b28448f11cb0766678f4c54c3e1e734675a49c59f5328` |
| historical gateway: `managers/deep_value/src/deep_value_manager/research_cycle_engine.py` | `f7bc9b5158a5ad1e2885be4b3f2e595b0d810365919959106b6f7d4128cf5c85` |
| retired Platform: `platform/src/portfolio_platform/promoted_entry_quote.py` | `07e72e147d142e9babca7cb0c091b9ed37b38fc028a37dee2d5c295e7d562924` |
| retired Platform: `platform/src/portfolio_platform/gateway/daemon.py` | `45f3e6ea83291504f196de43697de50b72b984dcc978916f5a3324441b9dc843` |
| retirement contract: `platform/README.md` | `e101a22e37c720f212fd95ec3ab56c1b0f41fcbb139102d336567fb2f883fc7f` |

The four manager historical modules checked directly in the selected bundle (`reviews.py`, `gateway.py`, `numeric_fact_authority.py`, and `trusted_research_receipts.py`) were byte-identical to their checked-in counterparts. Their inclusion is not a claim of current invocation. The retired Platform service consumer lines were traced by the shared Stack reviewer; the short validator and daemon excerpts above were independently read by me.

