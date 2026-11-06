# November cost report

**£5m office refurbishment and fit-out | 30 November 2026 | Illustrative scenario**

The expected final cost is **£5,117,400**, up **£120,000** from October and **£117,400 over approved funding**. The known forecast alone exceeds funding by £45,000. At P80, the funding gap is **£172,023**.

**Decision requested.** Confirm the funding confidence level and ask the project team to validate the £30,000 MEP coordination uplift and identify priced scope reductions before making further discretionary commitments. If the sponsor retains P80 as the planning basis, bring back a revised forecast showing how evidenced scope changes, mitigation or additional funding address the £172,023 gap.

## Forecast movement

| Movement | Effect on known final cost | Explanation |
| --- | ---: | --- |
| October known forecast | £4,915,000 | Opening position |
| WP03 accrual certified | £0 | £90,000 moved from accrued to certified cost. Total incurred cost stayed at £2,175,000. |
| CO05 ventilation revision approved | £0 | £180,000 moved from pending changes to commitments at the October forecast value. |
| CO10 instruction enters at November cutoff | +£100,000 | Separate approved instruction dated 3 November, outside the October cutoff. |
| Outstanding MEP coordination repriced | +£30,000 | WP03 base-scope allowance rose from £15,000 to £45,000. This scope is separate from CO05 and CO10. |
| **November known forecast** | **£5,045,000** | **£130,000 increase** |

The assumed MEP access sequence reduces the probability of restricted access (R02) from 35% to 20%. The impact range and delay assumptions stay at October levels. The residual risk allowance falls by £10,000, from £82,400 to £72,400, bringing the net increase in expected final cost to £120,000. Approved changes now total £530,000 against the original £500,000 contingency, so allocated package budgets exceed approved funding by £30,000.

## Funding position

| Measure | October | November | Movement |
| --- | ---: | ---: | ---: |
| Expected final cost | £4,997,400 | £5,117,400 | +£120,000 |
| Expected funding headroom (shortfall) | £2,600 | (£117,400) | −£120,000 |
| P80 final cost | £5,053,631 | £5,172,023 | +£118,391 |
| P80 funding gap | £53,631 | £172,023 | +£118,391 |

P80 figures and movements are rounded independently from the unrounded outputs. The P80 movement consists of the £130,000 known cost increase and an approximately £11,609 reduction in the simulated P80 residual allowance. All 50,000 November draws exceed the cap under these assumptions because the known forecast already exceeds funding and simulated risk costs are non-negative.

## Reproduce the report

Use the [October inputs](data/project-inputs.json) and [November inputs](data/november-inputs.json) with the same model. The [November output](data/november-results.json) includes the package reconciliation and the seeded simulation. Run from the repository root:

```sh
python projects/construction-cost-control/src/model.py --inputs projects/construction-cost-control/data/november-inputs.json
```

Both periods use synthetic records. The November cut is a forward scenario and assumes only the movements listed above. The Excel workbook and original management report show the October reporting cut.
