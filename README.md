# LabMate - Experimental Data-to-Report Agent

Private working prototype for review. A genuine Agent37 run was completed on 29 October 2026 with the synthetic sample. No publication or challenge submission has been completed. Python 3.10+; no third-party packages or model/API calls required for local execution.

## Run

Download or clone this repository. Open a terminal in the project folder:

```
python app.py
```

Open http://127.0.0.1:8765. Download the synthetic example, upload it and keep the synthetic-data checkbox selected. The app runs only on your own machine. Reload the home URL to upload another file.

For saved output files instead:

```
python labmate.py samples/synthetic_readings.csv --synthetic --out output
python -m unittest discover -s tests -v
```

Open `output/report.html`. The other outputs are `analysis.json` and `validation_log.json`. `demo_output` contains a pre-generated local run with the synthetic sample: 20 rows, 16 included and 4 excluded with explicit reasons. A mixed-unit warning keeps g/g and % separate.

## Data contract

Required columns: reading_id, sample_id, group, parameter, value, unit. Use a unique reading_id per row; sample_id identifies the physical sample and may repeat across parameters or technical replicates. Repeated sample IDs do not establish independent replicates. Non-empty metadata and finite numeric values required. Multiple rows with the same reading_id are all excluded conservatively. Repeated sample_id values are allowed. n counts readings, not independent physical samples. Mixed unit labels are warned and kept separate. No scientific unit conversion or automatic judgement of plausible values is made. Reports escape CSV strings as text.

Inputs may contain personal or confidential research information. Keep them local and do not put them in a public repository. The supplied example is synthetic and contains no participant information. This is a localhost development server, not a production internet-facing service.

## Agent37 role

See `agent37/WORKFLOW.md`. Intended product: the hosted agent accepts a file-analysis task, runs the same Python analysis in its Agent37 computer, inspects outputs, and returns the report and validation log. Agent37 runs the task, not merely writes the code. The workflow was executed on the approved Free instance on 29 October 2026. See AGENT37_RUN.md for observed results.

## Limits

Descriptive summaries only: n, mean, median, sample standard deviation (n-1), minimum, maximum. No adulteration detection, inferred causal effects, predictive model or significance testing. No claim that synthetic trends describe real tea. Group/parameter/unit labels are literal; case and spelling differences remain separate. The user must establish sample independence and the experimental method. The prototype has no paid dependencies, always-on jobs, messaging integration or public web hosting.

## Project status

The synthetic workflow has been run on Agent37. This repository contains code, synthetic examples and a run record, not private account screenshots or real laboratory data. No challenge submission has been completed.
