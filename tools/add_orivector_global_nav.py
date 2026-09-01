from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')

STYLE = '''\n<style id="orivector-global-nav-style">\n.orivector-global-nav{width:100%;background:#07101d;border-bottom:1px solid rgba(255,255,255,.08);padding:8px 14px;position:relative;z-index:1000}\n.orivector-global-nav a{display:inline-flex;align-items:center;min-height:34px;padding:0 12px;border:1px solid rgba(255,255,255,.16);border-radius:999px;background:rgba(255,255,255,.06);color:#eef5ff;text-decoration:none;font-size:13px;font-weight:900;letter-spacing:.02em}\n.orivector-global-nav a:hover{background:rgba(255,255,255,.11)}\n</style>\n'''
BAR = '<div class="orivector-global-nav"><a href="https://orivector.jp/" aria-label="ORIVECTORトップへ戻る">← ORIVECTOR</a></div>'

if 'orivector-global-nav-style' in text or 'class="orivector-global-nav"' in text:
    raise SystemExit('Safety stop: ORIVECTOR global nav already exists')
if '</head>' not in text:
    raise SystemExit('Safety stop: </head> not found')
if not re.search(r'<body(?:\s[^>]*)?>', text, flags=re.I):
    raise SystemExit('Safety stop: <body> not found')

text = text.replace('</head>', STYLE + '</head>', 1)
text, count = re.subn(r'(<body(?:\s[^>]*)?>)', r'\1' + BAR, text, count=1, flags=re.I)
if count != 1:
    raise SystemExit('Safety stop: body injection failed')

for guard in ('const questions=', 'function startWrong', 'function showQuestionList', 'ca-pub-1712701486247077'):
    if guard not in text:
        raise SystemExit(f'Safety stop: expected AWS site guard missing: {guard}')

path.write_text(text, encoding='utf-8')
print('Added shared ORIVECTOR top navigation to AWS study site')
