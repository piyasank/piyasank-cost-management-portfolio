# Production trial and investment decision

The trial would establish whether loss-control equipment can reduce bulk liquid loss consistently enough to justify the investment while maintaining product quality and saleable output. The current model breaks even at **about 2.25% bulk process loss**, using a 3.0% baseline and the published prices and costs. A measured baseline and firm quotations would change that threshold. This is a proposed trial for the illustrative line.

## Trial design

1. **Agree the measurement boundary.** Measure from bulk material input to conforming liquid released to filling. For each batch, record input and released mass, opening and closing work in progress, and any samples, waste, holds or transfers. Use calibrated scales or verified metering and convert volumes using measured density where needed. Count rework once and reconcile it before closing the batch.
2. **Establish a comparable baseline.** Measure batches with the current controls across representative products, shifts, batch sizes and start-up or changeover conditions. Compare against matched runs with the proposed controls. Keep routine operational losses in both samples and record unusual events so their effect can be checked. Use baseline variability and meter uncertainty to set the trial size before the comparison. Repeat runs if the evidence cannot distinguish performance from the updated break-even threshold.
3. **Reconcile the loss and check quality.** For each matched group, calculate loss as reconciled bulk loss in kg divided by net bulk input in kg, after adjusting for work in progress and transfers. Pool by summing kilograms before dividing, and compare results by product and shift. Record quality holds, product rejects, pre-fill packaging rejects, saleable litres and line speed separately. Check that apparent bulk savings are not offset by quality failures, downstream waste or lower throughput.
4. **Update the investment model.** Replace assumed baseline and proposed loss with the trial evidence. Use delivered ingredient rates, metered energy and waste disposal charges. Obtain itemised supplier quotes for equipment, installation and validation, and confirm maintenance, training, downtime and commissioning timing. Recalculate five-year NPV and break-even loss, then test a conservative loss case informed by measured variability.

## Worked example

The example assumes the baseline remains 3.0% and holds all inputs fixed except the proposed loss rate and equipment price. The existing 15% capital contingency applies in all three cases.

| Scenario | Proposed bulk loss | Equipment price before contingency | Total capex | Five-year NPV | Break-even loss |
| --- | ---: | ---: | ---: | ---: | ---: |
| Published model | 2.0% | £60,000 | £92,000 | £46,392 | 2.245% |
| Illustrative trial result | 2.2% | £60,000 | £92,000 | £8,535 | 2.245% |
| Same loss with a higher quote | 2.2% | £70,000 | £103,500 | (£2,965) | 2.184% |

The 2.2% result clears the original threshold but misses the threshold at the higher price. Even at £60,000, the gap between the trial estimate and break-even is only about 0.045 percentage points. Check measurement uncertainty and run-to-run variability before treating that result as sufficient for approval.

**Decision rule.** Recommend approval only if quality and output meet the agreed acceptance criteria and five-year NPV stays positive under a conservative, trial-supported loss estimate and confirmed costs. If the trial remains inconclusive, extend it. If the revised case fails the return test, revisit the price or equipment scope before seeking capital approval.

To reproduce the example, copy the [model assumptions](model/assumptions.json) and set `investment.target_loss` to `0.022`. Run the [Python model](src/model.py) with `--inputs` pointing to the copy. Then set `investment.equipment` to `70000` and rerun.
