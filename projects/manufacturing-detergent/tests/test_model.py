import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from model import calculate

class InvestmentCaseTests(unittest.TestCase):
    def setUp(self):
        self.config=json.loads((ROOT/'model/assumptions.json').read_text())
        self.expected=json.loads((ROOT/'model/published-results.json').read_text())

    def test_published_workbook_snapshot(self):
        result=calculate(self.config)
        for key in ['baselineCostPerBottle','proposalCostPerBottle','inputAvoided','grossSaving','netSaving','capex','initialEconomicOutflow','npv','paybackMonths','calendarPaybackMonths','year1ProfitBenefit','breakEvenLoss','maxEquipment']:
            with self.subTest(metric=key):self.assertAlmostEqual(result[key],self.expected[key],places=6)

    def test_mass_balance(self):
        r=calculate(self.config)
        self.assertAlmostEqual(r['baselineMassBalanceDifference'],0)
        self.assertAlmostEqual(r['proposalMassBalanceDifference'],0)

    def test_downside_reverses_decision(self):
        self.config['investment']['target_loss']=.025
        r=calculate(self.config)
        self.assertGreater(r['netSaving'],0)
        self.assertLess(r['npv'],0)
        self.assertAlmostEqual(r['npv'],self.expected['downsideNPV'],places=6)

    def test_break_even_threshold(self):
        threshold=calculate(self.config)['breakEvenLoss']
        self.config['investment']['target_loss']=threshold
        self.assertAlmostEqual(calculate(self.config)['npv'],0,places=6)

    def test_maximum_equipment_budget(self):
        maximum=calculate(self.config)['maxEquipment']
        self.config['investment']['equipment']=maximum
        self.assertAlmostEqual(calculate(self.config)['npv'],0,places=6)

    def test_no_process_improvement_has_no_gross_saving(self):
        self.config['investment']['target_loss']=self.config['production']['baseline_loss']
        r=calculate(self.config)
        self.assertAlmostEqual(r['grossSaving'],0)
        self.assertIsNone(r['paybackMonths'])

    def test_delayed_start_reduces_npv(self):
        before=calculate(self.config)['npv']
        self.config['investment']['commissioning_month']=10
        self.assertLess(calculate(self.config)['npv'],before)

    def test_no_year_one_savings_when_deferred(self):
        self.config['investment']['commissioning_month']=13
        self.assertEqual(calculate(self.config)['cashFlows'][1],0)

    def test_invalid_loss_rejected(self):
        self.config['investment']['target_loss']=1
        with self.assertRaises(ValueError):calculate(self.config)

    def test_invalid_material_mix_rejected(self):
        self.config['materials'][0]['mass_fraction']=.8
        with self.assertRaises(ValueError):calculate(self.config)

if __name__=='__main__':unittest.main()
