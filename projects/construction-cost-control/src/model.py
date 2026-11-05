"""Client cost-control model and seeded Monte Carlo analysis of synthetic data.

Run from any directory. No third-party packages are required.
"""
import argparse
import json
import math
import random
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / 'data' / 'project-inputs.json'


def validate(c):
    ids = [p['id'] for p in c['packages']]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate package IDs')
    for key in ['changes', 'unlet', 'risks']:
        items=c[key]
        if len({x['id'] for x in items}) != len(items):
            raise ValueError('Duplicate '+key+' IDs')
        if any(x['package'] not in ids for x in items):
            raise ValueError('Unknown package in '+key)
    if c['original_contingency'] < 0 or c['pending_change_factor'] < 0 or c['prolongation_per_week'] < 0:
        raise ValueError('Contingency, forecast factor and prolongation rate must be nonnegative')
    if not math.isclose(sum(x['probability'] for x in c['delay_states']),1,abs_tol=1e-9):
        raise ValueError('Delay probabilities must sum to one')
    if any(not 0 <= x['probability'] <= 1 or x['weeks'] < 0 for x in c['delay_states']):
        raise ValueError('Invalid delay distribution')
    change_ids={x['id'] for x in c['changes']}
    for r in c['risks']:
        if not 0 <= r['probability'] <= 1 or not 0 <= r['low'] <= r['mode'] <= r['high']:
            raise ValueError('Invalid risk distribution')
        if r['change_id'] and r['change_id'] not in change_ids:
            raise ValueError('Unknown risk/change link')
    for x in c['changes']:
        if x['status'] not in ['Approved','Pending','Rejected','Opportunity']:
            raise ValueError('Unknown change status')
        date.fromisoformat(x['date'])
    for x in c['unlet']:
        if x['quantity'] < 0 or x['rate'] < 0:
            raise ValueError('Unlet quantities and rates must be nonnegative')
    date.fromisoformat(c['as_of'])


def forecast(c):
    validate(c)
    effective=[x for x in c['changes'] if x['date'] <= c['as_of']]
    approved=[x for x in effective if x['status']=='Approved']
    pending=[x for x in effective if x['status']=='Pending']
    covered={x['id'] for x in effective if x['status'] in ['Approved','Pending']}
    rows=[]
    for p in c['packages']:
        approved_value=sum(x['agreed'] for x in approved if x['package']==p['id'])
        pending_value=sum(x['forecast'] for x in pending if x['package']==p['id'])*c['pending_change_factor']
        committed=p['award']+approved_value
        incurred=p['certified']+p['accrual']
        if any(p[k] < 0 for k in ['budget','award','certified','accrual']) or incurred > committed:
            raise ValueError('Invalid cost recognition or overdrawn commitment in '+p['id'])
        outstanding=committed-incurred
        unlet=sum(x['quantity']*x['rate'] for x in c['unlet'] if x['package']==p['id'])
        known=incurred+outstanding+unlet+p['base_forecast_adjustment']+pending_value
        budget=p['budget']+approved_value
        rows.append({'id':p['id'],'description':p['description'],'original_budget':p['budget'],
                     'approved_changes':approved_value,'current_budget':budget,'current_commitment':committed,
                     'certified':p['certified'],'accrual':p['accrual'],'incurred':incurred,
                     'outstanding_commitment':outstanding,'unlet':unlet,
                     'base_adjustment':p['base_forecast_adjustment'],'pending_changes':pending_value,
                     'known_forecast':known,'variance_to_current_budget':known-budget})
    active=[r for r in c['risks'] if r['change_id'] not in covered]
    excluded=[r['id'] for r in c['risks'] if r['change_id'] in covered]
    event_risk=sum(r['probability']*(r['low']+r['mode']+r['high'])/3 for r in active)
    delay_risk=sum(s['weeks']*s['probability'] for s in c['delay_states'])*c['prolongation_per_week']
    total=lambda key:sum(r[key] for r in rows)
    funding=c['approved_funding']
    known=total('known_forecast')
    expected=known+event_risk+delay_risk
    return {'as_of':c['as_of'],'funding':funding,'original_base_budget':total('original_budget'),
            'approved_changes':total('approved_changes'),'current_allocated_budget':total('current_budget'),
            'remaining_unallocated_contingency':c['original_contingency']-total('approved_changes'),
            'certified':total('certified'),'accrual':total('accrual'),'incurred':total('incurred'),
            'current_commitment':total('current_commitment'),'outstanding_commitment':total('outstanding_commitment'),
            'unlet':total('unlet'),'base_adjustment':total('base_adjustment'),'pending_changes':total('pending_changes'),
            'known_forecast':known,'funding_before_residual_risk':funding-known,
            'event_risk_emv':event_risk,'delay_risk_emv':delay_risk,'residual_risk_emv':event_risk+delay_risk,
            'expected_forecast':expected,'expected_headroom':funding-expected,
            'excluded_risk_ids':excluded,'effective_change_ids':[x['id'] for x in effective],
            'packages':rows}


def quantile(sorted_values, p):
    position=(len(sorted_values)-1)*p
    left=int(position)
    right=min(left+1,len(sorted_values)-1)
    return sorted_values[left]+(sorted_values[right]-sorted_values[left])*(position-left)


def simulate(c, trials=None, seed=None):
    f=forecast(c)
    trials=c['simulation_trials'] if trials is None else trials
    seed=c['simulation_seed'] if seed is None else seed
    if not isinstance(trials,int) or trials < 100:
        raise ValueError('At least 100 integer simulation trials required')
    rng=random.Random(seed)
    active=[r for r in c['risks'] if r['id'] not in f['excluded_risk_ids']]
    draws=[]
    for _ in range(trials):
        total=f['known_forecast']
        for r in active:
            if rng.random() < r['probability']:
                impact=r['low'] if r['low']==r['high'] else rng.triangular(r['low'],r['high'],r['mode'])
                total+=impact
        draw=rng.random()
        cumulative=0
        for state in c['delay_states']:
            cumulative+=state['probability']
            if draw < cumulative:
                total+=state['weeks']*c['prolongation_per_week']
                break
        draws.append(total)
    values=sorted(draws)
    mean=sum(values)/trials
    sample_sd=math.sqrt(sum((x-mean)**2 for x in values)/(trials-1))
    bins=Counter(min(19,int((x-f['known_forecast'])/25000)) for x in values)
    return {'trials':trials,'seed':seed,'mean':mean,'p50':quantile(values,.5),'p80':quantile(values,.8),
            'p90':quantile(values,.9),'p95':quantile(values,.95),
            'probability_over_budget':sum(x>f['funding'] for x in values)/trials,
            'p80_funding_gap':max(0,quantile(values,.8)-f['funding']),
            'sample_standard_error':sample_sd/math.sqrt(trials),
            'histogram':[{'lower':f['known_forecast']+k*25000,'upper':f['known_forecast']+(k+1)*25000,'count':bins[k]} for k in range(20)]}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs',type=Path,default=INPUTS)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    c=json.loads(args.inputs.read_text(encoding='utf-8-sig'))
    result={'forecast':forecast(c),'simulation':simulate(c)}
    text=json.dumps(result,indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text+'\n',encoding='utf-8')
    else:
        print(text)

if __name__=='__main__':main()
