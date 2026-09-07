from pathlib import Path
import json, re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

TITLE = 'AWS Cloud Practitioner 無料問題集306問｜CLF-C02対策｜ORIVECTOR'
DESC = 'AWS Certified Cloud Practitioner（CLF-C02）対策の無料問題集306問。10問・20問演習、本番形式65問模試、間違い復習、基礎学習、サービス比較・図解解説に対応。'
URL = 'https://orivector.jp/aws-study/'
OG = 'https://orivector.jp/assets/og-aws.png'

head_end = text.find('</head>')
if head_end == -1:
    raise SystemExit('index.html has no </head>')

# Remove only the SEO tags this script owns so reruns stay idempotent.
patterns = [
    r'<meta\s+name="description"[^>]*>\s*',
    r'<meta\s+name="robots"[^>]*>\s*',
    r'<meta\s+name="theme-color"[^>]*>\s*',
    r'<meta\s+name="author"[^>]*>\s*',
    r'<meta\s+property="og:[^"]+"[^>]*>\s*',
    r'<meta\s+name="twitter:[^"]+"[^>]*>\s*',
    r'<link\s+rel="canonical"[^>]*>\s*',
    r'<link\s+rel="author"[^>]*>\s*',
    r'<link\s+rel="icon"[^>]*>\s*',
    r'<link\s+rel="apple-touch-icon"[^>]*>\s*',
    r'<!-- aws-main-seo-v342 -->\s*<script type="application/ld\+json">.*?</script>\s*',
]
for pat in patterns:
    text = re.sub(pat, '', text, flags=re.I | re.S)

text = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', text, count=1, flags=re.I | re.S)

schema = {
    '@context': 'https://schema.org',
    '@graph': [
        {
            '@type': 'Organization',
            '@id': 'https://orivector.jp/#organization',
            'name': 'ORIVECTOR',
            'url': 'https://orivector.jp/'
        },
        {
            '@type': 'WebSite',
            '@id': 'https://orivector.jp/#website',
            'url': 'https://orivector.jp/',
            'name': 'ORIVECTOR',
            'publisher': {'@id': 'https://orivector.jp/#organization'},
            'inLanguage': 'ja-JP'
        },
        {
            '@type': ['WebApplication', 'LearningResource'],
            '@id': URL + '#app',
            'name': 'AWS Cloud Practitioner 無料問題集306問',
            'url': URL,
            'description': DESC,
            'applicationCategory': 'EducationalApplication',
            'operatingSystem': 'Web',
            'isAccessibleForFree': True,
            'educationalUse': 'AWS Certified Cloud Practitioner（CLF-C02）試験対策',
            'learningResourceType': ['問題集', '模擬試験', '基礎学習', '学習ガイド'],
            'inLanguage': 'ja',
            'publisher': {'@id': 'https://orivector.jp/#organization'},
            'image': OG
        },
        {
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'ORIVECTOR', 'item': 'https://orivector.jp/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'AWS Cloud Practitioner対策', 'item': URL}
            ]
        }
    ]
}

seo = f'''\n<meta name="description" content="{DESC}">
<link rel="canonical" href="{URL}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#07101d">
<meta name="author" content="shun">
<link rel="author" href="https://orivector.jp/about/">
<link rel="icon" type="image/png" sizes="512x512" href="https://orivector.jp/assets/favicon-512.png">
<link rel="icon" type="image/svg+xml" href="https://orivector.jp/assets/favicon.svg">
<link rel="apple-touch-icon" sizes="180x180" href="https://orivector.jp/assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:locale" content="ja_JP">
<meta property="og:site_name" content="ORIVECTOR">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{OG}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ORIVECTOR AWS Cloud Practitioner study">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="{OG}">
<!-- aws-main-seo-v342 -->
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(',', ':'))}</script>
'''
text = text.replace('</head>', seo + '</head>', 1)

# Keep the existing UI, but make the visible main heading and lead copy more descriptive.
text = text.replace(
    '<h1>試験対策を、迷わず進める。</h1><p>ORIVECTOR共通学習UI。演習・基礎・ガイドから、今やる学習を選べます。</p>',
    '<h1>AWS Cloud Practitionerを、<br>迷わず進める。</h1><p>CLF-C02対策・全306問。問題演習、65問模試、基礎学習、比較・図解ガイドから今やる学習を選べます。</p>',
    1
)
text = text.replace('<div class="version">ver 3.4.1</div>', '<div class="version">ver 3.4.2</div>', 1)

p.write_text(text, encoding='utf-8')
