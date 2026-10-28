# Detergent line material-loss investment case

**Question:** does the full cost of loss-control equipment justify the achievable reduction in material use?

This independent case study represents a hypothetical UK line producing 10 million saleable one-litre bottles annually. All calculations use GBP. It is separate from the earlier EUR100m introductory exercise and is not a forecast of Unilever.

## Findings under the illustrative base case

| Measure | Result |
| --- | ---: |
| Baseline process loss as a share of input | 3.0% |
| Proposed process loss | 2.0% |
| Annual liquid input avoided | 108,353 kg |
| Gross annual operating saving | £57,205 |
| Net annual recurring cash saving after maintenance | £49,205 |
| Capital spending including contingency | £92,000 |
| Total initial economic outflow | £117,767 |
| Five-year net present value at 10% | £46,392 |
| Simple payback after commissioning | 28.7 months |
| Payback including preparation | 34.7 months |
| First-year operating profit effect | (£10,364) |
| NPV if loss only falls to 2.5% | (£48,543) |
| Highest process loss at NPV zero, other assumptions unchanged | approximately 2.245% |

**Recommendation:** conduct a measured production trial and obtain supplier quotations before capital approval. Positive savings alone do not establish that an investment meets its required return.

## Start here

- [Excel investment model](model/Detergent-Line-Investment-Case.xlsx): begin on the Decision tab. Amber cells contain editable inputs.
- [One-page management brief](reports/Investment-Brief.pdf).
- [Six-slide presentation](presentation/LinkedIn-Carousel.pdf).
- [Assumptions in JSON](model/assumptions.json) and [published result snapshot](model/published-results.json).
- [Portable Python calculation](src/model.py) and [verification tests](tests/test_model.py).

## Calculation method

1. Saleable litres × density gives acceptable product mass.
2. Acceptable mass / (1 - process loss) gives required input mass.
3. Each ingredient group's quantity × assumed delivered rate gives its cost. The mix is a costing abstraction, not a usable product formulation.
4. Add packaging, labour, energy, disposal, freight, factory overhead and depreciation.
5. Compare baseline and proposal at identical saleable output. No automatic payroll saving, extra sales or working-capital release is claimed.
6. Deduct maintenance and extra electricity from avoided operating costs to derive recurring cash savings.
7. Include capital spending, pilot and training, and the contribution lost on installation output that cannot be recovered.
8. Discount the incremental economic cash flows over five years at an assumed 10% required return.

Capital and one-off economic costs are conservatively charged at time zero. Year 1 receives six months of savings. Project depreciation affects accounting profit but is excluded from cash flow. The pre-tax model excludes financing, inflation and working-capital changes.

Full proposal production cost includes new maintenance and project depreciation. It is approximately £0.904 per bottle, against £0.907 before the project. These are factory-level costs, excluding corporate costs.

## Reproduce the results

Python 3.10 or later is sufficient. There are no third-party Python dependencies.

From the repository root:

```sh
python projects/manufacturing-detergent/src/model.py
python -m unittest discover -s projects/manufacturing-detergent/tests -v
```

To test another set of assumptions, copy and edit `model/assumptions.json`, then run:

```sh
python projects/manufacturing-detergent/src/model.py --inputs path/to/your-assumptions.json
```

The Python calculation independently reproduces the published workbook snapshot. Editing its JSON does not update the Excel workbook, PDF or presentation. Likewise, Excel edits do not automatically update the published presentation or result snapshot.

## Evidence and limitations

Public sources establish business context and a plausible area for investigation. They do not validate this line's engineering quantities, loss rates, recipe or commercial rates.

- **Unilever Q3 2026 trading statement, pp. 5, 8 and 10:** user-supplied report providing the initial Home Care business context. The source PDF is not redistributed here.
- [Unilever's 2026 digital twins release](https://www.unilever.com/news/press-and-media/press-releases/2026/unilever-scales-digital-twins-across-global-manufacturing-network-with-accenture/): reports 1-2% premium-ingredient savings from dosing controls at Cu Chi. This is narrower than total process loss and does not validate the 3%-to-2% model assumption.
- [UK National Living Wage rates](https://www.gov.uk/national-minimum-wage-rates): a contextual statutory floor, not an estimate of skilled factory pay. The assumed model wage is £15/hour.

No factory records or commercial quotations have been supplied. Material prices, equipment costs, density, production volume, loss rates and the discount rate remain assumptions. The costing mix is not a production recipe. The model assumes bulk process loss occurs before filling and packaging defects are detected before liquid filling, with no salvage or rework credit.

The conclusion is conditional. A real appraisal would require calibrated baseline/trial records, quality results, delivered purchase prices, equipment scope and quotations, metered energy data, maintenance terms and an installation production plan.

## Validation

The Excel build was checked for mass balance, quantity/rate arithmetic, financial reconciliations, missing inputs, commissioning timing and downside outcomes. Native Excel sensitivity-table results were compared with recalculating the same model. Python tests reproduce the published results, check decision reversals and independently verify the break-even loss and equipment thresholds.

This is an independent portfolio study, with no affiliation to Unilever and no claim of achieved savings.
