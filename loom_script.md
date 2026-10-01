# Loom video script - about 2 minutes 45 seconds

Read the quoted text. The "Show" lines are screen directions, not spoken text.
Open solve.py, metrics.json, validation_predictions.csv, and the December chart
before recording. Speak slowly and use your own wording where it feels natural.

## 0:00-0:30 - Task and data

Show: the GitHub repository, then metrics.json.

"Hi, this is my Spotter freight-rate assessment. I kept the solution simple:
one time split, one baseline, one additional model, and one error metric.

The data has 48,000 labeled loads from January to October 2025. There are
300 missing weights and 374 missing market indices. There are no duplicate
load IDs or missing target prices. I kept extreme prices because I had no
evidence that they were wrong."

## 0:30-1:00 - Split and cleaning

Show: the train and test lines in main(), then make_model().

"I trained on January through June and tested on July through October.
That gives 28,806 training rows and 19,194 test rows. Using later dates for
testing checks how the model performs on future loads.

Missing weights are filled with the training median: 31,400 pounds.
The pipeline also learns scaling and category encoding from training only.
I fit it before predicting the test set, which prevents test-data leakage."

## 1:00-1:35 - Baseline and model

Show: baseline_price and baseline_mae, then make_model().

"First, my baseline predicts the training median price, 2,022 dollars and
89 cents, for every load. Its MAE is 1,138 dollars and 46 cents.
MAE means the average absolute dollar error. Lower is better.

Then I added one model: Ridge, which is linear regression with a small
fixed penalty. It uses distance, weight, pickup, delivery, equipment, and
weekday. I chose these inputs because they are also available for December.
I did not run a model search or tune lots of settings."

## 1:35-2:05 - Results and prediction code

Show: metrics.json, then final_model.fit and the template mapping in solve.py.

"The linear model's test MAE is 143 dollars and 78 cents, about 87 percent
lower than the baseline. So I selected it.

After evaluation, I refit it on all January-to-October labeled data to make
the final predictions. This does not change the earlier test result.
The code matches predictions to the template by load ID and saves the CSV."

## 2:05-2:45 - Outputs and limitations

Show: validation_predictions.csv, then scorer_results/candidate_december.png.

"The supplied scorer accepted all 12,000 final predictions and all 31
December rows. It checks the files and creates this chart; it does not
measure the hidden November accuracy.

For December, the route and other inputs stay fixed. Only the date changes.
My model uses weekday, so the chart repeats a weekly pattern. It does not
capture holiday demand or monthly seasonality.

The public repository includes the code, dependencies, prediction CSV,
report, and run instructions. Thank you."
