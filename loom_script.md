# Simple 2-3 minute recording script

## 0:00-0:30 - The task and data

"I built a simple freight-price prediction solution. There are 48,000 labeled
loads covering January through October 2025. We need to predict 12,000 loads
from November and create a December chart for one fixed route.

There are 300 missing weights and 374 missing market indices. There are no
missing target prices or duplicate load IDs. I kept extreme prices because
I had no evidence they were incorrect."

## 0:30-1:00 - Split and missing values

Show the split in solve.py.

"I trained on January through June and tested on July through October.
This checks how well the model predicts later loads. I filled missing weights
using only the training median, which was 31,400 pounds. The preprocessing
pipeline learns all its statistics from training, so test data cannot leak in."

## 1:00-1:40 - Baseline and one model

Show metrics.json, then make_model in solve.py.

"First, I predicted the training median price, $2,022.89, for every test load.
Its MAE was $1,138.46. MAE is the average absolute dollar error.

Next, I added one linear model called Ridge. It uses distance, weight, pickup,
delivery, equipment, and weekday. I used these inputs because they are available
in both prediction files. Its test MAE was $143.78, about 87 percent lower.
I did not search across models or tune many settings."

## 1:40-2:20 - Final files and limits

Show the output CSV and candidate_december.png.

"After measuring test performance, I trained the selected model on all labeled
January-through-October data and generated the final predictions. The supplied
scorer accepted all 12,000 predictions and all 31 December rows.

For December, only the date changes. My model uses weekday, so the chart repeats
a weekly pattern. It does not model holiday or monthly demand changes. The
November labels are hidden, so I cannot report the final November accuracy.
The README has the commands to reproduce the solution."
