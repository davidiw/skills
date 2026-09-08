"""Render the local synthetic page; no server, provider or network is needed."""
from pathlib import Path
import argparse, os, shutil, signal, subprocess, tempfile
p=argparse.ArgumentParser()
p.add_argument('--width',type=int,default=390)
p.add_argument('--height',type=int,default=844)
p.add_argument('--state',default='normal')
p.add_argument('--output',default='renders/current.png')
a=p.parse_args()
chrome=os.environ.get('EXPERIENCE_CHROMIUM') or shutil.which('chrome-headless-shell') or shutil.which('chromium') or shutil.which('google-chrome')
if not chrome: raise SystemExit('Chromium unavailable; report rendering unavailable.')
out=Path(a.output).resolve();out.parent.mkdir(parents=True,exist_ok=True)
url=Path('index.html').resolve().as_uri()+'?state='+a.state
with tempfile.TemporaryDirectory() as profile:
 process=subprocess.Popen([chrome,'--headless','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--no-proxy-server','--disable-background-networking','--host-resolver-rules=MAP * ~NOTFOUND','--user-data-dir='+profile,'--hide-scrollbars','--window-size='+str(a.width)+','+str(a.height),'--screenshot='+str(out),'--virtual-time-budget=1000',url],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
 try:
  stdout,stderr=process.communicate(timeout=35)
 except subprocess.TimeoutExpired:
  raise SystemExit('Rendering timed out; no verification claimed.')
 finally:
  try:os.killpg(process.pid,signal.SIGKILL)
  except ProcessLookupError:pass
  process.wait()
 if process.returncode or not out.is_file():raise SystemExit('Rendering failed: '+stderr[-1200:])
print(str(out))
