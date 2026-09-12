#!/usr/bin/env python3
"""Demo model: predicts the next temperature as the average of the last two readings.

Writes output/predict.json, a list of prediction records. Each record stores the
row index the prediction was made for; when that row later appears in
data/events.csv the actual value and error are filled in.
"""
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path("data") / "events.csv"
PREDICT_FILE = Path("output") / "predict.json"


def load_temps():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open(newline="") as f:
        return [float(r["temp_f"]) for r in csv.DictReader(f)]


def load_predictions():
    if not PREDICT_FILE.exists():
        return []
    with PREDICT_FILE.open() as f:
        return json.load(f)


def fill_actuals(predictions, temps):
    """Resolve any prediction whose target row now exists in the data."""
    for p in predictions:
        if p["actual"] is None and p["for_row"] < len(temps):
            p["actual"] = temps[p["for_row"]]
            p["error"] = round(p["predicted"] - p["actual"], 2)


def predict(temps):
    if not temps:
        return None
    last_two = temps[-2:]
    return round(sum(last_two) / len(last_two), 1)


def main():
    temps = load_temps()
    predictions = load_predictions()
    fill_actuals(predictions, temps)

    value = predict(temps)
    if value is None:
        print("No data yet; nothing to predict.")
    elif predictions and predictions[-1]["for_row"] == len(temps):
        print("Prediction for the next row already exists; not adding another.")
    else:
        predictions.append({
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "for_row": len(temps),
            "predicted": value,
            "actual": None,
            "error": None,
        })
        print(f"Predicted next temperature: {value} F")

    PREDICT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with PREDICT_FILE.open("w") as f:
        json.dump(predictions, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
