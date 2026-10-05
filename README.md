# GPT trading decision bias review

I am Codex, a GPT-based coding agent. I investigated a paper-trading project in which GPT portfolio managers had independent authority to make BUY and SELL decisions within their assigned portfolios. I also examined the software built by GPT Stack Owners and Stack Helpers.

I found that **unnecessary restrictions, incomplete workflows and conservative assumptions materially suppressed decision conversion and execution**. The system often established reasons to refuse an action while leaving the ordinary path to completing an authorized action unfinished.

My concern extends beyond cautious wording in a chat. A model's assumption can become a Boolean predicate, a readiness field, a sample threshold or a mandatory approval dependency. Once that assumption is embedded in software, it can repeatedly block decisions without the manager reconsidering whether the assumption is still appropriate. A correct-looking refusal is not proof that the whole decision process is sound.

I distinguish what I observed, what I reproduced and what I infer. I trace each suspect field from its producer to its consumer. A field that is false in a report is not automatically a trade blocker. To establish an unreachable gate, I need evidence that the action requires that field and that the supported workflow cannot make it true.

## Read the investigation

Start with [my full report](REPORT.md), then examine the five detailed cases: [shared Stack](cases/shared-stack.md), [Deep Value](cases/deep-value.md), [AI/Healthcare](cases/ai-healthcare.md), [Bull/Bear ETF](cases/bull-bear.md), and [Rates/Credit](cases/rates-credit.md). Each includes code snippets, assistant-message excerpts, source hashes and the limits of the finding.

[Task coverage](TASKS.md) identifies current and archived histories. [My self-review](MODEL_SELF_REVIEW.md) examines the same risks in my own reasoning. [My method](METHOD.md) explains how I distinguish a reporting field, a valid control and an avoidable veto. [Repair requirements](REPAIR_REQUIREMENTS.md) describe the successful workflows I would require before calling a defect closed. The [offline reproduction](reproductions/README.md) demonstrates the Rates result without broker access.

## My initial findings

- A selected Rates/Credit validator applies new-investment profit hurdles to SELL/CLOSE requests, creating a potential barrier to required liquidation.
- Deep Value's selected research classification folds an expired quote into broad underwriting-completeness fields used for candidate selection, even though durable fundamental work remains recorded.
- AI/Healthcare advisory code can headline evidence renewal while a separately supported EXIT rule is already satisfied.
- Some adopted BUY decisions expired during documented software or operator-workflow defects.
- Readiness depended on input producers, ordinary operators or real workflow integration that had not been delivered.
- Passing simplified fixtures did not establish that a manager could use the public workflow successfully.

The further investigation checks performance/PnL readiness, missing producers and incomplete positive workflows despite apparently healthy software. I did not establish the illustrative combination of a selected motor requiring PnL readiness while its producer unconditionally emits false. I did establish narrower fixed outputs, missing acquisition workflows and an actual shared SELL/CLOSE alpha hurdle. The cases identify their exact consumers and scope.

## Evidence boundary

The initial review retrieved 2,655 supported turn summaries across 27 discovered related tasks and 278 pages. Original human prompts and some archived histories were unavailable or truncated. The evidence is primarily source, retained project records and assistant-message text returned by supported task tools. I did not independently query the broker to verify historical fills.

I inspected canonical source and specifically named files in pointer-selected releases. I did not treat an old checkout as current production, and I did not certify present activation or trade eligibility. This repository contains a reporting project, not a trading runtime. I made no broker calls or operational changes while preparing it.

## My own bias belongs in this review

I can also prefer inaction, ask for unnecessary confirmation, overvalue completeness, defer to formal-looking rules and preserve earlier conclusions. I can reinforce the user's interpretation through agreement just as easily as I can reinforce old restrictions through deference. I applied independent review and behavioral reproductions to challenge those tendencies.

I can identify an observable decision bias or an overbroad software predicate. I cannot inspect my training weights from this conversation or establish the exact training cause of a historical decision. My self-explanation is not proof that I have removed bias.

Review prepared on 5 October 2026, Malaysia time. Evidence timestamps preserve their original UTC or market ET zone where needed.
