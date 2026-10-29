# LabMate - Experimental Data-to-Report Agent

A small experimental CSV validator and descriptive-report generator, with a genuine synthetic-data run completed on Agent37.

## Run the project

Download `LabMate_Source.zip` from this repository and extract it. Open a terminal in its `LabMate` folder. Requires Python 3.10+ and no third-party packages.

```
python app.py
```

Open http://127.0.0.1:8765 for the local upload interface. Download the synthetic example in the app, upload it, and keep the synthetic-data label selected.

For saved HTML and JSON outputs:

```
python labmate.py samples/synthetic_readings.csv --synthetic --out output
python -m unittest discover -s tests -v
```

The source archive includes the application, analysis code, tests, synthetic CSV, generated example report, workflow instructions and `AGENT37_RUN.md`. It preserves the folder structure needed to run the tests and sample.

## Genuine Agent37 use

A hosted Hermes agent received the source, ran the tests, analyzed the synthetic CSV and saved the HTML report and JSON validation log in its own computer on 29 October 2026. All 13 tests passed. The sample had 20 input rows, 16 included and 4 excluded with recorded reasons. The saved analysis and report were independently inspected. The archive's `demo_output` is the local example; private dashboard evidence and the hosted output remain separate.

## Data and scientific limits

The six required columns are `reading_id,sample_id,group,parameter,value,unit`. A reading ID must be unique; one physical sample may have several readings. Missing/nonfinite values and duplicated reading IDs are excluded with explicit reasons. Different unit labels stay separate, with no guessed conversions. Statistics are descriptive, and n counts readings rather than independent samples. No tea-adulteration diagnosis, experimental results, significance or causal effects are claimed. All sample data is synthetic.

No real lab data, credentials or private account screenshots are stored here. No paid subscription or top-up was used. The project has not been submitted to the challenge. This repository is private pending review.
