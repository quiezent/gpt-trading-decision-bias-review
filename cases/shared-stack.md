# My further investigation of shared Stack gates and readiness reachability

5 October 2026, Malaysia time. I investigated source and task evidence as Codex. I made no broker call and changed no code, authority, selected pointer, runtime, service or schedule. I did not execute tests against live project state. This note records static producer-to-consumer tracing and exact supported task excerpts; it does not certify the October 5 runtime.

## What I established

I found a missing production producer for fresh typed research proof in the retired Platform's standard daemon, an approval-before-sensing dependency, and a retained live-root test that demands Rates remain uncommissioned. Each has a concrete consumer. Their scopes differ: the first two belong to the broker path retired on July 23; the third is a historical candidate verifier still called by a root test. I did not find an always-false shared P&L field that I could prove gates the current BUY/SELL motor.

I also recovered exact Owner admissions that assignments stopped at confirmation and that completion claims preceded realistic workflow testing. The historical corrective messages explicitly moved qualitative investment judgments out of machine verdicts. These are observed engineering and workflow facts. I cannot infer a model-training cause from them, or assign source authorship to a particular agent from a configured Git author name.

## 1. A missing fresh-proof producer has a real conditional entry consumer

The retained standard `build_daemon()` constructs `TrustedResearchAuthority` with every new-proof capability unset. It has only `config` and `lane_factory` arguments, without a research-authority-provider injection argument. This is more than a false display field: the issuer raises before producing a receipt.

Exact source, `platform/src/portfolio_platform/gateway/daemon.py`, lines 1119–1124:

```python
        # Deliberately fail closed.  A future platform connector supplies an
        # independently authenticated source resolver.  A separate orchestrator
        # service supplies only a public-key verifier, never its private key.
        numeric_source_resolver=None,
        numeric_verifier=None,
        model_attestation_verifier=None,
```

The numeric issuer consumes those fields in `platform/src/portfolio_platform/trusted_research_authority.py`, lines 1276–1281:

```python
        resolver = self.numeric_source_resolver
        verifier = self.numeric_verifier
        if resolver is None or verifier is None:
            raise TrustedResearchAuthorityUnavailable(
                "trusted numeric resolver/verifier capability is unavailable"
            )
```

The model issuer consumes its unset verifier in the same file, lines 1363–1367:

```python
        verifier = self.model_attestation_verifier
        if verifier is None:
            raise TrustedResearchAuthorityUnavailable(
                "orchestrator model-attestation capability is unavailable"
            )
```

I traced the subsequent path rather than assuming that any missing research capability blocks trading:

| Stage | Exact retained source | Observable effect |
|---|---|---|
| Standard composition | `gateway/daemon.py:1119–1124` | No fresh numeric/model proof capability is supplied. |
| Numeric request | `gateway/service.py:2501` | The manager-facing numeric route calls `authority.ingest_numeric(...)`, which raises above. |
| Model request | `trusted_research_authority.py:1360–1367` | Issuance is a separate orchestrator capability and has no manager-authenticated HTTP route. |
| Entry proof validation | `gateway/service.py:2690`, `2733–2755` | `ENTER_LONG` resolves current typed receipts. Missing/unresolvable supplied receipts become `typed_trusted_receipt_invalid`. |
| Validation aggregation | `gateway/service.py:3684` | Those errors enter the order's validation report. |
| Actual order submission | `gateway/service.py:4615–4640` | An invalid report changes the intent to `REJECTED` before snapshot refresh and broker dispatch. |

The terminal consumer is exact `gateway/service.py`, lines 4629–4635:

```python
            if not report.valid:
                detail = ",".join(report.errors)
                sequence = self.store.transition_intent(
                    intent.intent_id,
                    IntentState.REJECTED,
                    rejection_code="authority_validation_failed",
                    detail=detail,
```

There is an essential qualification. `gateway/service.py`, lines 2688–2690, says:

```python
        if not typed_sources:
            return errors
        requires_current_approval = intent.operation is OrderOperation.ENTER_LONG
```

The shared service does not itself mandate those receipt types for every BUY. A manager-specific validator must establish that necessity. Existing properly sealed receipts can also resolve through `trusted_research_authority.py:1488–1524` without consulting the issuance capabilities. A separately commissioned composition could supply real capabilities and issue valid records into the same governed database/projection.

My supported conclusion is therefore narrow and concrete: **a new entry requiring newly generated typed numeric/model proof has no fresh producer through the checked-in standard daemon composition.** I do not claim every historical entry was unreachable. SELL/exit receipt resolution uses `resolve_historical_receipt` rather than the same current-entry approval path. Copying JSON or weakening a verifier would not repair this missing producer.

Origin: `git blame` attributes the quoted producer and issuer lines to commit `e72611e96cff548f0ba8396bbb16cdb750487530`, recorded author `Clayton Check`, timestamp `2026-07-21T23:11:06+08:00`, subject `Add trusted research authority contracts`. The inspected Platform HEAD was `55fcbee88e10af9b80d475e0ee65c88a2dc27d73`; the targeted files had no reported worktree modifications. Git identity does not prove which human or model wrote each line. `platform/README.md:3–9` and `platform/AGENTS.md:12` explicitly remove this path's current execution authority.

## 2. Semantic approval was required before the quote could be observed

I confirmed a sensory dependency rather than merely an order-preflight gate. The promoted-entry quote route calls `_validate_market_data_request_authority()` before adapter research (`gateway/service.py:2111–2115`). Its promoted branch reopens the promotion in `gateway/service.py:2318–2330`.

Exact predicate, `platform/src/portfolio_platform/promoted_entry_quote.py`, lines 270–279:

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

The existing test is exact evidence of the intended behavior. In `platform/tests/test_promoted_entry_quote.py:898`, it changes `explicit_executable_semantic_approval` to `False`, reconstructs the hashes, and then asserts the following at lines 909–913:

```python
    with pytest.raises(MarketDataEvidenceError, match="not explicitly executable"):
        service.submit_research_job(
            "deep_value", kind="market_data", request=request
        )
    assert adapter.research_calls == 0
```

I traced the motor connection too. The service revalidates a bound promoted-entry quote receipt at `gateway/service.py:3190–3197` and `3258–3268`, adds resulting errors at `3686`, and rejects the submitted intent through the terminal consumer above. This is an actual conditional entry control, not merely presentation text.

I call it **approval before sensing**, not a proven logically impossible cycle. The inspected source does not prove that semantic approval itself always requires this quote. Ordinary lifecycle entry quotes have another path (`gateway/service.py:2370–2376`). Nevertheless, this design can starve a manager of the current price needed to decide whether to promote a candidate. Identity-bound, non-executable sensing could avoid that dependency while preserving final execution controls.

Origin: the predicate is also attributed by `git blame` to `e72611e96cff548f0ba8396bbb16cdb750487530` on July 21. It is historical retired Platform code. I found no evidence that this file is the current Deep motor's selected implementation.

## 3. A root test demands that a commissioned manager remain absent

I found a retained historical verifier with a hard false success shape. Importantly, it does not simply report false regardless of truth: it first rejects positive commissioned state.

Exact `tools/verify_four_manager_authority.py`, lines 196–200:

```python
    rates_deployment = root / "deployments" / "native_tws" / "rates_credit"
    if (rates_deployment / "current.json").exists():
        raise FourManagerAuthorityError("rates candidate must remain non-selected")
    if (root / "runtime" / "managers" / "rates_credit" / "direct").exists():
        raise FourManagerAuthorityError("rates production runtime must remain absent")
```

Its successful report then emits `rates_selected=False` and `rates_runtime_exists=False` at lines 210–211. The actual consumer is `tests/test_four_manager_authority.py`, lines 16–23:

```python
def test_four_manager_registry_capital_and_isolation_are_exact() -> None:
    report = verify(ROOT)
    assert report["clients"] == [0, 1101, 1201, 1301, 1401, 2101, 2201, 2301, 2401]
    assert report["capital_equation_verified"] is True
    assert report["historical_authority_verified"] is True
    assert report["rates_selected"] is False
    assert report["rates_runtime_exists"] is False
    assert report["broker_mutations"] == 0
```

This test uses the actual workspace root, not an isolated candidate fixture. For any root with a Rates selected pointer or production runtime, its expected success is unreachable; earlier authority checks could fail first, but success still cannot satisfy the later absence predicates. I did not inspect present runtime state or run the test. The September 14 health documentation separately records an already selected and active Rates runtime. Applying this retained test to that documented state would reject commissioned existence.

I classify this as a **fossilized candidate-only acceptance condition attached to the live-root test surface**. I do not classify it as a direct BUY/SELL motor gate. The September lean-design inventory already says to archive the root historical commissioning chain's operational role (`docs/STACK_LEAN_DESIGN_20260908.md:163`). If an operator nevertheless insists on this generic all-green test for current commissioning, it creates an engineering liveness barrier. I have not established that such a demand blocked a particular current order.

A similar retained initial-state consumer, `tools/build_reconciliation_evidence.py:355–421`, demands zero owned positions, zero manager executions and full original cash during commissioning. Its caller at `644–650` validates the observed report. Those requirements were coherent for the original empty-sleeve commissioning proof; they are incompatible with treating it as a universal mature-portfolio readiness test. I did not relabel historical successful evidence as evidence for today's portfolios.

Authorship/release attribution: the workspace root is not a Git repository, so I cannot supply a per-line Git author for these root files. Their use is a retained historical commissioning/test contract; I have no proof of their inclusion in a selected current manager motor.

## 4. I could not establish the proposed always-false shared P&L gate

I searched the named shared source, tools and tests for P&L/readiness producer-consumer patterns, then read the concrete producer. The retired Platform's `manager_projection.py:2805–2814` computes a conditional result:

```python
        net_complete = market_complete and all(
            item["commission"] is not None
            and item["commission_currency"] == "USD"
            and item["executed_at"] is not None
            and bool(item["lot_allocations"])
            and (item["side"] != "SELL" or item["reservation_id"] is not None)
            for item in fills
        )
        if not net_complete:
            blockers.add("projection_net_pnl_unavailable")
```

This can be true; it is not an unconditional false constant. A search of the retained gateway consumer modules and projection-artifact module did not establish a direct order rejection based on this blocker. A manager validator outside this shared scope could consume it and requires its own trace. Missing commission/lot provenance can also be a valid incompleteness reason, so changing the field to `True` would not itself be a justified fix.

I excluded two apparent false positives: daemon readiness resets `False` before refreshing and restores positive readiness after success (`gateway/daemon.py:822`, `841`); `cutover_acceptance.py:6866` emits `overall_ready=False` in an exception result. Those are not permanent producer defects.

## Exact task excerpts I used

I obtained these from the supported `read_thread` results already paged in my first review. I preserved assistant text verbatim below. A turn-start timestamp identifies the turn; it is not asserted to be the exact message-send timestamp. Messages delivered as `userMessage` delegations are identified separately rather than presented as direct human quotations or assistant admissions.

**Owner completion failure.** Task `01a07f36-bfde-7fc1-adf4-d827cb73601c`, exact title `Trading Stack Owner`; turn `01a0805c-da54-76f1-b157-a75fbd713495`, started `2026-09-08T09:32:44.000Z`; assistant item `msg_0f9807cc049611be016aa018e92df887d091cb457b87811639`, phase `final_answer`:

> You were right: my earlier assignments stopped at requirements confirmation. I corrected that and followed all four builds through installation and Manager acceptance.

The immediately earlier assistant completion in turn `01a08050-e97e-7413-a037-7c954ccd3ce0`, started `2026-09-08T09:19:41.000Z`, item `msg_0f9807cc049611be016a9fd602534087d08c1367b9b3f61955`, phase `final_answer`, ended:

> Requirements alignment is complete; implementation has not started.

The earlier turn was explicitly a confirmation request. The later admission matters because the broader authorized building effort remained incomplete until the principal's next intervention; I do not claim every confirmation-only reply is wrong.

**Realistic workflow acceptance weakness.** Same Owner task; turn `01a084df-7788-7cf2-98ec-025e410bc3db`, started `2026-09-09T06:33:52.000Z`; assistant item `msg_0f9807cc049611be016aa11199fa8487d08b7614246c5419d1`, phase `final_answer`:

> Feedback was candid: support improved after resumption, but completion claims had sometimes preceded realistic workflow testing and installed acceptance.

The exact corresponding saved report identifies the Rates defect at `docs/STACK_FULFILLMENT_AND_SUPPORT_20260909.md:48–52`:

> That is documented ordinary-path ambiguity; a mandatory duplicate in the motor
> has not been proved. Subsequent public composition using a real parsed
> ManagerDecision exposed an AttributeError: the materializer read an invented
> object attribute instead of the existing sealed payload. A simplified old test
> fixture had masked it. Manager preserved and adopted the bounded defect repair;

That block is documentary source text, not a task-message quotation. I did not claim its defect remains installed; the saved report states correction and installed acceptance followed.

**Qualitative gate removal after the over-engineering correction.** Task `019fa308-48ce-72b1-bc70-bcb3f9877fb4`, exact title `Trading Stack Owner (Retired)`; turn `019fa798-831a-7440-8e0a-725372236089`, started `2026-07-28T07:20:17.000Z`; assistant item `item-634`, phase `final_answer`:

```text
- Keep scores, scenarios, exposure, and risk flags advisory only.
- Remove machine verdicts on catalysts, fundamentals, thesis quality, funding choice, qualitative overlap, and exit-lot selection.
- Enforce numeric caps only when explicitly commissioned; otherwise report `UNRESOLVED`.
```

Its closing paragraph was:

> This scope was sent directly to the AI/Healthcare manager. Existing remediation remains unpublished in the isolated worktree.

The same turn contains manager-delivered `userMessage` item `item-630`, source task `019fa312-878d-74a0-9b74-762c747e1e00`, whose input begins exactly:

> Principal correctly flags over-engineering risk. Pause feature expansion and do not publish/cut over yet. Reframe the candidate as lean on-demand decision support, not an autonomous strategy/rules engine.

I identify this as the manager's report of the principal correction, not an independently retrieved direct principal quotation. The initial eight-gate request in the turn was also manager-delivered. Responsibility for the broad initial design was shared; the later assistant explicitly accepted removing qualitative machine verdicts.

## Source identities for the quoted code

These SHA-256 values cover the complete source bytes I inspected, not just a reconstructed excerpt. Code line ranges above refer to those bytes. Paths are relative to the project root.

| Source path | SHA-256 |
|---|---|
| `platform/src/portfolio_platform/gateway/daemon.py` | `45f3e6ea83291504f196de43697de50b72b984dcc978916f5a3324441b9dc843` |
| `platform/src/portfolio_platform/trusted_research_authority.py` | `9d4872bb65e9ea478b73453c6a5dfcd0c8aa18aefb53107904d6cfbc11661e14` |
| `platform/src/portfolio_platform/gateway/service.py` | `a2b7ac5240fa7f635e1cf1ab1a43c3f1550b203f60950ffaef1895d55f152d5e` |
| `platform/src/portfolio_platform/promoted_entry_quote.py` | `07e72e147d142e9babca7cb0c091b9ed37b38fc028a37dee2d5c295e7d562924` |
| `platform/tests/test_promoted_entry_quote.py` | `219f681134a8ccd95ec1d842809502437e3eb7216028cc64e2df7f97cee35ab0` |
| `tools/verify_four_manager_authority.py` | `54081f74e917eb898fe6f39c23f099f87db161b36be31587325c768c08789319` |
| `tests/test_four_manager_authority.py` | `e9ac83679ad6c58cd7832342fe0ecb710ba4c68d16e86c914b6e9f6ba380469a` |
| `tools/build_reconciliation_evidence.py` | `c939bcdb4208bfa23fd67c7d9f632af6fd22e4da2b8393e56570d6b637c3914a` |
| `platform/src/portfolio_platform/manager_projection.py` | `70671cbbcf732d9097ecba4cf36c165962c5716b1f348219cf74b74e77d1a772` |
| `docs/STACK_FULFILLMENT_AND_SUPPORT_20260909.md` | `42e702eb89686e68b9e852be74e6a7cac6e5c595c73390dcc7998d4f8931ea55` |

## What I would require from a repair

I would require a control-by-control inventory of the producer, caller, effective scope and attainable successful public workflow. A new-proof requirement needs a real commissioned issuance path. Read-only sensing should not inherit qualitative order approval merely by sharing a schema. Candidate-only tests should use isolated candidate fixtures and remain distinct from current mature-state acceptance. A repaired motor needs positive BUY/SELL/lifecycle cases and exact genuine refusal cases, with missing analytics kept separate unless the manager expressly commissioned them as execution policy.

I would preserve ownership, capital, idempotency, uncertainty, quote integrity and order-lifecycle protections. I would not substitute a forced `True` readiness field for evidence. This investigation is complete; broker execution is **NOT_REQUESTED** and I issue no manager investment disposition or production change.
