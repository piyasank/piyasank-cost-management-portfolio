"""Compare illustrative December decisions against the November forecast."""

import json
from copy import deepcopy

from model import ROOT, forecast, simulate


def evaluate(inputs):
    costs = forecast(inputs)
    risks = simulate(inputs)
    return {
        "known_forecast": costs["known_forecast"],
        "expected_forecast": costs["expected_forecast"],
        "residual_risk_emv": costs["residual_risk_emv"],
        "p80": risks["p80"],
        "p80_gap": risks["p80_funding_gap"],
    }


def compare(baseline):
    deferred = deepcopy(baseline)
    handover = next(item for item in deferred["unlet"] if item["id"] == "U03")
    # Retain £20k of handover-critical scope. Track deferred costs separately.
    handover["rate"] -= 20_000

    combined = deepcopy(baseline)
    doors = next(item for item in combined["changes"] if item["id"] == "CO09")
    doors.update(status="Approved", agreed=doors["forecast"])
    mep = next(item for item in combined["packages"] if item["id"] == "WP03")
    mep["base_forecast_adjustment"] += -20_000 + 8_000
    access = next(item for item in combined["risks"] if item["id"] == "R02")
    unmitigated = evaluate(combined)
    access["probability"] = 0.10

    return {
        "retain_scope": evaluate(baseline),
        "defer_enhanced_training": evaluate(deferred),
        "combine_scope_and_mitigation": evaluate(combined),
        "combined_with_access_risk_unchanged": unmitigated,
    }


if __name__ == "__main__":
    inputs = json.loads((ROOT / "data" / "november-inputs.json").read_text(encoding="utf-8"))
    print(json.dumps(compare(inputs), indent=2))
