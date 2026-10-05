# My offline Rates reproduction

I extracted the stronger memory-store experiment from [the Rates case](../cases/rates-credit.md) into [rates-memory-store.py](rates-memory-store.py). It requires the exact inspected Rates selected source and its test helpers, release identity `ffcea91ba1ddb20f276ba8b52e13e25739b2c9c5`. This reporting repository does not distribute a broker runtime or the complete trading source.

```powershell
python -I -B .\rates-memory-store.py 'PATH_TO_REVIEWED_SELECTED_SOURCE'
```

The argument is the release's `source` directory containing `src` and `tests`. I made this path portable and changed the store's constructor label to `memory-only-manager.sqlite3`. SQLite connects only to `:memory:`; that label does not create a file. The logic comes from the recorded experiment. Do not substitute an operational database or execute an unreviewed source tree.

The reproduction forbids socket construction and transport access. It creates simulated authority, positions and source evidence in memory, then runs genuine Store authority imports, reconciliation, report production, risk snapshot, owned-quantity checks and ordinary coordinator preflight. Only deployment/activation/capital-identity admission is substituted.

The paired SELL/CLOSE cases differ in scenario return. The positive-alpha case passes; the negative-alpha case raises `PolicyViolation: Phase-1a after-cost hurdle is not met`. Advancing the high-alpha case by six seconds raises `IntegrityViolation: durable execution-risk reports are stale or expired`. The output also reports one reconciliation, one risk-report set, ten duration facts, a valid audit chain, and zero commands, orders and network calls.

These results establish source behavior under stated synthetic inputs. They do not establish authentic live-source availability, present activation, observed acquisition latency, the incremental utility of a real sale, or a profitable missed trade. The case preserves original experiment scripts and source hashes. [rates-memory-store-output.txt](rates-memory-store-output.txt) records the independently verified standalone run.
