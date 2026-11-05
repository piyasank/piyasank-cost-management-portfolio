# Walkthrough: construction cost control

## Start with the decision

Open the model on Dashboard. The question is whether the £5m funding cap is sufficient for the known work and remaining risks. The expected forecast leaves only £2,600. A P80 funding basis would require another £53,631 under the simulation assumptions.

P80 is not a prediction that cost will equal that number. It is the point at which 80% of the model's simulated outcomes are no higher.

## Terms in plain language

| Term | Meaning in this model |
| --- | --- |
| Certified value | Work already valued in a certificate, before retention. It is not a cash payment figure. |
| Accrual | Work completed but not yet included in a certificate. |
| Actual accrued cost | Certified value plus uncertified accrual. |
| Commitment | Current awarded contract value, including approved variations. |
| Outstanding commitment | Contract value remaining after incurred work has been recognised. |
| Unlet work | Scope that is outside the awarded contracts and still needs purchasing. |
| Pending change | A known instruction or scope change awaiting approval, priced at its best estimate. |
| Contingency | Funding held for uncertainty, not a saving that can automatically be released. |
| EMV | Expected monetary value, calculated from probability and average impact. |
| P80 | The 80th percentile of simulated final costs under the chosen risk model. |

## Experiment 1: approving a change should not count it twice

1. Open Changes and find CO05 on row 13.
2. Its forecast and agreed values both start at £180,000.
3. Change F13 from Pending to Approved.
4. Return to Cost Report. Current commitments rise by £180,000 and pending changes fall by £180,000.
5. Known forecast remains £4,915,000.
6. Restore F13 to Pending.

This tests reclassification of an existing forecast exposure. Approval at a different amount would change the forecast by the valuation difference.

## Experiment 2: certification should not invent new work

1. On Packages, MEP has £580,000 certified and £90,000 accrued.
2. Move £50,000 from accrual to certified: G11 becomes £630,000 and H11 becomes £40,000.
3. Actual accrued cost stays £670,000 for MEP. Final forecast also stays the same.
4. Restore G11 to £580,000 and H11 to £90,000.

If you increased certified cost without reducing accrual for the same work, you would temporarily recognise it twice.

## Experiment 3: observe risk and stale simulation control

1. On Risk, change D9 from £12,000 to £16,000 per week.
2. Expected delay cost and expected final cost rise by £8,800, because expected delay is 2.2 weeks.
3. Dashboard hides the old P50/P80/P90 results. Their simulation used a different weekly cost.
4. Restore D9 to £12,000 to return to the published snapshot.

## Experiment 4: respect the reporting cutoff

1. On Packages, change D5 from 31 October 2026 to 5 November 2026.
2. CO10 now falls within the cutoff. The known forecast increases by £100,000.
3. Return D5 to 31 October 2026 after the exercise.

A report as of October should not incorporate an instruction dated after its stated cutoff merely because you now know about it.

## Experiment 5: challenge an apparent saving

CO09 shows a possible £30,000 credit for alternative door finishes. It is an opportunity and has no deduction in the forecast. Approval would need confirmed scope, quality acceptance and a substantiated agreed credit. Even a valid £30,000 reduction would leave approximately £23,631 of the modelled P80 gap if the risk distribution stayed unchanged.

## Your two-minute explanation

I built a synthetic client cost report for a £5m office refurbishment. I started by reconciling certified valuations and accruals to actual incurred work, then added only the remaining contract commitments. I priced unlet work using quantity and rate and included pending changes at their full best estimate.

I treated approved changes as transfers from contingency into package budgets and commitments. The total funding cap stayed fixed. I also linked overlapping risk to the relevant change order so I did not add the same scope twice.

The expected forecast was about £4.997m, which initially looked within budget. A seeded risk simulation showed a P80 cost of about £5.054m and roughly a 45% modelled probability of exceeding funding.

My recommendation was to validate pending MEP scope, confirm the sponsor's required funding confidence and address the exposure through priced decisions. The main limitation is that every contract and risk input is synthetic. A real report would require project records and a review of correlated risks.

## Questions to prepare for

- Why does actual cost plus the full contract value overstate the forecast?
- How does approving a pending change affect contingency and commitments?
- Why is EMV different from P50?
- What does P80 depend on, and what would make it unreliable?
- Why have you excluded a potential value-engineering credit?
- Which project records would you obtain before issuing a real cost report?

I used AI assistance to help build and check the model and prepare the report. I would explain that openly, alongside what I learned and which assumptions I challenged.
