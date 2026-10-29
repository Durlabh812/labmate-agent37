# Agent37 execution record

Observed on 29 October 2026. The LabMate source ZIP was attached to a task in a Free Hermes agent on Agent37. The hosted agent extracted it and ran:

```
python3 -m unittest discover -s tests -v
python3 labmate.py samples/synthetic_readings.csv --synthetic --out agent37_output
```

Observed result: 13 tests passed. The saved analysis.json was opened independently through the Agent37 file viewer and showed synthetic=true, 20 input rows, 16 included rows and 4 excluded rows. The excluded rows were a missing value, a nonfinite value, and both rows with a duplicated reading_id. Moisture % and g/g were separate groups. The generated HTML file was also opened and its saved content inspected. This is a synthetic demonstration, not a completed food experiment or predictive adulteration study.

No paid plan, card, top-up, external API key or personal-service integration was used. The instance was created using the approved Free allowance. Usage page at 18:36 IST listed $0.003144 for the first run's eight model calls, within the included $0.20 allowance. Usage can update later; this is a timestamped observation, not a final billing total.

Private account dashboard evidence is held separately, not committed here. A public project entry has not yet been submitted.
