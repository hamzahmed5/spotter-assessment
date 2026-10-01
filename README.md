# Simple freight-rate solution

## Results

| Method | July-October MAE |
| --- | ---: |
| Predict the training median price ($2,022.89) | $1,138.46 |
| One linear model (Ridge) | $143.78 |

MAE means average absolute price error. Lower is better. The linear model
reduces this test error by 87.37%. These are internal test results, not the
hidden November score.

## The five rules

1. Train on January-June 2025 (28,806 loads). Test once on July-October
   2025 (19,194 loads). No random split or cross-validation.
2. Fill missing numeric inputs with training medians. Fill missing categories
   with the training's most common value. Fit all preprocessing on training
   only. The training weight median is 31,400 lb.
3. Start with one baseline: predict the training median price for every load.
   This gives us a simple reference and requires no input features.
4. Measure MAE on the later test period.
5. Add just one model: Ridge, a linear regression with a small fixed penalty.
   Compare its MAE with the baseline and keep the better one. No parameter search.

## Inputs and data quality

The model uses distance, weight, pickup, delivery, equipment, and weekday
(taken from date). Categories become simple indicator columns. Numeric inputs
are scaled using training statistics. Load ID is only used to match output rows.

There are 300 missing weights and 374 missing market indices in the 48,000
labeled rows. Market index, quote signal, and coordinates are left out because
the December inputs do not provide them. There are no missing targets or
duplicate load IDs. Observed rates range from $57.22 to $25,533.00; all are kept
because there is no evidence that extreme values are errors.

The supplied December inputs contain a fixed route, distance, equipment, and
weight. Only weekday changes in our model, so dates with the same weekday have
the same prediction. This is a simple model, not a full seasonal forecast.

After evaluation, refit on all January-October labels for final prediction.
At that point the whole development set is the training set: preprocessing
learns from it, never from November or December. Reported MAE remains the
earlier January-June / July-October result. Predicted prices are floored at $1
in both evaluation and final prediction to satisfy the scorer's positive-rate rule.

## Run

From this folder, with Python 3.10 or newer:

```sh
python -m pip install -r requirements.txt
python solve.py
python score.py --predictions validation_predictions.csv --december-predictions december_predictions.csv --output-dir scorer_results
```

The input files are in `data/`. The solution works relative to its own folder.

## Files

- `solve.py`: the complete baseline, model, evaluation, and prediction code.
- `metrics.json`: measured results and data-quality counts.
- `validation_predictions.csv`: all 12,000 final predictions in template order.
- `december_predictions.csv`: all 31 December rows with their original columns.
- `scorer_results/candidate_december.png`: chart created by the provided scorer.
- `report.pdf`: short assessment report including the chart.
- `loom_script.md`: a simple 2-3 minute recording script.

The provided scorer validates output format and generates the chart. It does
not calculate hidden November MAE. GitHub publication and a Loom recording
still need to be done by the submitter; this package provides the files and script.
