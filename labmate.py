#!/usr/bin/env python3
"""LabMate: deterministic, offline CSV validation and descriptive reporting."""
import argparse, csv, html, io, json, math, statistics
from pathlib import Path
from collections import Counter, defaultdict

REQUIRED = ['reading_id', 'sample_id', 'group', 'parameter', 'value', 'unit']

def analyze(text, synthetic=False):
    reader = csv.DictReader(io.StringIO(text.lstrip('\ufeff')))
    if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
        raise ValueError('CSV must have unique column names.')
    missing = set(REQUIRED) - set(reader.fieldnames)
    if missing:
        raise ValueError('Missing required columns: ' + ', '.join(sorted(missing)))
    records = list(reader)
    if not records:
        raise ValueError('CSV has no data rows.')
    if len(records) > 10000:
        raise ValueError('Maximum 10,000 rows per analysis.')
    issues, valid, candidates = [], [], []
    for line, row in enumerate(records, 2):
        if None in row:
            issues.append({'line': line, 'severity': 'error', 'message': 'Too many cells in row; row excluded.'})
            continue
        row = {k: (v or '').strip() for k, v in row.items()}
        absent = [k for k in REQUIRED if not row.get(k)]
        if absent:
            issues.append({'line': line, 'severity': 'error', 'message': 'Missing ' + ', '.join(absent) + '; row excluded.'})
            continue
        try:
            value = float(row['value'])
            if not math.isfinite(value):
                raise ValueError()
        except ValueError:
            issues.append({'line': line, 'severity': 'error', 'message': 'Value must be a finite number; row excluded.'})
            continue
        row['value'] = value
        row['line'] = line
        candidates.append(row)
    counts = Counter(r['reading_id'] for r in candidates)
    for row in candidates:
        if counts[row['reading_id']] > 1:
            issues.append({'line': row['line'], 'severity': 'error', 'message': 'Repeated reading_id ' + row['reading_id'] + '; all rows with this ID excluded. Use a unique reading_id for every reading; sample_id may repeat across parameters or technical replicates.'})
        else:
            valid.append(row)
    units = defaultdict(set)
    groups = defaultdict(list)
    for row in valid:
        units[row['parameter']].add(row['unit'])
        groups[(row['group'], row['parameter'], row['unit'])].append(row['value'])
    for parameter, choices in units.items():
        if len(choices) > 1:
            issues.append({'line': None, 'severity': 'warning', 'message': 'Multiple unit labels for ' + parameter + ': ' + ', '.join(sorted(choices)) + '. Kept separate; no conversion assumed.'})
    summaries = []
    for (group, parameter, unit), values in sorted(groups.items()):
        summaries.append(dict(group=group, parameter=parameter, unit=unit, n=len(values), mean=statistics.mean(values), median=statistics.median(values), sample_sd=statistics.stdev(values) if len(values)>1 else None, minimum=min(values), maximum=max(values)))
    return dict(synthetic=synthetic, input_rows=len(records), included_rows=len(valid), excluded_rows=len(records)-len(valid), issues=issues, summaries=summaries)

def render(result):
    esc = lambda v: html.escape(str(v), quote=True)
    fmt = lambda v: 'Not available (n=1)' if v is None else f'{v:.4g}'
    rows = ''.join('<tr>'+''.join('<td>'+esc(v)+'</td>' for v in [r['group'],r['parameter'],r['unit'],r['n'],fmt(r['mean']),fmt(r['median']),fmt(r['sample_sd']),fmt(r['minimum']),fmt(r['maximum'])])+'</tr>' for r in result['summaries'])
    issues = ''.join('<li><strong>'+esc(i['severity'].title())+'</strong> '+ ('Row '+str(i['line'])+': ' if i['line'] else '')+esc(i['message'])+'</li>' for i in result['issues']) or '<li>No structural issues found. Scientific validity is not established by this check.</li>'
    charts = ''
    pairs = sorted(set((r['parameter'],r['unit']) for r in result['summaries']))
    for parameter, unit in pairs:
        values = [r for r in result['summaries'] if (r['parameter'],r['unit']) == (parameter,unit)]
        scale = max([abs(r['mean']) for r in values]+[1e-12])
        bars = ''.join('<div class="barrow"><span>'+esc(r['group'])+'</span><div class="track"><div class="bar" style="width:'+str(abs(r['mean'])/scale*100)+'%"></div></div><strong>'+esc(fmt(r['mean']))+'</strong></div>' for r in values)
        charts += '<section><h2>'+esc(parameter)+' <small>('+esc(unit)+')</small></h2><p>Group means. Bar length shows absolute magnitude; signed values appear at right. No unit conversion.</p>'+bars+'</section>'
    label = 'Synthetic demonstration data - not experimental evidence.' if result['synthetic'] else 'User-supplied data - source and scientific validity not independently verified.'
    return '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>LabMate analysis report</title><style>
body{margin:0;background:#f4efec;color:#251f21;font:16px/1.6 system-ui,sans-serif}main{max-width:1000px;margin:auto;padding:32px 24px;background:white;min-height:100vh}h1{font:36px/1.15 Georgia,serif;margin:6px 0 16px}h2{font:24px/1.3 Georgia,serif}small,p{color:#585254}section{padding:20px 0;border-bottom:1px solid #eae9ea}.notice{background:#f4efec;padding:16px;border-radius:8px}.stats{display:flex;gap:24px;flex-wrap:wrap}.stats>div{margin-right:24px}.stats b{display:block;font-size:28px;color:#467b6d}.scroll{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;padding:10px;border-bottom:1px solid #eae9ea;white-space:nowrap}.barrow{display:grid;grid-template-columns:minmax(80px,1fr) 3fr 70px;gap:12px;align-items:center;margin:14px 0}.track{background:#f4efec;height:18px}.bar{background:#73a89a;height:100%}li{margin-bottom:12px}code{overflow-wrap:anywhere}@media(max-width:500px){main{padding:24px 16px}h1{font-size:30px}.barrow{grid-template-columns:80px 1fr 55px;font-size:13px}}
</style><main><small>LABMATE / PRIVATE PROTOTYPE</small><h1>Experimental data, with an audit trail.</h1><p class="notice">'''+label+'''</p><section class="stats"><div><b>'''+str(result['input_rows'])+'''</b>Input rows</div><div><b>'''+str(result['included_rows'])+'''</b>Included</div><div><b>'''+str(result['excluded_rows'])+'''</b>Excluded and logged</div></section><section><h2>Validation log</h2><ul>'''+issues+'''</ul></section>'''+charts+'''<section><h2>Descriptive statistics</h2><p>Scroll the supplemental table horizontally if needed. SD is sample standard deviation (n-1).</p><div class="scroll"><table><thead><tr><th>Group</th><th>Parameter</th><th>Unit</th><th>n</th><th>Mean</th><th>Median</th><th>Sample SD</th><th>Min</th><th>Max</th></tr></thead><tbody>'''+rows+'''</tbody></table></div></section><section><h2>Interpretation limits</h2><p>n counts readings, not independent physical samples. Repeated sample_id values across parameters or technical replicates are allowed; reading_id must be unique. Descriptive analysis only. No causal claims, hypothesis tests, adulteration diagnosis, automatic unit validation against a scientific standard, or invented experimental conclusions. Unit labels are compared literally. Independence of replicates and experimental design require human review.</p><p>This report contains synthetic data. It records descriptive output only; execution provenance must be documented separately.</p></section></main></html>'''

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_file', type=Path)
    parser.add_argument('--out', type=Path, default=Path('output'))
    parser.add_argument('--synthetic', action='store_true', help='Label every output as synthetic demonstration data')
    args=parser.parse_args()
    try:
        result=analyze(args.csv_file.read_text(encoding='utf-8-sig'),args.synthetic)
    except (ValueError, OSError, csv.Error) as error:
        parser.exit(2, str(error)+'\n')
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'analysis.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    (args.out/'validation_log.json').write_text(json.dumps(result['issues'],indent=2)+'\n')
    (args.out/'report.html').write_text(render(result))
    print(f'Created report.html, analysis.json and validation_log.json in {args.out}. Included {result["included_rows"]}/{result["input_rows"]} rows.')

if __name__=='__main__': main()
