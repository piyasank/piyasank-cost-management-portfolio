"""Reproduce the investment case with Python's standard library.

This is an illustrative model, not measured Unilever factory data.
Changing assumptions here does not update the Excel workbook, PDF or slides.
"""
import argparse
import json
from copy import deepcopy
from pathlib import Path

DEFAULT_INPUT = Path(__file__).resolve().parents[1] / 'model' / 'assumptions.json'


def calculate(config):
    p, o, v = config['production'], config['operations'], config['investment']
    for loss in [p['baseline_loss'], v['target_loss'], o['packaging_loss']]:
        if not 0 <= loss < 1:
            raise ValueError('Loss rates must be between zero and less than one.')
    if abs(sum(x['mass_fraction'] for x in config['materials']) - 1) > 1e-9:
        raise ValueError('Material mass fractions must sum to one.')
    if p['saleable_litres'] <= 0 or p['litres_per_bottle'] <= 0 or p['density_kg_per_litre'] <= 0:
        raise ValueError('Output, pack size and density must be positive.')
    if p['operating_days'] <= 0 or v['asset_life_years'] <= 0 or v['discount_rate'] <= -1:
        raise ValueError('Invalid operating days, asset life or discount rate.')
    if int(v['commissioning_month']) != v['commissioning_month'] or not 1 <= v['commissioning_month'] <= 13:
        raise ValueError('Commissioning month must be an integer from 1 to 13.')
    if not 0 <= v['unrecoverable_output_share'] <= 1:
        raise ValueError('Unrecoverable output share must lie between zero and one.')
    litres = p['saleable_litres']
    bottles = litres / p['litres_per_bottle']
    good_kg = litres * p['density_kg_per_litre']
    price_per_kg = sum(x['mass_fraction'] * x['price_per_kg'] for x in config['materials'])
    packaging = bottles / (1-o['packaging_loss']) * sum(x['quantity_per_bottle'] * x['price_per_item'] for x in config['packaging'])
    payroll = o['shifts'] * o['paid_hours'] * o['crew_per_shift'] * p['operating_days'] * o['hourly_wage'] * (1+o['employer_oncost'])

    def process(loss):
        incoming = good_kg / (1-loss)
        waste = incoming-good_kg
        ingredients = incoming*price_per_kg
        electricity = (incoming*o['process_kwh_per_input_kg'] + bottles*o['filling_kwh_per_bottle'])*o['electricity_per_kwh']
        variable = ingredients+packaging+electricity+waste*o['disposal_per_kg']+bottles*o['freight_per_bottle']
        total = variable+payroll+o['fixed_overhead']+o['existing_depreciation']
        return {'input_kg':incoming,'loss_kg':waste,'variable_cost':variable,'total_cost':total}

    baseline, proposal = process(p['baseline_loss']), process(v['target_loss'])
    gross = baseline['total_cost']-proposal['total_cost']
    upkeep = v['annual_maintenance']+v['extra_annual_kwh']*o['electricity_per_kwh']
    net = gross-upkeep
    capex = (v['equipment']+v['installation']+v['validation'])*(1+v['contingency'])
    lost_litres = litres/p['operating_days']*v['downtime_days']*v['unrecoverable_output_share']
    contribution = p['selling_price_per_litre']-baseline['variable_cost']/litres
    lost_contribution = lost_litres*contribution
    oneoff = v['pilot']+v['training']+lost_contribution
    outflow = capex+oneoff
    fraction = (13-v['commissioning_month'])/12
    flows = [-outflow,net*fraction,net,net,net,net+v['year5_residual']]
    rate = v['discount_rate']
    npv = sum(cf/(1+rate)**year for year,cf in enumerate(flows))
    pv_future = npv+outflow
    weighted_years = fraction/(1+rate)+sum(1/(1+rate)**year for year in range(2,6))
    required_gross = (outflow-v['year5_residual']/(1+rate)**5)/weighted_years+upkeep
    avoidable_per_kg = price_per_kg+o['process_kwh_per_input_kg']*o['electricity_per_kwh']+o['disposal_per_kg']
    required_input_reduction = required_gross/avoidable_per_kg
    allowed_input = baseline['input_kg']-required_input_reduction
    threshold = 1-good_kg/allowed_input if allowed_input>0 else None
    payback = outflow/net*12 if net>0 else None
    depreciation = capex/v['asset_life_years']
    return {
        'annualBottles':bottles,'baselineCostPerBottle':baseline['total_cost']/bottles,
        'proposalCostPerBottle':(proposal['total_cost']+upkeep+depreciation)/bottles,
        'inputAvoided':baseline['input_kg']-proposal['input_kg'],
        'grossSaving':gross,'netSaving':net,'capex':capex,'initialEconomicOutflow':outflow,
        'npv':npv,'paybackMonths':payback,
        'calendarPaybackMonths':payback+v['commissioning_month']-1 if payback is not None else None,
        'year1ProfitBenefit':(net-depreciation)*fraction-oneoff,
        'breakEvenLoss':threshold,
        'maxEquipment':(pv_future-oneoff)/(1+v['contingency'])-v['installation']-v['validation'],
        'cashFlows':flows,
        'baselineMassBalanceDifference':baseline['input_kg']-good_kg-baseline['loss_kg'],
        'proposalMassBalanceDifference':proposal['input_kg']-good_kg-proposal['loss_kg'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs',type=Path,default=DEFAULT_INPUT)
    args = parser.parse_args()
    inputs = json.loads(args.inputs.read_text(encoding='utf-8'))
    results = calculate(inputs)
    downside = deepcopy(inputs)
    downside['investment']['target_loss'] = 0.025
    results['downsideNPV'] = calculate(downside)['npv']
    print(json.dumps(results,indent=2))


if __name__ == '__main__':
    main()
