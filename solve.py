"""One time split, one baseline, one linear model, one metric."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
NUMERIC = ["distance", "weight"]
CATEGORICAL = ["pickup", "delivery", "equipment", "weekday"]


def features(frame):
    result = frame.copy()
    result["weekday"] = pd.to_datetime(result["date"]).dt.day_name()
    return result[NUMERIC + CATEGORICAL]


def make_model():
    preprocessing = ColumnTransformer([
        ("numbers", make_pipeline(SimpleImputer(strategy="median"),
                                  StandardScaler()), NUMERIC),
        ("categories", make_pipeline(SimpleImputer(strategy="most_frequent"),
                                     OneHotEncoder(handle_unknown="ignore")),
         CATEGORICAL),
    ])
    # Ridge is linear regression with a small fixed penalty; no tuning/search.
    return make_pipeline(preprocessing, Ridge(alpha=1.0, solver="lsqr"))


def main():
    labeled = pd.read_csv(DATA / "train-test.csv")
    dates = pd.to_datetime(labeled["date"])
    train = labeled.loc[dates.between("2025-01-01", "2025-06-30")]
    test = labeled.loc[dates.between("2025-07-01", "2025-10-31")]
    assert len(train) + len(test) == len(labeled)
    assert dates.loc[train.index].max() < dates.loc[test.index].min()
    assert labeled["load_id"].is_unique
    assert labeled["posted_rate"].notna().all()

    # Step 1: understand the baseline before fitting another model.
    baseline_price = float(train["posted_rate"].median())
    baseline_mae = mean_absolute_error(
        test["posted_rate"], np.full(len(test), baseline_price))
    print(f"Baseline: always predict ${baseline_price:,.2f}")
    print(f"Baseline July-October MAE: ${baseline_mae:,.2f}")

    # Step 2: preprocessing learns statistics from January-June only.
    model = make_model()
    model.fit(features(train), train["posted_rate"])
    # Positive rates are required by the supplied scorer.
    model_prediction = np.maximum(1.0, model.predict(features(test)))
    model_mae = mean_absolute_error(test["posted_rate"], model_prediction)
    print(f"Linear model July-October MAE: ${model_mae:,.2f}")
    winner = "linear model" if model_mae < baseline_mae else "median baseline"

    results = {
        "training_rows": len(train), "test_rows": len(test),
        "training_period": "2025-01-01 to 2025-06-30",
        "test_period": "2025-07-01 to 2025-10-31",
        "baseline_price": baseline_price,
        "baseline_mae": float(baseline_mae), "linear_model_mae": float(model_mae),
        "improvement_percent": float(100 * (baseline_mae-model_mae)/baseline_mae),
        "selected_model": winner,
        "missing_values": labeled.isna().sum().to_dict(),
        "training_weight_median": float(train["weight"].median()),
        "development_min_rate": float(labeled["posted_rate"].min()),
        "development_max_rate": float(labeled["posted_rate"].max()),
    }

    # Evaluation is finished. Refit the winner on all labeled development data
    # to predict November/December. This does not change the reported test MAE.
    if winner == "linear model":
        final_model = make_model()
        final_model.fit(features(labeled), labeled["posted_rate"])

    def predict(frame):
        if winner == "linear model":
            return np.maximum(1.0, final_model.predict(features(frame)))
        return np.full(len(frame), labeled["posted_rate"].median())

    validation = pd.read_csv(DATA / "validation.csv")
    template = pd.read_csv(DATA / "validation-predictions-template.csv")
    assert validation["load_id"].is_unique and template["load_id"].is_unique
    assert set(validation["load_id"]) == set(template["load_id"])
    by_id = pd.Series(predict(validation), index=validation["load_id"])
    template["predicted_rate"] = template["load_id"].map(by_id)
    template.to_csv(ROOT / "validation_predictions.csv", index=False)
    december = pd.read_csv(DATA / "december-chart-inputs.csv")
    december["predicted_rate"] = predict(december)
    december.to_csv(ROOT / "december_predictions.csv", index=False)
    (ROOT / "metrics.json").write_text(json.dumps(results, indent=2))
    print(f"Selected: {winner}. Saved November and December predictions.")


if __name__ == "__main__":
    main()
