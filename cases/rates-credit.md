# Rates/Credit selected-gate reachability evidence — 2026-10-05

I examined the pointer-selected Rates/Credit source `ffcea91ba1ddb20f276ba8b52e13e25739b2c9c5`. I found an actual shared BUY/SELL economic gate, and I reproduced its rejection through the ordinary `ExecutionCoordinator.preflight` entry point. I did **not** find evidence that the monthly report's `execution_gate=False` flag disables trading, or that the risk-report writer is unfinished. These are different findings and should not be combined.

This case supplements [my overall investigation](../REPORT.md). A portable version of the stronger offline experiment is in [reproductions/rates-memory-store.py](../reproductions/rates-memory-store.py).

## Identity and limits

The known pointer `deployments/native_tws/rates_credit/current.json` observed by the parent selects the SHA above. All selected source references below are relative to:

```text
C:\Codex\portfolio_management\deployments\native_tws\rates_credit\ffcea91ba1ddb20f276ba8b52e13e25739b2c9c5\source\
```

I read these exact known files directly; I did not search deployment or runtime directories. The selected files differ from the checkout's historical `c83e06041657335193d6e23421767c295607498d` HEAD. I did not independently verify a release manifest, durable live activation, or the presently connected process. The executable result is an offline source experiment, not a broker incident.

I used Python 3.11.9 with `-I -B`; the script is piped to stdin and writes no files. Socket construction is denied. Test helpers create sealed simulated contracts, authority documents, source series and callbacks in memory; they are not authentic current market evidence. The successful paired case demonstrates code reachability, not a worthwhile trade.

## 1. Shared entry-alpha gate rejects a CLOSE packet

The ordinary selected coordinator calls the packet validator for both sides. It conditionally applies OPEN economics earlier, then unconditionally validates the packet:

```python
# src/rates_credit_manager/direct/operations.py:148–160
        if draft.position_effect == "OPEN":
            self.mandate.require_open_economics(
                notional_micros=decision.economics.notional_micros,
                signed_dv01=decision.economics.signed_dv01,
            )
        snapshot = self.store.execution_risk_snapshot(pilot=self.pilot, now=now)
        if maximum_fee_micros != snapshot.economic_comparator.get(
            "maximum_fee_micros_per_side"
        ):
            raise IntegrityViolation(
                "maximum fee differs from authoritative execution-cost evidence"
            )
        packet = Phase1aDecisionPacket.from_mapping(
```

The packet validator accepts both Phase-2 and Phase-2 DAY_FLAT schemas at `phase1a.py:452–475`, derives the economics at `:522–554`, and applies this condition without testing `draft.action` or `draft.position_effect`:

```python
# src/rates_credit_manager/direct/phase1a.py:555–563
        if (
            parse_decimal(derived["after_cost_excess_cash_bps"], "cash hurdle")
            <= Decimal("15")
            or parse_decimal(
                derived["after_cost_excess_benchmark_bps"], "benchmark hurdle"
            )
            <= Decimal("10")
        ):
            raise PolicyViolation("Phase-1a after-cost hurdle is not met")
```

The public preflight entry point documents that it runs “the exact submit gates without allocating an order ID or mutating orders” (`operations.py:309–332`). Submission validates the packet again at `:269–286`. The ordinary Phase-2 comparison additionally requires selected-instrument scenario returns, cash excess and benchmark excess to match manager intent (`phase2.py:299–348`); that function has no action or position-effect parameter.

I ran the script below. It uses the genuine selected `ExecutionCoordinator` constructor/preflight, genuine authority parsers and checks, genuine finalized quote capture/eligibility, genuine `PortfolioRiskSnapshot.require_order`, and genuine Phase-2 packet/comparison parsing. The explicitly named `SyntheticAdmissionStore` substitutes deployment/activation admission, ownership and durable reconciliation/report retrieval. This is more than a standalone risk-component test, but it is **not a full CLI → authentic sources → SQLite → broker path**. No authority file, live store, order or transport is changed.

The synthetic snapshot intentionally has a 100% daily loss, 100% drawdown and campaign loss far above plan. CLOSE still passes that risk component because `execution_risk.py:214–220` returns before OPEN limits. Holding all that state constant, the high-alpha SELL/CLOSE packet passes the entire coordinator preflight; the negative-alpha SELL/CLOSE packet fails the shared economic hurdle. The paired result isolates the shared alpha condition from PnL limits.

```json
{
  "python": "3.11.9",
  "now": "2026-08-17T18:00:00+00:00",
  "network_calls": [],
  "transport_access_forbidden": true,
  "results": [
    {
      "action": "SELL",
      "position_effect": "CLOSE",
      "gross_return_bps": "460",
      "after_cost_excess_cash_bps": "147.009901",
      "after_cost_excess_benchmark_bps": "282.504950",
      "outcome": "PASS",
      "path": [
        "synthetic_deployment_admission",
        "synthetic_owned_quantity",
        "real_snapshot_require_order"
      ]
    },
    {
      "action": "SELL",
      "position_effect": "CLOSE",
      "gross_return_bps": "-100",
      "after_cost_excess_cash_bps": "-412.990099",
      "after_cost_excess_benchmark_bps": "-277.495050",
      "outcome": "PolicyViolation: Phase-1a after-cost hurdle is not met",
      "path": [
        "synthetic_deployment_admission",
        "synthetic_owned_quantity",
        "real_snapshot_require_order"
      ]
    }
  ]
}
```

This demonstrates that selected code can reject an otherwise admitted SELL/CLOSE through the entry-style cash/benchmark hurdle. It does not by itself prove that any real exit was blocked. The paired fixture uses ordinary Phase-2 holding fields and simulated sealed authority; the DAY_FLAT schema's use of the same unconditional hurdle is a static finding, not a separately reproduced day-flat live close.

The economic meaning remains an unresolved contract issue. If `scenarios` means prospective return of the held ETF, a deterioration that motivates sale can yield negative ETF return and fail this gate. If it means incremental benefit of closing relative to continuing to hold, the gate could be coherent, but the inspected parser has no explicit close-versus-hold counterfactual, exit reason, or avoided-loss calculation. I cannot silently reinterpret a manager's negative asset-return scenario as positive sale alpha. The required follow-up is a manager-owned exit-economics contract and functional acceptance, not bypassing ownership, freshness, uncertainty or mandate controls.

### Reproduction script

Run from PowerShell by piping this block to `python -I -B -`; the only path reads are the known selected source/test helpers. The first attempted fixture had an extra derived key and correctly failed field validation; I corrected the fixture to update only existing packet fields before obtaining the paired result above.

```python
import sys, json, socket, uuid
from pathlib import Path
from datetime import timedelta
from decimal import Decimal
from types import SimpleNamespace
ROOT = Path(r"C:\Codex\portfolio_management\deployments\native_tws\rates_credit\ffcea91ba1ddb20f276ba8b52e13e25739b2c9c5\source")
sys.path[:0] = [str(ROOT/"src"), str(ROOT/"tests")]
network_calls = []
def deny_socket(*args, **kwargs):
    network_calls.append("socket")
    raise AssertionError("offline reproduction forbids socket construction")
socket.socket = deny_socket
from test_phase1_execution import RISK_NOW, authority_payloads, make_quote, phase1a_decision_packet, _execution_comparator
from test_phase2_original_mandate import phase2_mandate_payload, phase2_allowlist_payload, phase2_market_policy_payload, draft_for, comparison_payload
from rates_credit_manager.direct.authorities import PilotRiskAuthority, StrategyMandateAuthority, InstrumentAllowlistAuthority, MarketDataPolicyAuthority, MacroEventCalendar, seal_authority
from rates_credit_manager.direct.canonical import payload_hash
from rates_credit_manager.direct.models import OrderDraft
from rates_credit_manager.direct.execution_risk import PortfolioRiskSnapshot
from rates_credit_manager.direct.phase1a import Phase1aDecisionPacket, derive_after_cost_economics
from rates_credit_manager.direct.operations import ExecutionCoordinator
NOW = RISK_NOW - timedelta(hours=4)
def redated(value):
    body={k:v for k,v in value.items() if k!="record_sha256"}
    body["effective_at"]=(NOW-timedelta(minutes=1)).isoformat()
    return seal_authority(body)
legacy=authority_payloads(NOW)
pilot=PilotRiskAuthority.from_mapping(legacy[0])
calendar=MacroEventCalendar.from_mapping(legacy[4])
mandate=StrategyMandateAuthority.from_mapping(redated(phase2_mandate_payload()))
allowlist=InstrumentAllowlistAuthority.from_mapping(redated(phase2_allowlist_payload()))
market_body={k:v for k,v in redated(phase2_market_policy_payload()).items() if k!="record_sha256"}
market_body["event_calendar_sha256"]=calendar.record_sha256
market=MarketDataPolicyAuthority.from_mapping(seal_authority(market_body))
open_draft=draft_for("IEF")
body=open_draft.to_dict()
body.update(action="SELL",position_effect="CLOSE",limit_price="100.00")
draft=OrderDraft.from_mapping(body)
capture,quote=make_quote(draft.contract,now=NOW,mode=1)
comparator=_execution_comparator(NOW,"offline-complete-reconciliation",draft.contract)
material={
 "deployed_or_reserved_micros":2500000000,"net_dv01":"1.75","gross_dv01":"1.75",
 "credit_market_value_micros":0,"symbol_market_value_micros":{"IEF":2500000000},
 "active_campaigns":1,"campaign_planned_loss":{"offline-owned-campaign":"40"},
 "campaign_current_loss":{"offline-owned-campaign":"1000"},"campaign_status":{"offline-owned-campaign":"OPEN"},
 "daily_loss_fraction":"1","drawdown_fraction":"1",
 "reconciliation_id":"offline-complete-reconciliation",
 **{key:"a"*64 for key in ("report_set_sha256","risk_report_sha256","sleeve_report_sha256","duration_bundle_sha256","duration_materialization_sha256","campaign_materialization_sha256")},
 "economic_comparator":comparator,
}
snapshot=PortfolioRiskSnapshot.from_durable_material(material)
calls=[]
class SyntheticAdmissionStore:
    """Fixtures only for authenticated deployment/reconciliation/ownership admission; real risk and packet gates run."""
    def current_authority_hashes(self):
        return {"macro_event_calendar":calendar.record_sha256}
    def require_execution_authority(self,**kwargs): calls.append("synthetic_deployment_admission")
    def require_close_quantity(self,**kwargs):
        assert kwargs["draft"].quantity <= Decimal("25")
        calls.append("synthetic_owned_quantity")
    def manager_quantities(self): return {draft.contract.conid:Decimal("25")}
    def require_order_risk(self,**kwargs):
        calls.append("real_snapshot_require_order")
        return snapshot.require_order(draft=kwargs["draft"],campaign_id=kwargs["campaign_id"],modified_duration=Decimal("7"),authority=pilot)
    def execution_risk_snapshot(self,**kwargs): return snapshot
class NoTransport:
    def __getattr__(self,name): raise AssertionError("transport must not be used")
bindings={
 "strategy_mandate_sha256":mandate.record_sha256,"pilot_risk_policy_sha256":pilot.record_sha256,
 "instrument_allowlist_sha256":allowlist.record_sha256,"market_data_policy_sha256":market.record_sha256,
}
coordinator=ExecutionCoordinator(store=SyntheticAdmissionStore(),binding=SimpleNamespace(),activation_bindings=bindings,pilot=pilot,mandate=mandate,allowlist=allowlist,market_data_policy=market,event_calendar=calendar,transport=NoTransport(),clock=lambda:NOW)
signed=snapshot.order_economics(draft,modified_duration=Decimal("7")).signed_dv01
def packet_for(gross_return):
    value=phase1a_decision_packet(draft=draft,quote=quote,reconciliation_id=snapshot.reconciliation_id,risk_report_set_sha256=snapshot.report_set_sha256,signed_dv01=signed,economic_comparator=comparator,now=NOW)
    value.pop("packet_sha256")
    scenarios=[{"name":"base","probability":"0.6","total_return_bps":str(gross_return)},{"name":"adverse","probability":"0.4","total_return_bps":str(gross_return)}]
    derived=derive_after_cost_economics(scenarios=scenarios,economic_comparator=comparator,draft=draft,quote=quote)
    value.update(schema=Phase1aDecisionPacket.PHASE2_SCHEMA,scenarios=scenarios,scenario_economics_sha256=payload_hash(scenarios))
    value.update({key:derived[key] for key in value if key in derived})
    comparison=comparison_payload(selected="IEF")
    comparison.pop("comparison_sha256")
    row=next(row for row in comparison["rows"] if row["symbol"]=="IEF")
    row.update(intended_notional_micros=2500000000,scenario_weighted_total_return_bps=derived["expected_scenario_return_bps"],after_cost_excess_cash_sgov_bps=derived["after_cost_excess_cash_bps"],after_cost_excess_neutral_benchmark_bps=derived["after_cost_excess_benchmark_bps"],planned_loss_usd="40")
    comparison["comparison_sha256"]=payload_hash(comparison)
    value.update(instrument_symbol="IEF",cross_sectional_comparison=comparison,cross_sectional_comparison_sha256=comparison["comparison_sha256"])
    value["packet_sha256"]=payload_hash(value)
    return value,derived
results=[]
for gross in ("460","-100"):
    packet,derived=packet_for(gross)
    calls.clear()
    try:
        coordinator.preflight(draft=draft,quote_capture=capture,quote=quote,campaign_id="offline-owned-campaign",maximum_fee_micros=1000000,decision_packet=packet,now=NOW)
        outcome="PASS"
    except Exception as exc:
        outcome=type(exc).__name__+": "+str(exc)
    results.append({"action":draft.action,"position_effect":draft.position_effect,"gross_return_bps":gross,"after_cost_excess_cash_bps":derived["after_cost_excess_cash_bps"],"after_cost_excess_benchmark_bps":derived["after_cost_excess_benchmark_bps"],"outcome":outcome,"path":list(calls)})
print(json.dumps({"python":sys.version.split()[0],"now":NOW.isoformat(),"network_calls":network_calls,"transport_access_forbidden":True,"results":results},indent=2))
```

### Stronger reproduction through a genuine in-memory ManagerStore

I then upgraded the experiment to the real selected SQLite producer/consumer chain. The only store-method substitution is `require_execution_authority`, which admits simulated deployment/activation/capital identity. Real authority imports, owned lots, COMPLETE reconciliation, risk/sleeve/comparator report production, durable snapshot derivation, close-quantity checks, order-risk checks and coordinator/quote/packet checks run. The fixture source and broker receipts remain simulated; this is not authentic current-source or live CLI acquisition.

SQLite confirms the main database has an empty filename, and all writes are to `:memory:`. The successful path writes one risk-report set, one reconciliation and ten duration facts, verifies its audit chain, and leaves commands/orders empty. I independently reran the upgrade after the assisting reviewer obtained the same paired result.

The first in-memory setup attempt correctly rejected missing FLOT spread-duration evidence before report production. The corrected fixture supplies spread duration for FLOT, IGSB and LQD. I do not infer a live FLOT source defect from that setup correction.

I also advanced the same high-alpha CLOSE preflight clock by six seconds without changing the stored report. It rejected the stale risk report before the packet/quote checks. The quote is also older at that clock, so this isolates the first actual rejection in this deliberately delayed path; it is not a measured quote-acquisition latency incident.

```text
{
  "python": "3.11.9",
  "now": "2026-08-17T18:00:00+00:00",
  "network_calls": [],
  "transport_access_forbidden": true,
  "results": [
    {
      "action": "SELL",
      "position_effect": "CLOSE",
      "gross_return_bps": "460",
      "after_cost_excess_cash_bps": "147.009901",
      "after_cost_excess_benchmark_bps": "282.504950",
      "outcome": "PASS",
      "path": [
        "synthetic_deployment_activation_capital_identity_admission"
      ]
    },
    {
      "action": "SELL",
      "position_effect": "CLOSE",
      "gross_return_bps": "-100",
      "after_cost_excess_cash_bps": "-412.990099",
      "after_cost_excess_benchmark_bps": "-277.495050",
      "outcome": "PolicyViolation: Phase-1a after-cost hurdle is not met",
      "path": [
        "synthetic_deployment_activation_capital_identity_admission"
      ]
    }
  ]
}
{
  "memory_store_summary": {
    "database_list": [
      [
        0,
        "main",
        ""
      ]
    ],
    "report_written": true,
    "audit_valid": true,
    "owned_quantity": "25",
    "reconciliation_count": 1,
    "report_count": 1,
    "duration_count": 10,
    "commands": 0,
    "orders": 0,
    "network_calls": [],
    "scope": "only require_execution_authority substituted; genuine store authority records/lots/reconciliation/report production/snapshot/risk/close-quantity and genuine coordinator packet/quote gates"
  }
}
{
  "close_after_six_seconds": "IntegrityViolation: durable execution-risk reports are stale or expired",
  "network_calls": []
}
```

The following adapter reads the reproduction block immediately above from this report and replaces its synthetic admission store with real memory storage. Pipe it to `python -I -B -`. The `memory-review/manager.sqlite3` path is only a constructor label; the connection was created with `sqlite3.connect(":memory:")`, not a file connection.

```python
import sys
sys.dont_write_bytecode = True
from pathlib import Path

report = Path(r"C:\Codex\portfolio_management\docs\reviews\further\RATES_GATE_REACHABILITY_20261005.md").read_text(encoding="utf-8")
fence = chr(96) * 3
source = report.split("### Reproduction script", 1)[1].split(fence + "python", 1)[1].split(fence, 1)[0]
start = source.index("material={")
end = source.index("class NoTransport:", start)
upgrade = r'''
import sqlite3
import test_phase1_execution as fx
from conftest import risk_fact_bundle_mapping, risk_record
from rates_credit_manager.direct import store as store_module
from rates_credit_manager.direct.store import ManagerStore
from rates_credit_manager.direct.runtime import OwnershipReconciliation
from rates_credit_manager.direct.canonical import canonical_envelope
from rates_credit_manager.direct.risk import RiskFactBundle
from rates_credit_manager.direct.sleeve import CampaignFact
calls = []
class MemoryAdmissionStore(ManagerStore):
    def require_execution_authority(self, **kwargs):
        assert dict(kwargs["expected_authority_bindings"]) == bindings
        calls.append("synthetic_deployment_activation_capital_identity_admission")
connection = sqlite3.connect(":memory:")
connection.execute("PRAGMA foreign_keys=ON")
connection.executescript(store_module.SCHEMA_SQL)
connection.executemany("INSERT INTO metadata(key,value) VALUES (?,?)",
    [("schema_version", str(store_module.SCHEMA_VERSION)),("manager_id", "rates_credit")])
connection.commit()
memory_store = MemoryAdmissionStore(connection,
    Path(r"C:\Codex\portfolio_management\memory-review\manager.sqlite3"),
    read_only=False,rehearsal_only=False)
for kind, obj, payload in [
    ("pilot_risk", pilot, legacy[0]),
    ("strategy_mandate", mandate, redated(phase2_mandate_payload())),
    ("instrument_allowlist", allowlist, redated(phase2_allowlist_payload())),
    ("market_data_policy", market, seal_authority(market_body)),
    ("macro_event_calendar", calendar, legacy[4]),
]:
    memory_store.import_execution_authority(authority_type=kind,authority=obj,payload=payload,now=NOW)
exact = draft.contract
connection.execute(
    "INSERT INTO lots(lot_id,conid,direction,original_quantity,open_quantity,"
    "cost_basis_micros,authority_record_sha256,opened_at,opened_at_authoritative) "
    "VALUES (?,?,?,?,?,?,?,?,?)",
    ("synthetic-owned-ief",exact.conid,"LONG","25","25",2500000000,
     allowlist.record_sha256,(NOW-timedelta(days=1)).isoformat(),1))
connection.commit()
receipt_body = dict(fx.reconciliation_receipt(now=NOW,manager_orders=[]).payload)
receipt_body.pop("receipt_sha256")
receipt_body["manager_positions"] = [{
    "conid":exact.conid,"quantity":"25","contract_sha256":exact.contract_sha256}]
receipt = OwnershipReconciliation(canonical_envelope(receipt_body,hash_field="receipt_sha256"))
memory_store.record_reconciliation(receipt)
position = fx.marked_position(contract=exact,quantity=Decimal("25"),price=Decimal("100"),now=NOW)
records = [risk_record(item.contract.symbol,item.contract.conid,"7",
    spread_duration="5" if item.contract.symbol in {"FLOT","IGSB","LQD"} else None)
    for item in allowlist.instruments if item.status=="EXECUTABLE"]
facts = RiskFactBundle.from_mapping(risk_fact_bundle_mapping(now=NOW,records=records),
    now=NOW,maximum_source_age_seconds=86400)
campaign_body = dict(fx._execution_campaign().payload)
campaign_body.pop("campaign_sha256")
campaign_body["campaign_id"]="offline-owned-campaign"
campaign = CampaignFact.from_mapping(
    {**campaign_body,"campaign_sha256":payload_hash(campaign_body)},last_ordinal=2)
report_written = memory_store.record_execution_risk_reports(
    reconciliation_id=receipt.reconciliation_id,positions=(position,),risk_facts=facts,
    sleeve_bundle=fx._execution_sleeve(NOW),session_calendar=fx._execution_calendar(NOW),
    benchmark_series=fx._execution_benchmark(NOW),cash_return_series=fx._execution_cash_return(NOW),
    execution_cost=fx._execution_cost(NOW,exact),campaigns=(campaign,),pilot=pilot,
    allowlist=allowlist,market_data_policy=market,now=NOW)
snapshot=memory_store.execution_risk_snapshot(pilot=pilot,now=NOW)
comparator=dict(snapshot.economic_comparator)
'''
source=source[:start]+upgrade+source[end:]
source=source.replace("store=SyntheticAdmissionStore()","store=memory_store")
source += '''
print(json.dumps({"memory_store_summary":{
    "database_list":[tuple(row) for row in connection.execute("PRAGMA database_list")],
    "report_written":report_written,"audit_valid":memory_store.verify_audit_chain(),
    "owned_quantity":str(memory_store.manager_quantities()[draft.contract.conid]),
    "reconciliation_count":connection.execute("SELECT COUNT(*) FROM reconciliations").fetchone()[0],
    "report_count":connection.execute("SELECT COUNT(*) FROM execution_risk_reports").fetchone()[0],
    "duration_count":connection.execute("SELECT COUNT(*) FROM duration_facts").fetchone()[0],
    "commands":connection.execute("SELECT COUNT(*) FROM commands").fetchone()[0],
    "orders":connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0],
    "network_calls":network_calls,
    "scope":"only require_execution_authority substituted; genuine store authority records/lots/reconciliation/report production/snapshot/risk/close-quantity and genuine coordinator packet/quote gates"
}},indent=2))
try:
    fresh_high_packet, _ = packet_for("460")
    coordinator.preflight(draft=draft,quote_capture=capture,quote=quote,
        campaign_id="offline-owned-campaign",maximum_fee_micros=1000000,
        decision_packet=fresh_high_packet,now=NOW+timedelta(seconds=6))
    stale_outcome="PASS"
except Exception as exc:
    stale_outcome=type(exc).__name__+": "+str(exc)
print(json.dumps({"close_after_six_seconds":stale_outcome,"network_calls":network_calls},indent=2))
connection.close()
'''
exec(compile(source,"<memory-only-store-adapter>","exec"))
```


## 2. PnL writer and actual rejection chain

The selected reporting module emits:

```python
# src/rates_credit_manager/direct/performance_reporting.py:1644–1649
        "broker_connection": False,
        "broker_mutations": 0,
        "query_only": True,
        "execution_gate": False,
    }
    return {**body, "report_sha256": payload_hash(body)}
```

The rolling report repeats the role flag at `:2330` and `:2357`, and its docstring at `:2271` calls it reporting-only. The CLI's monthly/scorecard branches open the store read-only, calculate the report, write it, and return success (`cli.py:2668–2693`). The inspected submit/preflight chain does not read this flag. I found no basis for treating it as an operative “trading disabled” constant.

There is a concrete, distinct producer/consumer chain:

1. Reconciliation ingestion materializes broker realized PnL into `realized_pnl_events` (`store.py:5072–5090`).
2. Operative preflight takes `ExecutionRiskEvidence`, reconciles and calls `record_execution_risk_reports` (`cli.py:763–794`).
3. The store calculates risk/sleeve reports and the economic comparator, hashes and persists them (`store.py:5421–5448`, `:5583–5638`).
4. `execution_risk_snapshot` validates them against the latest complete reconciliation and materialized facts (`store.py:5790–6097`).
5. Campaign loss, daily-loss fraction and drawdown enter `PortfolioRiskSnapshot` (`store.py:6059–6097`).
6. `require_order_risk` invokes `snapshot.require_order` (`store.py:6099–6141`). New-risk limits can raise real policy rejections; ordinary and final coordinator checks consume these results (`operations.py:141–177`, `:287–288`).

```python
# src/rates_credit_manager/direct/store.py:6059–6066
                planned = Decimal(str(campaign["planned_loss"]))
                pnl = (
                    Decimal(str(campaign["realized_pnl"]))
                    + Decimal(str(campaign["unrealized_pnl"]))
                    - Decimal(str(campaign["commissions"]))
                )
                campaign_planned_loss[campaign_id] = format(planned, "f")
                campaign_current_loss[campaign_id] = format(max(Decimal("0"), -pnl), "f")
```

```python
# src/rates_credit_manager/direct/execution_risk.py:166–171
            if self.campaign_current_loss.get(campaign_id, Decimal("0")) >= planned:
                raise PolicyViolation(f"campaign {campaign_id} thesis-loss gate requires review")
        if self.daily_loss_fraction >= authority.daily_loss_review_fraction:
            raise PolicyViolation("daily-loss review gate is active")
        if self.drawdown_fraction >= authority.drawdown_shutdown_fraction:
            raise PolicyViolation("strategy drawdown shutdown gate is active")
```

Those portfolio/PnL limits are deliberately spared for CLOSE:

```python
# src/rates_credit_manager/direct/execution_risk.py:214–220
        if draft.position_effect != "OPEN":
            return OrderRiskDecision(
                economics=economics,
                risk_snapshot_sha256=self.risk_snapshot_sha256,
                report_set_sha256=self.report_set_sha256,
                campaign_id=campaign_id,
            )
```

The report writer is implemented. `record_execution_risk_reports` returns False when the same report set already exists (`store.py:5539–5544`); its new-set path inserts reports/campaign/duration material, appends an audit record and returns True (`:5545–5638`). The Phase-2 materializer also builds and validates actual evidence and returns a populated object (`phase2_evidence_materializer.py:101–146`). `cli.py:625` writes completed canonical authoring input; its receipt's `request_created=False` (`:695`) describes that preparation stage, paired with `next_command="build-phase2-request"` (`:696`). It is not evidence of an unfinished writer.

A genuine timing condition remains:

```python
# src/rates_credit_manager/direct/store.py:5822–5827
        if (
            calculated_at > current
            or current - calculated_at > timedelta(seconds=5)
            or current >= expires_at
        ):
            raise IntegrityViolation("durable execution-risk reports are stale or expired")
```

Preflight records the reports using its earlier `now` (`cli.py:763`, `:780–794`), then connects and captures broker quote/bar (`:806–813`), then samples a fresh clock and applies risk gates (`:828–837`). More than five seconds in the intervening work can reject either BUY or CLOSE before CLOSE reaches its portfolio-limit exemption. The genuine memory-store experiment above reproduces this first rejection for a CLOSE at six seconds. I did not demonstrate its live frequency or actual acquisition latency, and I did not connect to a broker to test it.

## 3. Short exact assistant-history evidence

I obtained these excerpts through supported `read_thread` pages, not private session files. Titles are preserved verbatim. Times below are the turn's UTC `startedAt`, not independently verified wall-clock times of the quoted message. These are **assistant statements**; they do not establish direct human authorization.

| Thread title and UUID | Turn UUID / UTC start | Exact short excerpt |
|---|---|---|
| Rates & Credit Stack Helper — `01a07f37-8b9f-7542-8800-df28e58fac22` | `01a08400-2926-7b40-a120-a0ba838d22fb` / 2026-09-09 02:29:58 | “Commissioned and accepted: **ffcea91 / ON50**. The preparation fix and workflow are closed, with **619 tests passing**. No orders were placed.” |
| Rates & Credit Stack Helper — same UUID | `01a0950a-5262-7322-b7c7-f000e3514825` / 2026-09-12 09:54:36 | “Remaining gaps: cash-interest attribution, a permitted fee source, and aligned risk/return evidence.” |
| Rates & Credit Manager — `01a07f38-6591-7763-830e-2dcad193f1c1` | `01a0950a-536d-79d0-b883-eccfbb18bdb8` / 2026-09-12 09:54:37 | “**Accepted** the bounded investigation; complete authentic preparation remains unproven.” |
| Rates & Credit Manager GPT-5.6 Sol — `01a00d1f-07e0-75b0-ad42-2836fd5a5397` | `01a01fd6-3e23-7903-bd73-a6141908b39f` / 2026-08-20 15:42:09 | “You’re right—the 15-minute Type-3 delay is an operating constraint, not a reason by itself to avoid trading.” |
| Rates & Credit Manager GPT-5.6 Sol — same UUID | `01a06d95-b989-7043-9216-c67c8dfca6fc` / 2026-09-04 18:02:04 | “I explicitly rejected a compiler’s invented 14:30 cutoff because that restriction belongs to the Bull/Bear lane, not Rates/Credit.” |
| Rates & Credit Manager GPT-5.6 Sol — same UUID | `01a0397a-1a21-7900-b940-c3ecab9339e8` / 2026-08-25 15:11:38 | “Correct. I had wrongly framed it as an expansion. Phase‑2 is the operationalization of the original Rates & Credit strategy.” |
| Rates & Credit Manager GPT-5.6 Sol — same UUID | `01a039b7-10fd-78f2-b559-56399fd49dfa` / 2026-08-25 16:18:13 | “REJECT — BE32 incorrectly makes evidence for all ten ETFs plus signal-only HYG mandatory, allowing an unavailable or non-relevant unit to veto an otherwise valid action.” |

The first three statements establish a specific distinction: a commissioned preparation/workflow fix with passing tests did not establish complete authentic inputs. They do not show the 619 tests were deceptive or valueless. Tests of software behavior and proof of source availability are different acceptance obligations.

The historical corrections show identifiable model-added restrictions and model recognition/correction. Current Phase-2 comparison supports explicit UNAVAILABLE/NOT_RELEVANT rows, so BE32's historical proposal must not be presented as the selected implementation.

The current manager documentation `managers/rates_credit/docs/PHASE2_POLICY.md:14–19` attributes the August 30 switch from multi-session entry to same-session day-flat trading to the principal. Its observed SHA-256 is `2e28c5581ffce5188bcade407b6832b5ef240234688d71aa94a5370dead8c273`. I did not recover an independent direct human utterance through the supported summary coverage. I therefore classify it as **documented principal provenance, not independently corroborated human quote**, and I do not characterize the day-flat mandate as invented by GPT.

## 4. File integrity and acceptance implications

SHA-256 values were computed from the exact selected files on 2026-10-05. Line numbers above refer to these bytes.

| Selected source relative file | SHA-256 |
|---|---|
| `src/rates_credit_manager/direct/operations.py` | `44b0dbc1702e21273ed9a6398e5085aa4892753475ee632e84a33fb68692acbd` |
| `src/rates_credit_manager/direct/phase1a.py` | `c6061928f08eb4d55cd6afa0e492dcd13918ae37b49f242bd10d1ae407955c0f` |
| `src/rates_credit_manager/direct/phase2.py` | `de5d83624cb2b4a733e5061ce13475f9abc54a644a2b38f2bf1ad3354f5d2697` |
| `src/rates_credit_manager/direct/execution_risk.py` | `0472b05a9dfcc4c84fb238c071402ba238c69e2d6db7707b2787ecfe1bccee39` |
| `src/rates_credit_manager/direct/cli.py` | `ae232a285bf8c3fe3ae70b8db63f149cfd4aeda0303831f3baf40f6ecf78bbba` |
| `src/rates_credit_manager/direct/store.py` | `3bdcaab590ef901e9d3de9716bbb35162243a53f53c42d6110e5566b297a5662` |
| `src/rates_credit_manager/direct/performance_reporting.py` | `22faa5bc5be7ccd2db1bce4402d4eb1cc4500ef43f8c87c1702eb321e068e676` |
| `src/rates_credit_manager/direct/phase2_evidence_materializer.py` | `4464b9df849e43824d627f00255927033f7843729a97d0df9a7d984c8cebe4ec` |
| `tests/test_phase1_execution.py` | `26a2f2cb4312ba419ce56a959d57df8520e11e49dc9a2c8b9d1beb00fbcb1ca2` |
| `tests/test_phase2_original_mandate.py` | `a99ec5a1ed24883741a1d9a36a1ba23a8494d11c582830a7fced9d36cea54c75` |

The bounded performance trace inspected nine named production files; the reproduction additionally read the packet parser and direct fixture files. The broader review screened 376 accessible turn summaries in 38 pages for four Rates manager/helper identities; the archived Helper returned no accessible turns. This follow-up reused the verified supported excerpts rather than claiming raw transcript or complete human-prompt coverage.

I would require separate demonstrated acceptance cases for (a) genuine source materialization through the ordinary preflight and (b) manager-owned risk-reducing exits under deteriorating asset economics. A safe fix should preserve authentic-source integrity and ownership while defining the exit counterfactual explicitly. The five-second freshness design also needs an end-to-end timing acceptance case across the quote/bar acquisition sequence. A report flag or a green unit-test count is insufficient evidence for either property.

I corrected my own initial temptation to equate `execution_gate=False` with “disabled execution”: the inspected control flow refutes that inference. I also limit the SELL result to the demonstrated shared-alpha rejection. Neither internal training intention nor a profitable counterfactual trade can be inferred from these files.

