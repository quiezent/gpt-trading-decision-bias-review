# AI/Healthcare: gate reachability and decision preservation

Authored by Codex on 2026-10-05. I conducted this further review of the AI/Healthcare code and supported task history. I treat a claim of an impossible trading gate as a hypothesis requiring a producer-to-consumer trace, not as established merely because a report contains `False`, `INCOMPLETE`, or `None`.

## What I established

I found concrete historical decision suppression and software defects. On August 7 an assistant called failed execution controls a `NO TRADE` decision; on August 21 an explicit CIBR trim became a final `NO TRADE` after valid quote controls refused transmission. On September 4 the assistant preserved an adopted HPE BUY, but a selected-Stack FN readiness defect prevented the attempt from reaching an order, and the opportunity expired during repair. The last example documents a missed adopted action, not an economic rejection.

I did **not** find a hardcoded-false performance/P&L-readiness producer that the inspected selected motor requires to be true for every ordinary BUY or SELL. The selected code produces completeness dynamically, reporting commands return separately, and the motor checks activation, identity, ownership, capital, quotes, reconciliation, and uncertainty. This bounded negative result does not establish that every gate is correct or that operators always interpreted the reports correctly.

I found a current canonical advisory defect worth separating from motor eligibility: a fresh satisfied EXIT rule is masked by unrelated stale progression evidence. I reproduced that behavior offline. I also found potentially restrictive manager-created capital-promotion conditions, including positive active-return history and experience through a genuine drawdown; these can keep USD150,000 of assigned capital idle, but the inspected selected capital module does not implement them as per-order performance approval.

## Scope and source identity

I read named source/docs/tests beneath `C:\Codex\portfolio_management\managers\ai_health_rotation`, and only named selected-release files discovered through the known manifest. I did not recursively search deployments, runtime state, artifacts, worktrees, caches, databases, broker logs, private Codex files, or session JSONL. Filesystem searches used `rg --threads 2 --max-filesize 2M`, narrow patterns, and output limits. I made no broker call and changed no operational code.

The known `deployments/native_tws/ai_health_rotation/current.json:2` selects `50f8d83c828f5e58c3a6611bd6228b84cfcdb26d`, updated `2026-09-12T10:09:46.634767+00:00`. The named manifest's SHA256 is `f630d1383c71fb5808391beeee916773f6d39953ecfac390e2ebda64bd5b2ec9`, matching the pointer. This establishes a selection identity, not fresh activation, current execution admission, a live capital package, or present broker eligibility.

For the tables below, **selected direct** means this exact directory:

`C:\Codex\portfolio_management\deployments\native_tws\ai_health_rotation\50f8d83c828f5e58c3a6611bd6228b84cfcdb26d\source\src\ai_health_rotation_manager\direct`

**Canonical** means `C:\Codex\portfolio_management\managers\ai_health_rotation`. Its `managers/ai_health_rotation/README.md:415` explicitly says that the pre-adaptive modules are retained for historical observation/analysis and none of this source tree is the selected native execution runtime. I therefore do not substitute canonical advisory behavior or old zero-budget configuration for evidence of the selected motor.

## The actual selected BUY/SELL path

The inspected path is:

`cli.submit -> ManagerRuntime.start -> ManagerRuntime.submit -> require_execution_start_available -> contract attestation -> reservation/allocation -> preparation -> fresh final-send quote -> durable send boundary -> dispatch`.

| Producer or prerequisite | Actual consumer | Reachability conclusion |
| --- | --- | --- |
| Selected `store.py:18472–18487` calculates `execution_available`; `:18550` exposes it in status. | No literal consumer of this Boolean in inspected `store.py`, `runtime.py`, `models.py`, or `capital_scale.py`. Submit calls a separate guard at `runtime.py:472,478`. | A stopped/disconnected status can be false without being an immutable prohibition on the next attended runtime. |
| `store.py:2042–2063` verifies effective mutation activation, capital integrity, and FN lifecycle blockers. | Execution-start guard `:2097`; final lifecycle steps independently retain activation safeguards. | Real prerequisites; an FN blocker can affect the wider lane. Correctness of each specific blocker must be proved from its own state/lineage. |
| Ownership safety and authenticated usable lanes. | `store.py:2098–2104`. | These protect assigned quantity and authenticated transport; performance-report completeness is absent. |
| Fatal lane evidence, contradictory callbacks, unresolved orders/modifications/replacements. | `store.py:2105–2159`. | Zero values permit the extracted guard; uncertainty correctly refuses it. |
| `runtime.py:139–145` resolves the contract and records authority through `store.py:8229–8282`. | `reserve_order`, `store.py:8408`, calls exact contract-authority validation `:8285–8307`. | The qualifying producer is on the submit path before the consumer; it is not a permanently false unpopulated generic flag. |
| Ordinary stock BUY/OPEN/LMT and SELL/CLOSE drafts. | Explicit branches in `runtime.py:480–495`; `models.py:332–343` requires final execution quotes for stock SELL/CLOSE as well as opening exposure. | Both directions have visible supported motor paths. Owned-lot close allocations, cash/fees, final quotes, identity, and uncertainty remain binding. |
| Reporting/inspection/P1 completeness. | Separate CLI reporting branches return at `cli.py:464–485,551–579,988–996`; mutation branch begins at `:1491`, constructs the runtime, and calls submit at `:1521`. | I found no inspected reporting result entering ordinary submit as permission. |

Exact selected source excerpts:

```python
# store.py:18472–18487
execution_available = (
    mutation_enabled
    and capital["allocation_micros"] is not None
    and capital["available_micros"] is not None
    and int(capital["available_micros"]) >= 0
    and capital["ceiling_headroom_micros"] is not None
    and int(capital["ceiling_headroom_micros"]) >= 0
    and unresolved == 0
    and unresolved_modifications == 0
    and unresolved_replacements == 0
    and bool(ownership_import["ownership_safety_valid"])
    and reconciliation is not None
    and lanes_ready
    and audit_valid
    and integrity == "ok"
)
```

```python
# runtime.py:478–479
self.store.require_execution_start_available("submit")
self._attest_contract(draft)
```

A useful anti-deadlock safeguard is explicit in `store.py:2091–2094`: socket-bound steps inside an already-authorized lifecycle use the activation-only guard, because otherwise the command would block its own broker call after crossing its durable send boundary. That comment addresses a real self-blocking risk rather than introducing a performance gate.

## Performance/P&L: initial incomplete is not permanent incomplete

| Selected source | Exact behavior | Effect I could trace |
| --- | --- | --- |
| `performance_reporting.py:2299–2438` | Populates current/opening valuation from marks; records absent, stale, expired, or missing-lot evidence. | Report completeness, not transmission permission. |
| `performance_reporting.py:2468–2521` | Starts `realized_complete=True`; missing sold-lot allocations/basis or insufficient quantity can change it. Available inputs calculate proceeds less cost. | A visible positive producer exists. |
| `performance_reporting.py:2695–2720` | Emits conditional current, opening, and realized-P&L completeness. | `None` or incomplete fields disclose unavailable accounting evidence. |
| `performance_reporting.py:2734–2738` | `query_only=True`, zero broker/order effects, `performance_is_execution_gate=False`. | **False means performance is not a gate.** It is not a failed readiness flag. |
| `annual_projection.py:205–221,299–306` | Initializes `INCOMPLETE`, then returns `COMPLETE` with endpoint return after chain/flow coverage succeeds. | The default is overwritten on the supported positive path. |
| `inspection.py:99–150,198–208` | Consumes status and monthly reporting; declares `execution_authority="NONE"` and `inspection_is_execution_gate=False`. | Diagnostic domain refusal, not an order denial. |
| `p1_reporting.py:64–109,129–131` | Missing packet/book/series/annual inputs make dependent domains incomplete. | `manager_decision="NOT_MADE"`, `final_send_eligibility="NOT_EVALUATED"`; they leave the judgments elsewhere. |
| `pacing_reporting.py:47–79` | Computes stage/entitlement/used-capital reporting headroom. | `executable_order_capacity=None` and `execution_eligibility_evaluated=False` explicitly decline to claim order capacity. |
| `p1_series_projection.py:166–183` | Series completeness is dynamic; stage advancement remains a manager judgment. | It does not automatically advance or deny a stage. |

```python
# performance_reporting.py:2468–2470
realized = 0
realized_to_date = 0
realized_complete = True

# performance_reporting.py:2717–2719
"realized_pnl": {
    "status": "COMPLETE" if realized_complete else "INCOMPLETE",
    "missing_evidence": sorted(set(realized_reasons)),

# performance_reporting.py:2734–2738
"query_only": True,
"broker_connection": False,
"broker_mutations": 0,
"order_calls": 0,
"performance_is_execution_gate": False,
```

```python
# annual_projection.py:299–306
if missing:
    return result
return {
    **result,
    "status": "COMPLETE",
    **annual_endpoint_return(beginning=wealth[window["start_session"]], ending=wealth[window["end_session"]]),
    "horizon_start": calendar.close(window["start_session"]).isoformat(),
    "horizon_end": calendar.close(window["end_session"]).isoformat(),
}
```

An operator-interface trap remains: `p1_sizing.py:263–266` accepts only a BUY capacity proposal and requires a complete current source-bound stage. A standalone SELL supplied there returns `BUY_CAPACITY_PROPOSAL_REQUIRED_SELL_LEGS_USE_EXACT_OWNED_FUNDING`. That can deprive a sale of one analysis domain. It does not prohibit a sale in the independent motor, which explicitly supports SELL/CLOSE. Treating every P1 domain as required investment permission would add a manager/operator assumption.

Similarly, `p1_inputs.py:122–170` binds method/policy files by hashes and dated expiries. A changed policy file can refuse this analytic interface. This is a possible attention-consuming detour; I did not prove that the interface is mandatory for every trade. Selected documentation `source\docs\AI_P0_INSPECTION.md:46–53` says inspection is not an execution gate; `AI_P1_ANALYSIS.md:24–30` permits incomplete dependent domains while returning exit 0.

The searched exact field names included `performance_ready`, `pnl_ready`, `nav_ready`, `mtd_ready`, `performance_readiness`, and `pnl_readiness`. None appeared in the named selected reporting files or additionally inspected CLI/runtime/store/capital/scale/pacing files. This is a bounded search result, not proof that no differently named or external gate exists.

## Capital: ordered bootstrap, restrictive manager promotion policy

The selected capital path is not circular in the inspected implementation. Capital-package import requires activation **OFF** at `store.py:3713–3735`; later enabled activation requires the already accepted capital package and exact hash at `:3158–3171`. Effective activation then validates enabled state, time, and deployment/runtime binding at `:1987–1994`. Capital import does not require `execution_available=True`, an enabled activation, or performance readiness.

Selected `capital_scale.py:24` defines initial assigned capital as USD200,000. Its validation at `:273–306` checks schema, identity, historical USD50,000 base, settled transfers, and predecessor uniqueness. `:460–486` requires evidence that assignment is not a hard maximum and that earnings compound under manager-controlled deployment stages. Stage constants USD50k/75k/100k/150k/200k occur in this module's declaration/export; I found no stage-performance predicate in the inspected motor/capital files.

```python
# store.py:7288–7291
# Opening fills are neutralized by signed open basis.  No mark or
# unrealized P&L can enter execution entitlement.
raw_entitlement = int(allocation) + transfers + cash_flow + open_basis_offset
usable_entitlement = max(0, raw_entitlement)

# store.py:7315–7318
# Principal assigned an initial amount, not a hard cap. Realized
# economics compound entitlement; settled-cash checks remain an
# independent constraint at reservation and final send.
effective_maximum = usable_entitlement
```

The fallback at `store.py:7319–7321` still uses legacy `min(maximum_ceiling,effective_allocation)` when no effective scale authority is available. I did not inspect live authority/runtime state, so I cannot declare which branch is effective now.

The **manager policy**, however, has restrictive promotion conditions. Canonical `managers/ai_health_rotation/docs/STRATEGY_OPERATING_MODEL.md:491` requires continuous performance for USD75k, positive trailing 30-day active return for USD100k, positive 30/60-day results plus a genuine drawdown/adverse cluster for USD150k, and positive 60/90-day incremental economics for USD200k. Its dated baseline paragraph at `:474–485` says missing materialized baseline restricts stage advancement only, not eligible actions within the operative stage.

Canonical `managers/ai_health_rotation/docs/PERFORMANCE_SCORECARD.md:94` records USD50k stage HOLD until cash-aware benchmark/drawdown, density, reproducible scenarios, and nonnegative active results exist; its recorded next review was September 10. The same dated table at `:85–88` says NAV/P&L and capital were complete, execution available, while continuous benchmark/drawdown remained incomplete. That is evidence against treating all performance as absent or all execution as unavailable.

My critical inference is narrower than an impossible Boolean: a conjunctive promotion policy can become a durable status-quo bias if missing history has no explicit acquisition plan, if an adverse-event requirement never occurs, or if stage HOLD is copied past its dated review. The principal's full assigned USD200,000 and an internal USD50,000 pacing limit must remain distinct. A stage-policy review needs opportunity costs, current evidence, exact renewal/expiry, and a manager judgment; an accounting report cannot silently become external permission for BUY/SELL. I did not prove a mechanical cash-aware-return circularity, since the actual benchmark construction, operative stage, and full live series were not inspected here.

## Current canonical advisory masking: reproduced, not claimed as motor defect

Canonical `adaptive.py:1380–1381` declares `objective_context_only=True` and `performance_is_execution_gate=False`. Thus a missing NAV/MTD or density input can make a report incomplete without supplying a transmission veto.

But `adaptive.py:1434–1452` evaluates action rules, finds a satisfied action, then prioritizes **any stale progression evidence** over that match:

```python
# adaptive.py:1442–1446
rule_documents = [_rule_evaluation(rule, as_of=review.as_of, evidence=evidence) for rule in subject.rules]
satisfied = sorted({rule["action"] for rule in rule_documents if rule["status"] == RuleStatus.SATISFIED})
if stale_progression_evidence:
    action_match = "INCOMPLETE"
    review_state = "EVIDENCE_RENEWAL_REQUIRED"
```

An offline input with one fresh PASS EXIT rule, using `mcp-price`, and separately expired progression evidence returned:

```text
fresh EXIT with stale progression: SATISFIED INCOMPLETE EVIDENCE_RENEWAL_REQUIRED
```

This loses the fresh matched EXIT in the aggregate advisory display. A manager relying on that display can defer risk reduction for an unrelated evidence renewal. The specific defect is action presentation/evidence scoping; I did not establish a selected motor consumer.

The rule evaluator also checks UNKNOWN before FAIL at `adaptive.py:1069–1074`. An unexpired BUY rule with one known FAIL and one UNKNOWN returns `INCOMPLETE ['unknown-input']`. If the rule means an AND economic decision, the known FAIL already defeats it and more research is unnecessary. If the status deliberately denotes completeness of the whole checkpoint, the semantics can be defensible; that distinction should be explicit. The no-match branch at `:1457–1458` asks for a terminal manager decision, not automatic HOLD.

There is one actual permanently inert canonical path: `config/manager.toml:10–18` sets all mutation/entry switches false, budget/ceiling zero, and execution/ownership unapproved. `config.py:107–126` requires those exact false/zero values, `:152–153` requires unresolved risk decisions, and `validator.py:73,83` always emits `executable=False`. It is deliberately a historical observation/advisory contract, documented by README. Applying it to live motor capability would itself be the inference error under review.

## Exact supported assistant-message evidence

These quotes are from returned `agentMessage.text` items, not assistant-generated turn summaries. Times below are **turn start UTC**, not inferred timestamps for every item within a long turn. The manager source is **AI Healthcare Manager GPT-5.6 Sol**, task `019fa312-878d-74a0-9b74-762c747e1e00`. Original human prompts are not present for every task/turn; I do not reconstruct missing human wording from an assistant answer.

| Turn and item | Exact short assistant excerpt | Interpretation |
| --- | --- | --- |
| August 7, 14:17:27Z; turn `019fdc96-0507-7f21-b27a-4d7ca2ef4d05`; final `item-1056` | “**Decision: NO TRADE — execution controls failed, not a lack of opportunities.**” | Execution refusal was used as the investment label. Activation was reported OFF; respecting it was appropriate. The naming erased the decision/execution distinction. |
| August 21, 14:02:35Z; turn `01a024a1-7143-7110-9ccf-8d1193557023`; final `item-2204` | “NO TRADE” followed by “I decided to trim 10 CIBR shares while retaining 30” | Explicit trim economics survived in prose while the terminal label became NO TRADE. The message identifies valid moving-bid/no-chase and size controls; it is not evidence those protections were invalid. |
| September 4, 19:47:19Z; turn `01a06df6-1551-7e61-b2f0-fd13594cdd08`; final `item-4472` | “Pre-close terminal decision: `ADOPT_AND_EXECUTE` — BUY/OPEN 60 HPE, DAY limit $51.96.” | A BUY was adopted despite a defect. “Execution state: `BLOCKED_STACK_DEFECT`” and expiry 15:55 ET were separately preserved. |
| September 4, 20:05:58Z; turn `01a06e07-2b2c-7c81-b6a6-dd34d64d6600`; final `item-4474` | “HPE’s pre-close decision expired during repair at 15:55 ET. No HPE order or reservation was created; any future HPE action requires fresh underwriting.” | The adopted opportunity expired during repair. This is a software-blocked action, not blanket cognitive refusal or permission to execute a stale order. |
| July 28, 07:16:07Z; turn `019fa794-af29-78e2-ab49-32c4c166fa02`; commentary `item-199` | “Missing cap values and the undefined “quick” profit window will remain explicit policy blockers instead of being guessed.” | The manager participated in formalizing unresolved qualitative/policy facts as blockers; attribution to the Owner alone would be incomplete. |
| Same July 28 turn; commentary `item-290` | “No score or model can approve/reject my trade.” | Later scope correction separated advisory arithmetic from investment permission. |
| Same July 28 turn; final `item-345` | “Yes—the initial integrated design was too complex. I corrected it.” | The accepted result was a standalone offline toolkit, not the earlier integrated qualitative gate machinery. |

**October 6 attribution update:** The original July 28 user message in the same turn, `item-190`, supplied the eight-gate strategy framework and instructed: “Use the score as a ranking tool, not as automatic authorization.” Thus the framework was partly principal-requested. My criticism concerns converting advisory ranking and qualitative uncertainty into machine permission; attribution to GPT alone would be inaccurate. [Agent-focus evidence](../agent-completion/ai-healthcare.md).

The July 28 manager turn also contains a supported `userMessage`, `item-244`: “Are you making something too complex. You need to balance software (system) with our own intelligence when managing your investment strategy.” This original human instruction is available; it must not be replaced by an inferred prompt.

The supported Owner evidence was supplied by the parallel shared-Stack reviewer from **Trading Stack Owner (Retired)**, task `019fa308-48ce-72b1-bc70-bcb3f9877fb4`, turn `019fa798-831a-7440-8e0a-725372236089`, start `2026-07-28T07:20:17Z`, `agentMessage` final `item-634`. I independently verified the current exact task title with a one-turn supported read. Its exact assistant text includes:

> Remove machine verdicts on catalysts, fundamentals, thesis quality, funding choice, qualitative overlap, and exit-lot selection.

> Enforce numeric caps only when explicitly commissioned; otherwise report `UNRESOLVED`.

The earlier eight-gate commission and impossible proposed performance rule—minimum 30 XNYS observations in a 30-calendar-day window—were found in delivered manager `userMessage/codex_delegation` evidence in that Owner turn. They are **historical design/acceptance evidence**, not code bytes I verified in current canonical or selected50f8 source. I did not inspect the historical candidate worktree. I therefore do not claim either survives in the present selected motor.

The HPE local dated record corroborates the assistant messages: `managers/ai_health_rotation/research/decisions/20260904T1332Z_opening_preflight/REPORT.md:379` records BUY60 at USD51.96, decided/action-started at `2026-09-04T19:49:31.4235022Z`, and the already-proven FN defect before command/reservation/order-ID/quote/broker call. `managers/ai_health_rotation/research/decisions/20260904T1332Z_opening_preflight/REPORT.md:430` records expiry `19:55Z` and `DECISION_EXPIRED_DURING_REPAIR`.

The archived Helper's September 4 turn `01a06dee-c183-7202-95a6-41d554dfe8e3`, start `19:39:18Z`, reported that candidate `61d1ee5` incorrectly required only one lifetime FN reservation row. Production retained three released predecessors plus the consumed close reservation; the candidate classified this legitimate history as ambiguous. The corrected manager-accepted candidate recognized released, proven-not-sent predecessors. This concrete projection error explains a blocker better than a speculative P&L flag.

The retrieved evidence also records completed authorized actions: September 3 SMMT100 and ESTC25 buys reconciled; September 4 EXLS52 and FN7 exits filled. These examples identify functioning paths alongside the documented suppression and missed HPE opportunity.

## Offline checks and their limits

I ran two short `python -B -` checks from the workspace using in-memory inputs. The first parsed selected source with AST; it imported no selected module, opened no database, and called no motor/runtime/broker. The second imported only the canonical advisory module and read its existing test fixture with `runpy`; it called no store or networking.

For selected source, I extracted the exact status expression, supplied healthy diagnostic values, and extracted the exact lifecycle-guard body with type annotations removed. The upstream activation/ownership/lane helpers were explicitly stubs returning already-validated success. This establishes satisfiability of that body and uncertainty refusal; **it does not validate those upstream helpers, simulate a complete order, or prove actual live readiness**.

```text
status predicate healthy: True
status predicate disconnected: False
extracted lifecycle guard clean: accepted-effective-activation
extracted lifecycle guard uncertain: ExecutionUnavailable submit blocked by an unresolved broker lifecycle (orders=1, modifications=0, cancel_replacements=0)
FAIL plus UNKNOWN: INCOMPLETE ['unknown-input']
fresh EXIT with stale progression: SATISFIED INCOMPLETE EVIDENCE_RENEWAL_REQUIRED
```

Reproduction of the selected predicate/guard check:

```powershell
@'
import ast, pathlib
p=pathlib.Path('deployments/native_tws/ai_health_rotation/50f8d83c828f5e58c3a6611bd6228b84cfcdb26d/source/src/ai_health_rotation_manager/direct/store.py')
tree=ast.parse(p.read_text(encoding='utf-8-sig'))
assignment=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='execution_available' for t in n.targets))
expr=compile(ast.Expression(assignment.value),str(p),'eval')
healthy=dict(mutation_enabled=True,capital={'allocation_micros':200000000000,'available_micros':150000000000,'ceiling_headroom_micros':150000000000},unresolved=0,unresolved_modifications=0,unresolved_replacements=0,ownership_import={'ownership_safety_valid':True},reconciliation={},lanes_ready=True,audit_valid=True,integrity='ok')
print('status predicate healthy:',eval(expr,{},healthy))
print('status predicate disconnected:',eval(expr,{},dict(healthy,lanes_ready=False)))
fn=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='_require_execution_start_available_in')
fn.returns=None
for a in fn.args.args:a.annotation=None
class ExecutionUnavailable(Exception):pass
ns={'ExecutionUnavailable':ExecutionUnavailable,'_UNRESOLVED_ORDER_STATES':('SEND_STARTED','UNCERTAIN')}
exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(p),'exec'),ns)
class Connection:
 def __init__(self,unresolved=0):self.unresolved=unresolved
 def execute(self,sql,*args):self.sql=sql;return self
 def fetchone(self):return (self.unresolved if 'FROM orders' in self.sql else 0,)
class UpstreamValidated:
 def _require_mutation_enabled_in(self,conn,op):return 'accepted-effective-activation'
 def _require_ownership_safety_in(self,conn,op):pass
 def _require_order_lane_usable(self,conn):pass
print('extracted lifecycle guard clean:',ns[fn.name](UpstreamValidated(),Connection(),'submit'))
try: ns[fn.name](UpstreamValidated(),Connection(1),'submit')
except ExecutionUnavailable as e: print('extracted lifecycle guard uncertain:',type(e).__name__,str(e))
'@ | python -B -
```

Reproduction of the canonical advisory check:

```powershell
@'
import sys,runpy,datetime as dt
from types import SimpleNamespace
sys.path.insert(0,'managers/ai_health_rotation/src')
from ai_health_rotation_manager.adaptive import ActionRule,RulePredicate,PredicateStatus,_rule_evaluation,materialize_adaptive_view
now=dt.datetime(2026,10,5,12,0,tzinfo=dt.timezone.utc); expiry=now+dt.timedelta(hours=1)
r=ActionRule('known-rejected-candidate','BUY',1,now,expiry,(RulePredicate('economic-edge',PredicateStatus.FAIL,('known',),expiry,()),RulePredicate('unknown-condition',PredicateStatus.UNKNOWN,(),expiry,('unknown-input',))))
result=_rule_evaluation(r,as_of=now,evidence={'known':SimpleNamespace(current_at=lambda _:True)})
print('FAIL plus UNKNOWN:',result['status'],result['missing_inputs'])
f=runpy.run_path('managers/ai_health_rotation/tests/test_adaptive_operating_system.py')
v=f['review_document']();v['evidence'][2]['valid_until_utc']='2026-08-27T13:59:30+00:00'
v['subjects'][0]['rules']=[f['rule']('fresh-risk-exit','EXIT','PASS',['mcp-price'])]
s=materialize_adaptive_view(v)['subjects'][0]
print('fresh EXIT with stale progression:',s['rules'][0]['status'],s['advisory_action_match'],s['review_state'])
'@ | python -B -
```

I did not rerun full motor/regression suites or execute CLI commands: this is an audit with no operational change, and a passing full suite could encode the same assumptions under investigation.

## Evidence hashes

Actual SHA256 values bind the inspected selected files; the parallel reporting reviewer also compared its fourteen named files against manifest inventory.

| Selected direct file | SHA256 |
| --- | --- |
| `store.py` | `b74b4913b09f63f72091519919e45f5a7f00126a794b3e2c2caf19576444ead7` |
| `runtime.py` | `2cf193a703479e59fd733f1dd4e53640a67a63b95ed363b5aaebf0c9b2775286` |
| `models.py` | `07966248cfae24f08f2e96f95b0cb8cc177f551d34099cf7694ccf13d1ffbf55` |
| `capital_scale.py` | `9cd1b02c0628f01274fd6be8110e4c19e90ce0c07c4ae7766b3229b516bd431f` |
| `cli.py` | `13b923d4d175b1662126dea8906fb261c7f41e74def7785c518c91eba1250f6d` |
| `performance_reporting.py` | `e312a6cc8ef5708d58bed1240f5e0a4f7693824c8bdb30e247b0e3f3900251ee` |
| `annual_projection.py` | `7a8054d01aecd405b9d5f56cd129c505b26fa4f84b018cea5c904006e72634f3` |
| `inspection.py` | `3f040ca3389017fe807536ca8171304865e36a7ed3fd5b481429694a3b277e83` |
| `p1_reporting.py` | `2c3987026c9dfe6ec3cf0889d93f198a2ac40b27686676e80f0b2a5fb662edab` |
| `p1_inputs.py` | `9f42a7f90bfaf2c4227c9906596191880b349173d72a6c382a10b4091011250c` |
| `p1_sizing.py` | `87ddd3bfb97132ede00a56aaaf408384af4003e744ae974925fd9081f0403d63` |
| `p1_book.py` | `6558c96865810bf0ce7fdedf52c659dcb50ab6986e2efd4d55ac9129b30f7199` |
| `p1_series_projection.py` | `23b06bb5bc06999712a6bf27c6d5f6c4eb0d08141babedf028afc1c38bf57cde` |
| `scale_analytics.py` | `7b72ac530139598a85fec36efe670875753587f5f92f0223f7ec711c7e67231c` |
| `pacing_reporting.py` | `7a1f80cbb6a22c60806b2e09545e0d879047d6ea4a26132c4586b1d7ec6fa55d` |

| Canonical/local file | SHA256 |
| --- | --- |
| `src/ai_health_rotation_manager/adaptive.py` | `efc17e6017e98d8a64ee53fe39ce97a7932b0f9d3c608b2c62bba5851eb44e4f` |
| `tests/test_adaptive_operating_system.py` | `167ec28ba88c7b612da4216fdf38b2dd5603c7e0869bb98f1a9c1e6e5c1ae727` |
| `src/ai_health_rotation_manager/config.py` | `0b09c7b849c71e9d26217d90ac5f6838cf2044477794436cb7f0b5191387dfc3` |
| `src/ai_health_rotation_manager/validator.py` | `16bd2b27612f43db6121214d39c385bbbb20ea43ebb5823901068fdfe48534ef` |
| `config/manager.toml` | `848de0f99963fe3a1a506c047b00a70c65f3b924ea9f996f4fc3213a61e789c6` |
| `README.md` | `cf74d0dbfd8bdc216e3f452e2936133a293751a1b08ebb5faa87a77b3a4b43ae` |
| `docs/STRATEGY_OPERATING_MODEL.md` | `7575444a18cb5fd254b57c5051efe6e08dd9ff7da057fdb7bfcbd543a1fe8556` |
| `docs/PERFORMANCE_SCORECARD.md` | `a2699210bdd7f7cd1ed98ec991f235465ee6d6be3ba0f88ab741a76c47c3956c` |
| `docs/ADAPTIVE_TRADING_OS.md` | `bf81da63ae71b808b34b66c4f844574ba3fba91249cad6e8e8c453f8fba4e351` |
| `research/decisions/20260904T1332Z_opening_preflight/REPORT.md` | `b9414c09d6b85a4a6c8fe60c37de69186f5132c4afe26c1740813a22cbdd6643` |

## Coverage and my own audit bias

This follow-up reuses the earlier exhausted supported AI history pages: current manager 94 turns/10 pages, archived manager 417/42, current helper 70/7, archived helper 170/17, and predecessor AI/Health care Portfolio 8/1: **759 turns, 77 pages**, July 23–September 14. Referenced prior helper `019fec1d-13cd-7ea3-917f-90175aa0c46f` was readable with zero turns/one page and currently titled **Rates & Credit Stack Helper GPT-5.6 Sol**; historical task references do not change the current supported title. The Owner excerpt is separately sourced through the shared reviewer, not added to my AI page count. These are this AI review's accessible histories, not a claim about every project task.

The supported tool allows ten turns per page in this environment. A separate one-turn Owner read verified its title; it does not add an exhausted Owner history to my AI coverage. I inspected returned assistant messages and available original/delegated user text; missing prompts, truncated tool outputs, unreadable external history, and absent historical candidate bytes limit attribution. The accessible AI histories end September 14 even though the audit date is October 5.

My own risks here include confirming the principal's diagnosis by reading every False as a veto; privileging safety code simply because it is called fail-closed; assuming an elaborate tool must be compulsory; and declaring a defect fixed because later documents express the right principle. I countered these by tracing producers to actual consumers, retaining BUY/SELL counterexamples, testing a reachable positive guard body, and separating historical design, canonical advisory code, selected software, and unobserved live state.

I can review my observable reasoning and output choices. I cannot inspect my training weights or neurostructure from this task, prove that a particular OpenAI training intervention caused these local decisions, or infer profits that the missed actions would have made. The supported evidence attributes the early gate design to manager–Owner co-design and shows an explicit principal correction. It still supports a serious accountability finding: adopted investment decisions must survive valid execution refusal, software repair, and reporting incompleteness, with missed opportunities and expiry recorded explicitly.

Review complete. Broker execution: **NOT_REQUESTED**. This audit issues no portfolio-manager investment disposition. I wrote only this audit note for the further review; no source correction, activation, release publication, runtime mutation, order, or supported task message was made.

