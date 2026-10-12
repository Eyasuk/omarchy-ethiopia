import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "public/assets/graphics"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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

COMMON_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap');
* { margin:0; padding:0; box-sizing:border-box; }
.am { font-family:'Noto Sans Ethiopic','Plus Jakarta Sans',sans-serif; }
body { background:#08090c; font-family:'Plus Jakarta Sans',sans-serif; color:#f8fafc; overflow:hidden; position:relative; display:flex; flex-direction:column; }
.flag-bar { width:100%; height:6px; display:flex; z-index:10; }
.flag-green { width:33.333%; background:#10b981; box-shadow:0 0 16px rgba(16,185,129,.8);}
.flag-yellow { width:33.334%; background:#fbbf24; box-shadow:0 0 16px rgba(251,191,36,.9);}
.flag-red { width:33.333%; background:#ef4444; box-shadow:0 0 16px rgba(239,68,68,.8);}
.grid-pattern { position:absolute; inset:0; background-image:radial-gradient(circle at 1px 1px, rgba(255,255,255,.06) 1px, transparent 0); background-size:36px 36px; pointer-events:none; z-index:1; }
.mono { font-family:'JetBrains Mono',monospace; }
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


def square():
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{COMMON_CSS}
body {{ width:1200px; height:1200px; background:radial-gradient(circle at 50% 40%, rgba(251,191,36,.12) 0%, transparent 60%), radial-gradient(circle at 85% 12%, rgba(16,185,129,.08) 0%, transparent 45%), #08090c; }}
.wrap {{ position:relative; z-index:5; width:100%; height:100%; display:flex; flex-direction:column; justify-content:space-between; padding:48px 60px 40px 60px; }}
.header {{ display:flex; align-items:center; justify-content:space-between; }}
.brand-left {{ display:flex; align-items:center; gap:16px; }}
.logo-mark {{ width:48px; height:48px; color:#fbbf24; filter:drop-shadow(0 0 16px rgba(251,191,36,.6)); }}
.wordmark {{ width:195px; height:40px; color:#fbbf24; }}
.brand-sub {{ font-family:'JetBrains Mono',monospace; font-size:11.5px; font-weight:700; letter-spacing:.42em; color:#10b981; }}
.date-badge {{ display:flex; align-items:center; gap:10px; background:rgba(251,191,36,.1); border:1px solid rgba(251,191,36,.4); border-radius:9999px; padding:10px 22px; font-family:'JetBrains Mono',monospace; font-size:13px; font-weight:800; color:#fbbf24; letter-spacing:.08em; }}
.date-badge .dot {{ width:8px; height:8px; background:#10b981; border-radius:50%; box-shadow:0 0 10px #10b981; }}
.center {{ display:flex; flex-direction:column; align-items:center; text-align:center; margin:auto 0; gap:20px; }}
.eyebrow {{ font-family:'JetBrains Mono',monospace; font-size:14px; font-weight:800; letter-spacing:.24em; color:#10b981; }}
.title {{ font-size:64px; font-weight:800; letter-spacing:-.03em; line-height:1.03; color:#fff; }}
.title span {{ color:#fbbf24; text-shadow:0 0 45px rgba(251,191,36,.5); }}
.time-card {{ display:flex; align-items:center; gap:22px; background:linear-gradient(180deg, rgba(251,191,36,.16) 0%, rgba(14,15,20,.98) 100%); border:2px solid rgba(251,191,36,.6); border-radius:20px; padding:20px 36px; box-shadow:0 16px 45px -10px rgba(251,191,36,.3); }}
.time-big {{ font-family:'JetBrains Mono',monospace; font-size:46px; font-weight:800; color:#fbbf24; line-height:1; }}
.time-sub {{ font-family:'JetBrains Mono',monospace; font-size:14px; font-weight:700; color:#fff; text-align:left; line-height:1.5; }}
.venue {{ background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.12); border-radius:16px; padding:18px 28px; max-width:920px; }}
.venue-name {{ font-size:21px; font-weight:800; color:#fff; }}
.venue-addr {{ font-family:'JetBrains Mono',monospace; font-size:13.5px; color:rgba(244,237,228,.75); margin-top:8px; line-height:1.6; }}
.venue-code {{ display:inline-block; margin-top:10px; font-family:'JetBrains Mono',monospace; font-size:12px; font-weight:700; color:#10b981; background:rgba(16,185,129,.12); border:1px solid rgba(16,185,129,.35); padding:4px 14px; border-radius:9999px; }}
.note {{ font-family:'JetBrains Mono',monospace; font-size:13px; color:rgba(244,237,228,.65); }}
.note strong {{ color:#fbbf24; }}
.qr-bar {{ display:flex; align-items:center; justify-content:center; gap:12px; background:rgba(16,185,129,.1); border:1px solid rgba(16,185,129,.5); border-radius:14px; padding:12px 26px; max-width:920px; }}
.qr-bar .qr-en {{ font-family:'JetBrains Mono',monospace; font-size:13.5px; font-weight:800; letter-spacing:.1em; color:#10b981; }}
.qr-bar .qr-am {{ font-size:16px; font-weight:700; color:#fff; }}
.footer {{ border-top:1px solid rgba(255,255,255,.1); padding-top:20px; display:flex; align-items:center; justify-content:space-between; font-family:'JetBrains Mono',monospace; font-size:13px; }}
.footer-right {{ color:#fbbf24; font-weight:600; display:flex; gap:16px; }}
</style></head><body>
<div class="flag-bar"><div class="flag-green"></div><div class="flag-yellow"></div><div class="flag-red"></div></div>
<div class="grid-pattern"></div>
<div class="wrap">
<div class="header">
<div class="brand-left">
<svg class="logo-mark" viewBox="0 0 1200 1200"><path fill="currentColor" d="{OMARCHY_MARK_PATH}"/></svg>
<div style="display:flex;flex-direction:column;gap:2px;"><div class="wordmark">{OMARCHY_WORDMARK_SVG}</div><div class="brand-sub">ETHIOPIA</div></div>
</div>
<div class="date-badge"><span class="dot"></span><span>SAT, OCT 17 <span class="am">&nbsp;• ቅዳሜ ጥቅምት 7</span></span></div>
</div>
<div class="center">
<div class="eyebrow">THIS SATURDAY IN ADDIS ABABA</div>
<h1 class="title">SEE YOU <span>ON SATURDAY</span></h1>
<div class="time-card">
<div class="time-big">2:00 PM</div>
<div class="time-sub">Saturday, Oct 17 <span class="am">• ቅዳሜ ጥቅምት 7</span><br>8:00 in the afternoon, local time</div>
</div>
<div class="venue">
<div class="venue-name">Elsadol Building, 8th floor, office 806</div>
<div class="venue-addr">Mike Leyland road, the road from Atlas to 22, in front of NB Business Centre<br>Addis Ababa, Ethiopia</div>
<div class="venue-code">Plus code: 2Q6J+3C</div>
</div>
<div class="qr-bar"><span class="qr-en">QR CHECK-IN REQUIRED</span><span class="qr-am am">ለመግቢያ QR ኮድ ያስፈልጋል</span></div>
<div class="note"><strong>Bring your laptop.</strong> In person meetup, livestream for remote folks.</div>
</div>
<div class="footer">
<div style="color:rgba(244,237,228,.7);">RSVP: luma.com/zh5jv195</div>
<div class="footer-right"><span>omarchy.org.et/meetup</span></div>
</div>
</div>
</body></html>"""


def landscape():
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{COMMON_CSS}
body {{ width:1200px; height:675px; background:radial-gradient(circle at 50% 45%, rgba(251,191,36,.11) 0%, transparent 60%), #08090c; }}
.wrap {{ position:relative; z-index:5; width:100%; height:100%; display:flex; flex-direction:column; justify-content:space-between; padding:28px 52px 22px 52px; }}
.header {{ display:flex; align-items:center; justify-content:space-between; }}
.brand-left {{ display:flex; align-items:center; gap:14px; }}
.logo-mark {{ width:38px; height:38px; color:#fbbf24; filter:drop-shadow(0 0 14px rgba(251,191,36,.6)); }}
.wordmark {{ width:150px; height:30px; color:#fbbf24; }}
.brand-sub {{ font-family:'JetBrains Mono',monospace; font-size:9.5px; font-weight:700; letter-spacing:.38em; color:#10b981; }}
.date-badge {{ display:flex; align-items:center; gap:8px; background:rgba(251,191,36,.1); border:1px solid rgba(251,191,36,.35); border-radius:9999px; padding:6px 16px; font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:800; color:#fbbf24; }}
.center {{ display:flex; align-items:center; justify-content:center; gap:36px; margin:auto 0; }}
.left {{ text-align:left; }}
.eyebrow {{ font-family:'JetBrains Mono',monospace; font-size:11px; font-weight:800; letter-spacing:.22em; color:#10b981; margin-bottom:8px; }}
.title {{ font-size:52px; font-weight:800; letter-spacing:-.025em; line-height:1.03; color:#fff; }}
.title span {{ color:#fbbf24; text-shadow:0 0 35px rgba(251,191,36,.45); }}
.time-row {{ display:flex; align-items:center; gap:14px; margin-top:14px; }}
.time-big {{ font-family:'JetBrains Mono',monospace; font-size:32px; font-weight:800; color:#08090c; background:#fbbf24; padding:6px 18px; border-radius:12px; box-shadow:0 0 25px rgba(251,191,36,.5); }}
.time-sub {{ font-family:'JetBrains Mono',monospace; font-size:12px; font-weight:700; color:#fff; line-height:1.5; }}
.right {{ background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.12); border-radius:14px; padding:16px 20px; max-width:440px; }}
.venue-name {{ font-size:17px; font-weight:800; color:#fff; }}
.venue-addr {{ font-family:'JetBrains Mono',monospace; font-size:11px; color:rgba(244,237,228,.75); margin-top:6px; line-height:1.6; }}
.venue-code {{ display:inline-block; margin-top:8px; font-family:'JetBrains Mono',monospace; font-size:10.5px; font-weight:700; color:#10b981; background:rgba(16,185,129,.12); border:1px solid rgba(16,185,129,.35); padding:3px 12px; border-radius:9999px; }}
.note {{ font-family:'JetBrains Mono',monospace; font-size:11px; color:rgba(244,237,228,.65); margin-top:10px; }}
.note strong {{ color:#fbbf24; }}
.qr-line {{ display:flex; align-items:center; gap:8px; margin-top:10px; background:rgba(16,185,129,.1); border:1px solid rgba(16,185,129,.45); border-radius:10px; padding:7px 12px; }}
.qr-line .qr-en {{ font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:800; letter-spacing:.08em; color:#10b981; }}
.qr-line .qr-am {{ font-size:12.5px; font-weight:700; color:#fff; }}
.footer {{ border-top:1px solid rgba(255,255,255,.1); padding-top:12px; display:flex; align-items:center; justify-content:space-between; font-family:'JetBrains Mono',monospace; font-size:11px; color:rgba(244,237,228,.7); }}
.footer-right {{ color:#fbbf24; font-weight:600; }}
</style></head><body>
<div class="flag-bar"><div class="flag-green"></div><div class="flag-yellow"></div><div class="flag-red"></div></div>
<div class="grid-pattern"></div>
<div class="wrap">
<div class="header">
<div class="brand-left">
<svg class="logo-mark" viewBox="0 0 1200 1200"><path fill="currentColor" d="{OMARCHY_MARK_PATH}"/></svg>
<div style="display:flex;flex-direction:column;gap:2px;"><div class="wordmark">{OMARCHY_WORDMARK_SVG}</div><div class="brand-sub">ETHIOPIA</div></div>
</div>
<div class="date-badge"><span>SAT, OCT 17, 2:00 PM <span class="am">• ቅዳሜ ጥቅምት 7</span></span></div>
</div>
<div class="center">
<div class="left">
<div class="eyebrow">THIS SATURDAY IN ADDIS ABABA</div>
<h1 class="title">SEE YOU<br><span>ON SATURDAY</span></h1>
<div class="time-row">
<div class="time-big">2:00 PM</div>
<div class="time-sub">Saturday, Oct 17 <span class="am">• ቅዳሜ ጥቅምት 7</span><br>8:00 in the afternoon, local time</div>
</div>
</div>
<div class="right">
<div class="venue-name">Elsadol Building, 8th floor, office 806</div>
<div class="venue-addr">Mike Leyland road, the road from Atlas to 22, in front of NB Business Centre, Addis Ababa</div>
<div class="venue-code">Plus code: 2Q6J+3C</div>
<div class="qr-line"><span class="qr-en">QR CHECK-IN REQUIRED</span><span class="qr-am am">ለመግቢያ QR ኮድ ያስፈልጋል</span></div>
<div class="note"><strong>Bring your laptop.</strong> In person plus livestream.</div>
</div>
</div>
<div class="footer">
<div>RSVP: luma.com/zh5jv195</div>
<div class="footer-right"><span>omarchy.org.et/meetup</span></div>
</div>
</div>
</body></html>"""


def main():
    generate_png(square(), OUTPUT_DIR / "event-saturday-oct17-square.png", 1200, 1200)
    generate_png(landscape(), OUTPUT_DIR / "event-saturday-oct17-landscape.png", 1200, 675)
    print("Saturday event graphics done.")


if __name__ == "__main__":
    main()
