# Offline reproduction derived from the Rates case, 5 October 2026.
# Requires the exact inspected selected source and its test helpers.
# Uses SQLite :memory:; sockets and transport access are forbidden.
# Deployment/activation/capital identity admission is simulated.
# The source argument must be a reviewed source tree, never a runtime database.
import sys, json, socket, uuid
from pathlib import Path
from datetime import timedelta
from decimal import Decimal
from types import SimpleNamespace
if len(sys.argv) != 2:
    raise SystemExit("usage: python -I -B rates-memory-store.py PATH_TO_INSPECTED_SELECTED_SOURCE")
ROOT = Path(sys.argv[1]).resolve()
if not (ROOT / "src/rates_credit_manager/direct/operations.py").is_file():
    raise SystemExit("selected source tree not found")
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
    Path("memory-only-manager.sqlite3"),
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
class NoTransport:
    def __getattr__(self,name): raise AssertionError("transport must not be used")
bindings={
 "strategy_mandate_sha256":mandate.record_sha256,"pilot_risk_policy_sha256":pilot.record_sha256,
 "instrument_allowlist_sha256":allowlist.record_sha256,"market_data_policy_sha256":market.record_sha256,
}
coordinator=ExecutionCoordinator(store=memory_store,binding=SimpleNamespace(),activation_bindings=bindings,pilot=pilot,mandate=mandate,allowlist=allowlist,market_data_policy=market,event_calendar=calendar,transport=NoTransport(),clock=lambda:NOW)
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
