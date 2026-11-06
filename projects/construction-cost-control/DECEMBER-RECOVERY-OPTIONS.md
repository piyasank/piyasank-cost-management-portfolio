# December recovery options

**£5m office refurbishment and fit-out | Illustrative sponsor decision | Based on the 30 November forecast**

The November known forecast was **£5.045m**, or **£45k over approved funding before residual risk**. The P80 funding gap was **about £172k**. This review compares three choices using the same November baseline. The prices, delivery effects and mitigation assumptions are synthetic. The options are assessed separately.

## Options at the existing £5m funding cap

| Option | Change to known cost | Revised known cost | Known-cost shortfall | Expected final cost | P80 funding gap |
| --- | ---: | ---: | ---: | ---: | ---: |
| A. Retain scope and seek funding | £0 | £5,045k | £45k | £5,117k | £172k |
| B. Defer enhanced training | −£20k | £5,025k | £25k | £5,097k | £152k |
| C. Reduce scope costs and protect MEP access | −£42k | £5,003k | £3k | £5,069k | £119k |

Figures are rounded to the nearest £1k. The table shows gaps before any increase in funding is authorised.

| Option | Price and delivery consequence | Owner and approval needed |
| --- | --- | --- |
| A. Retain scope | Keep the existing specification and handover scope. An extra £173k in approved funding would cover the modelled P80, assuming no further forecast movement. | Project sponsor to confirm the funding basis and approve the increase at the December decision meeting. |
| B. Defer enhanced training | Split the £40k handover allowance into £20k of essential handover work retained now and £20k of optional training moved to a later budget. Allow £5k for a separate return visit. The future budget would need £25k, and total cost across both budgets would rise £5k before risk. | Facilities lead to confirm essential training, documentation and safe handover remain within the retained scope. Sponsor to approve the scope split and future budget before issuing a revised instruction. |
| C. Reduce scope costs and protect MEP access | Assume a £30k credit for alternative door finishes and £20k from simplifying outstanding MEP coordination scope. Spend £8k on protected access windows and trade sequencing, giving a net £42k reduction in known cost. Finishes change and access windows restrict when some trades can work. | Cost manager to obtain the credit and revised MEP price. Design lead to confirm fire, acoustic and accessibility requirements are met. Planner to confirm the access windows before the sponsor approves the package. |

## Recommendation

Take **Option C** to the December decision meeting with supplier-backed prices and an agreed access programme. Even if those prices hold, the known forecast remains **£3k above the cap**. At P80, allow **about £119k** of additional funding if the access mitigation is supported. If the access cost is incurred but restricted-access probability stays at November’s 20%, the modelled P80 gap is **about £130k**.

Keep the November forecast as the control baseline until scope and funding decisions are approved. If the package cannot be evidenced by the decision meeting, use Option A as the funding reference. Use Option B only if the facilities team can demonstrate that the training can safely be deferred and the sponsor accepts the later cost.

## How risk was treated

Options A and B retain the November risk inputs. Option C separately tests a reduction in the probability of restricted access from 20% to 10%, with the impact range and other risks held constant. That assumption lowers expected residual risk by about £6.7k. The £42k known-cost reduction is the net effect of the illustrative prices and mitigation spend. It does not include the reduction in risk allowance.

The [November report](NOVEMBER-REPORT.md) explains the baseline. Run the comparison from the repository root using the existing model and 50,000 seeded draws:

```sh
python projects/construction-cost-control/src/recovery_options.py
```
