#!/usr/bin/env python3
"""Local-only upload interface. No network services or model calls."""
import argparse, json, re
from http.server import BaseHTTPRequestHandler, HTTPServer
from labmate import analyze, render
PAGE='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>LabMate</title><style>body{font:16px/1.6 system-ui;color:#251f21;background:#f4efec;margin:0}main{max-width:720px;background:white;margin:40px auto;padding:32px;border-radius:16px}h1{font:40px Georgia}button{background:#467b6d;color:white;border:0;padding:14px 22px;font-size:16px;border-radius:5px;cursor:pointer}input{margin:12px 0;max-width:100%}code{overflow-wrap:anywhere}p{color:#585254}.notice{padding:16px;background:#f4efec}#error{color:#b41320}label{display:block}a{color:#32695a}@media(max-width:600px){main{margin:0;padding:24px 16px;border-radius:0}h1{font-size:34px}}</style><main><small>PRIVATE PROTOTYPE / NO MODEL CALLS</small><h1>LabMate</h1><p>Turn experimental readings into a checked report. Upload your CSV, inspect the validation log, then review the summary.</p><p class="notice">Local demo only. No Agent37 run has been completed. Sample data is synthetic, not evidence from tea experiments.</p><h2>Your data</h2><p>Required columns: <code>reading_id,sample_id,group,parameter,value,unit</code>. Each reading needs a unique reading_id. The same physical sample_id may have several readings. Unit labels are compared literally, not scientifically certified.</p><form id="upload"><label>CSV file <input id="file" type="file" accept=".csv,text/csv" required></label><label><input id="synthetic" type="checkbox" checked> Label as synthetic demonstration data</label><p><button>Validate and create report</button></p><p id="error" role="alert"></p></form><p><a href="/sample">Download synthetic example CSV</a></p><p>No data leaves this local application. Max file size 1 MB; max 10,000 rows. No automatic unit conversions, diagnostic claims or statistical significance claims.</p></main><script>document.getElementById('upload').onsubmit=async e=>{e.preventDefault();let f=document.getElementById('file').files[0];if(!f)return;let err=document.getElementById('error');err.textContent='';try{let r=await fetch('/analyze?synthetic='+document.getElementById('synthetic').checked,{method:'POST',headers:{'Content-Type':'text/csv'},body:await f.text()});let t=await r.text();if(!r.ok){err.textContent=t;return;}document.open();document.write(t);document.close();}catch(x){err.textContent='Analysis failed. Check that the local server is running.';}};</script></html>'''
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def send(self, body, status=200, kind='text/html; charset=utf-8'):
        b=body.encode('utf-8');self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(b)));self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(b)
    def do_GET(self):
        if self.path=='/': self.send(PAGE)
        elif self.path=='/sample':
            from pathlib import Path
            self.send((Path(__file__).parent/'samples/synthetic_readings.csv').read_text(),kind='text/csv; charset=utf-8')
        else: self.send('Not found',404,'text/plain')
    def do_POST(self):
        if self.path.split('?')[0]!='/analyze': return self.send('Not found',404,'text/plain')
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=1000000: raise ValueError('CSV must be between 1 byte and 1 MB.')
            result=analyze(self.rfile.read(length).decode('utf-8-sig'),synthetic=self.path=='/analyze?synthetic=true')
            self.send(render(result))
        except (ValueError,UnicodeError) as e:self.send(str(e),400,'text/plain; charset=utf-8')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8765);args=p.parse_args()
    print(f'Open http://127.0.0.1:{args.port}. Localhost only; Ctrl+C to stop.')
    HTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
