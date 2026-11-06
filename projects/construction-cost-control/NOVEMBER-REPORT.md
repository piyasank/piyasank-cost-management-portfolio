# November cost report

**£5m office refurbishment and fit-out | 30 November 2026 | Illustrative scenario**

The expected final cost is **£5,117,400**, up **£120,000** from October and **£117,400 over approved funding**. The known forecast alone exceeds funding by £45,000. At P80, the funding gap is **£172,023**.

**Decision requested.** Confirm the funding confidence level and ask the project team to validate the £30,000 MEP coordination uplift and identify priced scope reductions before making further discretionary commitments. If the sponsor retains P80 as the planning basis, bring back a revised forecast showing how evidenced scope changes, mitigation or additional funding address the £172,023 gap.

[Download the November Excel workbook](model/November-Cost-Control.xlsx) · [Download the November Word report](reports/November-Cost-Report.docx)

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

## Evidence behind the MEP assumptions

### £30,000 coordination uplift

This illustrative build-up reconciles the October and November WP03 allowances. The hours and rates show how a scope increase could produce the uplift. They are sample estimate inputs for this case.

| Coordination activity | Rate | October hours | October cost | November hours | November cost | Uplift |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Site surveys and verification | £100/h | 60 | £6,000 | 180 | £18,000 | £12,000 |
| Coordinated drawings and clash resolution | £75/h | 80 | £6,000 | 240 | £18,000 | £12,000 |
| Trade coordination and sequencing reviews | £100/h | 30 | £3,000 | 90 | £9,000 | £6,000 |
| **Total** | | **170** | **£15,000** | **510** | **£45,000** | **£30,000** |

In this example, the repricing comes from 340 additional hours at the original rates. On a live project, ask the MEP lead for a marked-up scope and drawing register showing what additional work is required. Ask the cost manager to reconcile the hours and rates to an itemised quotation and check the scope against the contract, CO05 and CO10 before carrying the uplift as a priced forecast item.

### Restricted access probability

The 20% assumption depends on the proposed work sequence making the required areas available when each trade needs them. Ask the planner for an agreed, zone-by-zone access programme with dates, work windows and dependencies. Check it with the affected trades against permits, shutdown bookings and recent access or clash records before relying on the lower probability.

| November sensitivity | R02 probability | Known forecast | Residual risk allowance | Expected final cost | P80 funding gap |
| --- | ---: | ---: | ---: | ---: | ---: |
| Access sequence delivers the assumed benefit | 20% | £5,045,000 | £72,400 | £5,117,400 | about £172k |
| Keep October's access probability | 35% | £5,045,000 | £82,400 | £5,127,400 | about £184k |

Keeping the probability at 35% adds £10,000 to expected final cost. The known forecast stays the same. To reproduce the sensitivity, copy the November inputs, change risk `R02`’s `probability` from `0.20` to `0.35`, then run the command below using the copied file. The comparison holds the other November inputs, simulation seed and trial count fixed.

## Reproduce the report

Use the [October inputs](data/project-inputs.json) and [November inputs](data/november-inputs.json) with the same model. The [November output](data/november-results.json) includes the package reconciliation and the seeded simulation. Run from the repository root:

```sh
python projects/construction-cost-control/src/model.py --inputs projects/construction-cost-control/data/november-inputs.json
```

Both periods use synthetic records. The November cut is a forward scenario and assumes only the movements listed above. The October working model and original management report show the October reporting cut.
