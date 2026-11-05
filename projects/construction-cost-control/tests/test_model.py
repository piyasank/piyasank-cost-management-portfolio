import json,sys,unittest
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from model import forecast,simulate

class CostControlTests(unittest.TestCase):
    def setUp(self):self.c=json.loads((ROOT/'data/project-inputs.json').read_text(encoding='utf-8-sig'))
    def test_forecast_reconciles(self):
        f=forecast(self.c)
        self.assertEqual(f['funding'],5000000)
        self.assertEqual(f['known_forecast'],4915000)
        self.assertEqual(f['incurred']+f['outstanding_commitment'],f['current_commitment'])
        self.assertEqual(f['current_allocated_budget']+f['remaining_unallocated_contingency'],f['funding'])
        self.assertAlmostEqual(f['expected_forecast'],4997400)
        self.assertAlmostEqual(f['expected_headroom'],2600)
    def test_approval_reclassifies_without_double_count(self):
        before=forecast(self.c)
        self.c['changes'][4]['status']='Approved'
        after=forecast(self.c)
        self.assertEqual(after['known_forecast'],before['known_forecast'])
        self.assertEqual(after['current_commitment']-before['current_commitment'],180000)
        self.assertEqual(after['pending_changes']-before['pending_changes'],-180000)
    def test_accrual_certification_is_not_new_cost(self):
        before=forecast(self.c)
        self.c['packages'][2]['certified']+=50000
        self.c['packages'][2]['accrual']-=50000
        after=forecast(self.c)
        self.assertEqual(after['incurred'],before['incurred'])
        self.assertEqual(after['known_forecast'],before['known_forecast'])
    def test_reporting_cutoff_excludes_future_instruction(self):
        before=forecast(self.c)
        self.assertNotIn('CO10',before['effective_change_ids'])
        self.c['as_of']='2026-11-05'
        after=forecast(self.c)
        self.assertEqual(after['known_forecast']-before['known_forecast'],100000)
    def test_unapproved_opportunity_not_deducted(self):
        before=forecast(self.c)
        self.c['changes'][8]['forecast']=-300000
        self.assertEqual(forecast(self.c)['known_forecast'],before['known_forecast'])
    def test_rejected_change_not_included(self):
        before=forecast(self.c)
        self.c['changes'][7]['forecast']=900000
        self.assertEqual(forecast(self.c)['known_forecast'],before['known_forecast'])
    def test_risk_already_in_change_is_excluded(self):
        f=forecast(self.c)
        self.assertEqual(f['excluded_risk_ids'],['R04'])
        self.c['risks'][3]['probability']=0
        self.assertEqual(forecast(self.c)['residual_risk_emv'],f['residual_risk_emv'])
    def test_no_remaining_commitment_double_count(self):
        self.c['packages'][0]['accrual']+=20000
        before=forecast(json.loads((ROOT/'data/project-inputs.json').read_text()))
        after=forecast(self.c)
        self.assertEqual(after['known_forecast'],before['known_forecast'])
        self.assertEqual(after['outstanding_commitment'],before['outstanding_commitment']-20000)
    def test_unlet_quantity_rate_change(self):
        before=forecast(self.c)
        self.c['unlet'][0]['rate']+=1000
        self.assertEqual(forecast(self.c)['known_forecast']-before['known_forecast'],3000)
    def test_duplicate_package_rejected(self):
        self.c['packages'][1]['id']='WP01'
        with self.assertRaises(ValueError):forecast(self.c)
    def test_unknown_scope_key_rejected(self):
        self.c['changes'][0]['package']='MISSING'
        with self.assertRaises(ValueError):forecast(self.c)
    def test_overdrawn_commitment_rejected(self):
        self.c['packages'][0]['accrual']=900000
        with self.assertRaises(ValueError):forecast(self.c)
    def test_invalid_risk_triangle_rejected(self):
        self.c['risks'][0]['mode']=999999
        with self.assertRaises(ValueError):forecast(self.c)
    def test_delay_probabilities_must_reconcile(self):
        self.c['delay_states'][0]['probability']=.9
        with self.assertRaises(ValueError):simulate(self.c,trials=100)
    def test_seed_reproduces_results(self):
        self.assertEqual(simulate(self.c,trials=500),simulate(self.c,trials=500))
    def test_no_risks_gives_degenerate_forecast(self):
        for r in self.c['risks']:r['probability']=0
        self.c['delay_states']=[{'weeks':0,'probability':1}]
        s=simulate(self.c,trials=500)
        self.assertEqual(s['p50'],forecast(self.c)['known_forecast'])
        self.assertEqual(s['p80'],s['p50'])
    def test_simulated_mean_matches_analytic_expectation(self):
        s=simulate(self.c)
        self.assertLess(abs(s['mean']-forecast(self.c)['expected_forecast']),4*s['sample_standard_error'])
        self.assertLessEqual(s['p50'],s['p80'])
        self.assertLessEqual(s['p80'],s['p90'])
        self.assertGreater(s['p80_funding_gap'],0)

if __name__=='__main__':unittest.main()
