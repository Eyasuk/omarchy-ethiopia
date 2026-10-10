import base64
import subprocess
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "public/assets/graphics"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FORM_URL = "https://forms.gle/41W6YoqL9r8Uv5W59"
FORM_SHORT = "forms.gle/41W6YoqL9r8Uv5W59"

OMARCHY_MARK_PATH = "m1200 1200h-480v-80h400v-1040h-479.996v160h-400v720h720v-720h-80v-80h159.996v880h-400v160h-640v-1200h1200zm-1120-80h480v-80h-400l.004-400h-80.004zm0-560h80.004v-400h400v-80h-480.004z"

OMARCHY_WORDMARK_SVG = """<svg viewBox="0 0 1215 285" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
<path clip-rule="evenodd" fill-rule="evenodd" d="m720 120h-15v15h-14.998v14.999l-60.002.001v15.002l90-.002v.002h.002l-.002 89.998h-15v15h-13v15h-17v-89.998h-45v90l-45-.002v-89.998h-14.998v-30h14.998v-15.002h-14.998v-30.001h14.998v-75h15v-14.997h15v-15.002h105.002zm-90-.001h45v-74.997h-45z"/>
<path clip-rule="evenodd" fill-rule="evenodd" d="m105 30.002h15v14.997h15v180.001h-15v15h-15v15.002h-75v-15.002h-15v-15h-15v-180.001h15v-14.997h15v-15.002h75zm-60 194.998h45v-179.998h-45z"/>
<path d="m300 15h60v15h15v14.999h15v180.001h-15v15h-15v15h-15l-.004-209.998h-44.994v-.002h-.002v210.002h-45v-210h-44.998v179.997h-.002v30.003h-15v-15.002h-15v-15h-14.998v-180.001h14.998v-14.999h15v-15h60v-15h45z"/>
<path clip-rule="evenodd" fill-rule="evenodd" d="m555 225h-15v15h-15v15h-15v-105.001l-44.998.001v105.002h-45.002v-105.002h-15v-30.001h15v-75h15.002v-14.997h15v-15.002h105zm-89.998-105.001h44.998v-74.997h-44.998z"/>
<path d="m885 75h-15v15h-15v15h-15v-59.998h-45v179.998h45v-59.998h15v14.997h15v15.001h15v30h-15v15h-15v15.002l-105-.002v-210.001h14.998v-14.997h15.002v-15.002h105z"/>
<path d="m960 119.999h45v-104.999h15v15h15v14.999h15v75.001h15v15h-15v90h-15v15h-15v15h-15v-105h-45v105.002l-45-.002v-105h-30v-15h15v-15.001h15v-75h15v-14.997h15v-15.002h15z"/>
<path d="m1125 119.999h45v-104.999h15v15h15v15h15v180h-15v15h-15v15.002l-75-.002v-15h-15v-15h-15v-45.001h15v-14.997-.002h30v60h45v-75h-90v-105.001h15v-14.997h15v-15.002h15z"/>
</svg>"""


def get_qr_b64(url: str = FORM_URL) -> str:
    """Generate a QR PNG with qrencode and return data URI. White bg, black modules."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        res = subprocess.run(
            ["qrencode", "-o", tmp_path, "-s", "10", "-m", "4", "-l", "M", url],
            capture_output=True, text=True,
        )
        if res.returncode != 0:
            print(f"qrencode failed: {res.stderr[:300]}")
            return ""
        data = Path(tmp_path).read_bytes()
        return f"data:image/png;base64,{base64.b64encode(data).decode()}"
    finally:
        try:
            Path(tmp_path).unlink(missing_ok=True)
        except Exception:
            pass


COMMON_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap');
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#08090c; font-family:'Plus Jakarta Sans',sans-serif; color:#f8fafc; overflow:hidden; position:relative; display:flex; flex-direction:column; }
.flag-bar { width:100%; height:6px; display:flex; z-index:10; }
.flag-green { width:33.333%; background:#10b981; box-shadow:0 0 16px rgba(16,185,129,.8);}
.flag-yellow { width:33.334%; background:#fbbf24; box-shadow:0 0 16px rgba(251,191,36,.9);}
.flag-red { width:33.333%; background:#ef4444; box-shadow:0 0 16px rgba(239,68,68,.8);}
.grid-pattern { position:absolute; inset:0; background-image:radial-gradient(circle at 1px 1px, rgba(255,255,255,.06) 1px, transparent 0); background-size:36px 36px; pointer-events:none; z-index:1; }
.glow { position:absolute; width:600px; height:600px; background:radial-gradient(circle, rgba(251,191,36,.12) 0%, transparent 65%); top:-120px; right:-120px; z-index:1; pointer-events:none; }
.glow-green { position:absolute; width:500px; height:500px; background:radial-gradient(circle, rgba(16,185,129,.1) 0%, transparent 65%); bottom:-100px; left:-100px; z-index:1; pointer-events:none; }
.mono { font-family:'JetBrains Mono',monospace; }
"""

HEADER_HTML = f"""
<div class="header">
  <div class="brand-left">
    <svg class="logo-mark" viewBox="0 0 1200 1200"><path fill="currentColor" d="{OMARCHY_MARK_PATH}"/></svg>
    <div style="display:flex;flex-direction:column;gap:2px;">
      <div class="wordmark">{OMARCHY_WORDMARK_SVG}</div>
      <div class="brand-sub">ETHIOPIA</div>
    </div>
  </div>
  <div class="prize-badge"><span class="dot"></span><span>10,000 ETB PRIZE POOL</span></div>
</div>
"""


def generate_png(html, path, w, h):
    tmp = path.with_suffix(".tmp.html")
    tmp.write_text(html, encoding="utf-8")
    cmd = ["chromium", "--headless", "--disable-gpu", "--no-sandbox",
           "--hide-scrollbars", f"--window-size={w},{h}",
           f"--screenshot={path}", f"file://{tmp.resolve()}"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if tmp.exists():
        tmp.unlink()
    if res.returncode != 0:
        print(f"ERR {path}: {res.stderr[:500]}")
    else:
        print(f"OK {path.name} ({w}x{h})")


def square(qr_b64):
    qr_img = f'<img class="qr-img" src="{qr_b64}" alt="Submit QR" />' if qr_b64 else ""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{COMMON_CSS}
body {{ width:1200px; height:1200px; background:radial-gradient(circle at 85% 12%, rgba(251,191,36,.1) 0%, transparent 45%), #08090c; }}
.wrap {{ position:relative; z-index:5; width:100%; height:100%; display:flex; flex-direction:column; justify-content:space-between; padding:42px 56px 36px 56px; }}
.header {{ display:flex; align-items:center; justify-content:space-between; }}
.brand-left {{ display:flex; align-items:center; gap:16px; }}
.logo-mark {{ width:46px; height:46px; color:#fbbf24; filter:drop-shadow(0 0 16px rgba(251,191,36,.6)); }}
.wordmark {{ width:185px; height:38px; color:#fbbf24; }}
.brand-sub {{ font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:700; letter-spacing:.42em; color:#10b981; }}
.prize-badge {{ display:flex; align-items:center; gap:10px; background:rgba(251,191,36,.1); border:1px solid rgba(251,191,36,.4); border-radius:9999px; padding:9px 20px; font-family:'JetBrains Mono',monospace; font-size:13px; font-weight:800; color:#fbbf24; letter-spacing:.06em; }}
.dot {{ width:8px; height:8px; background:#10b981; border-radius:50%; box-shadow:0 0 10px #10b981; }}
.eyebrow {{ font-family:'JetBrains Mono',monospace; font-size:13px; font-weight:700; letter-spacing:.22em; color:#10b981; margin-bottom:10px; }}
.title {{ font-size:62px; font-weight:800; letter-spacing:-.03em; line-height:1.02; color:#fff; }}
.title span {{ color:#fbbf24; text-shadow:0 0 40px rgba(251,191,36,.45); }}
.sub {{ font-size:18px; color:rgba(244,237,228,.72); margin-top:10px; line-height:1.5; max-width:880px; }}
.prizes {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:18px; margin:22px 0 18px 0; }}
.card {{ background:#0e0f14; border:1px solid rgba(255,255,255,.1); border-radius:16px; padding:22px 20px; text-align:center; }}
.card.first {{ background:linear-gradient(180deg, rgba(251,191,36,.16) 0%, rgba(14,15,20,.98) 100%); border:2px solid rgba(251,191,36,.65); box-shadow:0 16px 40px -10px rgba(251,191,36,.3); }}
.place {{ font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:800; letter-spacing:.12em; padding:4px 12px; border-radius:9999px; display:inline-block; margin-bottom:10px; }}
.first .place {{ background:#fbbf24; color:#08090c; }}
.second .place {{ background:rgba(16,185,129,.18); color:#10b981; border:1px solid rgba(16,185,129,.4); }}
.third .place {{ background:rgba(255,255,255,.08); color:#fff; }}
.amount {{ font-family:'JetBrains Mono',monospace; font-size:44px; font-weight:800; line-height:1; }}
.first .amount {{ color:#fbbf24; }} .second .amount {{ color:#10b981; }} .third .amount {{ color:#fff; }}
.cur {{ font-family:'JetBrains Mono',monospace; font-size:14px; color:rgba(255,255,255,.55); font-weight:700; }}
.rules {{ display:flex; gap:12px; margin-bottom:16px; }}
.rule {{ flex:1; background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.1); border-radius:12px; padding:12px 16px; font-family:'JetBrains Mono',monospace; font-size:12.5px; color:rgba(255,255,255,.8); text-align:center; }}
.rule strong {{ color:#fbbf24; display:block; font-size:11px; letter-spacing:.1em; margin-bottom:4px; }}
.cta-qr {{ background:#ffffff; border-radius:14px; padding:16px 22px; display:flex; align-items:center; gap:20px; }}
.qr-img {{ width:128px; height:128px; border-radius:8px; background:#fff; flex-shrink:0; }}
.cta-main {{ flex:1; text-align:left; }}
.cta-title {{ font-family:'JetBrains Mono',monospace; font-size:20px; font-weight:800; color:#08090c; letter-spacing:.02em; }}
.cta-link {{ font-family:'JetBrains Mono',monospace; font-size:15px; font-weight:700; color:#08090c; background:rgba(0,0,0,.07); display:inline-block; padding:6px 14px; border-radius:9999px; margin-top:8px; }}
.cta-note {{ font-size:13px; color:rgba(0,0,0,.6); margin-top:8px; }}
.cta-side {{ text-align:right; flex-shrink:0; }}
.cta-side-date {{ font-family:'JetBrains Mono',monospace; font-size:13px; font-weight:800; color:#08090c; background:#fbbf24; padding:8px 16px; border-radius:9999px; }}
.cta-side-sub {{ font-family:'JetBrains Mono',monospace; font-size:11px; color:rgba(0,0,0,.6); margin-top:8px; }}
.footer {{ border-top:1px solid rgba(255,255,255,.1); padding-top:14px; display:flex; justify-content:space-between; font-family:'JetBrains Mono',monospace; font-size:12px; color:rgba(255,255,255,.6); }}
.footer b {{ color:#fbbf24; }}
</style></head><body>
<div class="flag-bar"><div class="flag-green"></div><div class="flag-yellow"></div><div class="flag-red"></div></div>
<div class="grid-pattern"></div><div class="glow"></div><div class="glow-green"></div>
<div class="wrap">{HEADER_HTML}
<div><div class="eyebrow">[ // THEME COMPETITION — MEETUP 2026 ]</div>
<h1 class="title">DESIGN THE<br><span>ETHIOPIAN</span> THEME</h1>
<p class="sub">Submit your original theme for the Omarchy Ethiopia Theme Competition. See Google Form for details and rules.</p></div>
<div class="prizes">
<div class="card first"><span class="place">🥇 1ST PLACE</span><div class="amount">5,000</div><div class="cur">ETB</div></div>
<div class="card second"><span class="place">🥈 2ND PLACE</span><div class="amount">3,000</div><div class="cur">ETB</div></div>
<div class="card third"><span class="place">🥉 3RD PLACE</span><div class="amount">2,000</div><div class="cur">ETB</div></div>
</div>
<div class="rules">
<div class="rule"><strong>SUBMIT</strong>Scan QR or use form link</div>
<div class="rule"><strong>DEADLINE</strong>Oct 15, 11:59 PM EAT</div>
<div class="rule"><strong>WINNERS</strong>Oct 17 • Addis Ababa</div>
</div>
<div class="cta-qr">{qr_img}
<div class="cta-main"><div class="cta-title">SCAN TO SUBMIT →</div><div class="cta-link">{FORM_SHORT}</div><div class="cta-note">Full details and rules in the Google Form</div></div>
<div class="cta-side"><div class="cta-side-date">10K POOL</div><div class="cta-side-sub">Telebirr / CBE</div></div>
</div>
<div class="footer"><div>omarchy.org.et • <b>Omarchy Ethiopia</b></div><div>Theme Competition 2026</div></div>
</div></body></html>"""


def landscape(qr_b64):
    qr_img = f'<img src="{qr_b64}" alt="Submit QR" style="width:96px;height:96px;border-radius:8px;background:#fff;flex-shrink:0;" />' if qr_b64 else ""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{COMMON_CSS}
body {{ width:1200px; height:675px; }}
.wrap {{ position:relative; z-index:5; width:100%; height:100%; display:flex; gap:28px; padding:28px 44px; }}
.left {{ flex:1.15; display:flex; flex-direction:column; justify-content:space-between; }}
.right {{ flex:.85; display:flex; flex-direction:column; gap:12px; justify-content:center; }}
.header {{ display:flex; align-items:center; justify-content:space-between; }}
.brand-left {{ display:flex; align-items:center; gap:12px; }}
.logo-mark {{ width:36px; height:36px; color:#fbbf24; }}
.wordmark {{ width:140px; height:28px; color:#fbbf24; }}
.brand-sub {{ font-family:'JetBrains Mono',monospace; font-size:9px; font-weight:700; letter-spacing:.38em; color:#10b981; }}
.prize-badge {{ display:flex; align-items:center; gap:8px; background:rgba(251,191,36,.1); border:1px solid rgba(251,191,36,.35); border-radius:9999px; padding:6px 14px; font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:800; color:#fbbf24; }}
.dot {{ width:7px; height:7px; background:#10b981; border-radius:50%; }}
.eyebrow {{ font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:700; letter-spacing:.2em; color:#10b981; margin-bottom:6px; }}
.title {{ font-size:44px; font-weight:800; letter-spacing:-.02em; line-height:1.05; }}
.title span {{ color:#fbbf24; }}
.sub {{ font-size:13.5px; color:rgba(255,255,255,.7); margin-top:8px; line-height:1.5; }}
.meta {{ display:flex; gap:10px; margin-top:12px; }}
.meta div {{ font-family:'JetBrains Mono',monospace; font-size:11px; background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.12); padding:8px 12px; border-radius:8px; color:#fff; }}
.meta b {{ color:#fbbf24; }}
.card {{ background:#0e0f14; border:1px solid rgba(255,255,255,.1); border-radius:12px; padding:14px 18px; display:flex; align-items:center; gap:14px; }}
.card.first {{ border:1.5px solid rgba(251,191,36,.6); background:linear-gradient(90deg, rgba(251,191,36,.14), rgba(14,15,20,.98)); }}
.place {{ font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:800; letter-spacing:.08em; }}
.amount {{ font-family:'JetBrains Mono',monospace; font-size:30px; font-weight:800; }}
.first .amount {{ color:#fbbf24; }} .second .amount {{ color:#10b981; }}
.cta-qr {{ background:#ffffff; border-radius:12px; padding:12px 16px; display:flex; align-items:center; gap:14px; }}
.cta-qr-title {{ font-family:'JetBrains Mono',monospace; font-size:13px; font-weight:800; color:#08090c; }}
.cta-qr-link {{ font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:700; color:rgba(0,0,0,.7); }}
</style></head><body>
<div class="flag-bar"><div class="flag-green"></div><div class="flag-yellow"></div><div class="flag-red"></div></div>
<div class="grid-pattern"></div><div class="glow"></div>
<div class="wrap">
<div class="left">{HEADER_HTML}
<div><div class="eyebrow">[ // THEME COMPETITION ]</div>
<h1 class="title">DESIGN THE<br><span>ETHIOPIAN</span> THEME</h1>
<p class="sub">Submit your original theme for the Omarchy Ethiopia Theme Competition. See Google Form for details and rules.</p>
<div class="meta"><div><b>DEADLINE:</b> Oct 15 EAT</div><div><b>WINNERS:</b> Oct 17 Addis</div></div>
</div>
<div class="mono" style="font-size:11px;color:rgba(255,255,255,.55)">omarchy.org.et • 10,000 ETB pool • Telebirr/CBE</div>
</div>
<div class="right">
<div class="card first"><div style="font-size:28px">🥇</div><div><div class="place">1ST — WINNER</div><div class="amount">5,000 ETB</div></div></div>
<div class="card second"><div style="font-size:28px">🥈</div><div><div class="place">2ND PLACE</div><div class="amount">3,000 ETB</div></div></div>
<div class="card"><div style="font-size:28px">🥉</div><div><div class="place">3RD PLACE</div><div class="amount" style="color:#fff">2,000 ETB</div></div></div>
<div class="cta-qr">{qr_img}<div><div class="cta-qr-title">SCAN TO SUBMIT →</div><div class="cta-qr-link">{FORM_SHORT}</div><div class="cta-qr-link">Details in Google Form</div></div></div>
</div>
</div></body></html>"""


def story(qr_b64):
    qr_img = f'<img src="{qr_b64}" alt="Submit QR" style="width:210px;height:210px;border-radius:12px;background:#fff;" />' if qr_b64 else ""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{COMMON_CSS}
body {{ width:1080px; height:1920px; background:radial-gradient(circle at 50% 0%, rgba(251,191,36,.12) 0%, transparent 50%), #08090c; }}
.wrap {{ position:relative; z-index:5; width:100%; height:100%; display:flex; flex-direction:column; justify-content:space-between; padding:56px 56px 48px 56px; text-align:center; }}
.header {{ display:flex; flex-direction:column; align-items:center; gap:14px; }}
.logo-mark {{ width:64px; height:64px; color:#fbbf24; filter:drop-shadow(0 0 20px rgba(251,191,36,.6)); }}
.wordmark {{ width:260px; height:54px; color:#fbbf24; margin:0 auto; }}
.brand-sub {{ font-family:'JetBrains Mono',monospace; font-size:14px; font-weight:700; letter-spacing:.5em; color:#10b981; padding-left:.5em; }}
.prize-badge {{ background:rgba(251,191,36,.1); border:1px solid rgba(251,191,36,.4); border-radius:9999px; padding:10px 26px; font-family:'JetBrains Mono',monospace; font-size:15px; font-weight:800; color:#fbbf24; letter-spacing:.06em; }}
.eyebrow {{ font-family:'JetBrains Mono',monospace; font-size:15px; font-weight:700; letter-spacing:.24em; color:#10b981; }}
.title {{ font-size:84px; font-weight:800; letter-spacing:-.03em; line-height:1.0; margin:12px 0; }}
.title span {{ color:#fbbf24; text-shadow:0 0 50px rgba(251,191,36,.5); }}
.sub {{ font-size:22px; color:rgba(255,255,255,.72); line-height:1.5; max-width:800px; margin:0 auto; }}
.card {{ background:#0e0f14; border:1px solid rgba(255,255,255,.12); border-radius:20px; padding:24px; display:flex; align-items:center; gap:18px; text-align:left; }}
.card.first {{ border:2px solid rgba(251,191,36,.65); background:linear-gradient(90deg, rgba(251,191,36,.16), rgba(14,15,20,.98)); }}
.amount {{ font-family:'JetBrains Mono',monospace; font-size:52px; font-weight:800; }}
.first .amount {{ color:#fbbf24; }} .second .amount {{ color:#10b981; }}
.cta-qr {{ background:#ffffff; border-radius:20px; padding:28px; display:flex; flex-direction:column; align-items:center; gap:14px; }}
.cta-qr-title {{ font-family:'JetBrains Mono',monospace; font-weight:800; color:#08090c; font-size:26px; }}
.cta-qr-link {{ font-family:'JetBrains Mono',monospace; font-weight:700; color:#08090c; font-size:19px; background:rgba(0,0,0,.07); padding:8px 18px; border-radius:9999px; }}
.cta-qr-note {{ font-size:16px; color:rgba(0,0,0,.6); }}
.small {{ font-family:'JetBrains Mono',monospace; font-size:15px; color:rgba(255,255,255,.6); }}
.small b {{ color:#fbbf24; }}
</style></head><body>
<div class="flag-bar"><div class="flag-green"></div><div class="flag-yellow"></div><div class="flag-red"></div></div>
<div class="grid-pattern"></div><div class="glow"></div><div class="glow-green"></div>
<div class="wrap">
<div class="header">
<svg class="logo-mark" viewBox="0 0 1200 1200"><path fill="currentColor" d="{OMARCHY_MARK_PATH}"/></svg>
<div><div class="wordmark">{OMARCHY_WORDMARK_SVG}</div><div class="brand-sub">ETHIOPIA</div></div>
<div class="prize-badge">✦ 10,000 ETB PRIZE POOL ✦</div>
</div>
<div><div class="eyebrow">[ // THEME COMPETITION ]</div>
<h1 class="title">DESIGN<br>THE <span>ETHIOPIAN</span><br>THEME</h1>
<p class="sub">Submit your original theme for the Omarchy Ethiopia Theme Competition. See Google Form for details and rules.</p></div>
<div style="display:flex;flex-direction:column;gap:16px;">
<div class="card first"><div style="font-size:44px">🥇</div><div><div class="mono" style="font-size:13px;font-weight:800;letter-spacing:.1em;">1ST PLACE — WINNER</div><div class="amount">5,000 ETB</div></div></div>
<div class="card second"><div style="font-size:44px">🥈</div><div><div class="mono" style="font-size:13px;font-weight:800;letter-spacing:.1em;">2ND PLACE</div><div class="amount">3,000 ETB</div></div></div>
<div class="card"><div style="font-size:44px">🥉</div><div><div class="mono" style="font-size:13px;font-weight:800;letter-spacing:.1em;">3RD PLACE</div><div class="amount" style="color:#fff">2,000 ETB</div></div></div>
</div>
<div style="display:flex;flex-direction:column;gap:14px;">
<div class="cta-qr">{qr_img}
<div class="cta-qr-title">SCAN TO SUBMIT →</div>
<div class="cta-qr-link">{FORM_SHORT}</div>
<div class="cta-qr-note">Full details and rules in the Google Form</div>
</div>
<div class="small"><b>DEADLINE:</b> Oct 15, 11:59 PM EAT<br>Winners Oct 17 • Addis Ababa • omarchy.org.et</div>
</div>
</div>
<div class="flag-bar"><div class="flag-green"></div><div class="flag-yellow"></div><div class="flag-red"></div></div>
</body></html>"""


def main():
    qr_b64 = get_qr_b64()
    if not qr_b64:
        print("WARNING: QR generation failed, rendering without QR")
    generate_png(square(qr_b64), OUTPUT_DIR / "theme-competition-square.png", 1200, 1200)
    generate_png(landscape(qr_b64), OUTPUT_DIR / "theme-competition-landscape.png", 1200, 675)
    generate_png(story(qr_b64), OUTPUT_DIR / "theme-competition-story.png", 1080, 1920)
    print("Theme competition graphics done.")

if __name__ == "__main__":
    main()
