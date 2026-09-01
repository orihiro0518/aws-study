from pathlib import Path
import re, json, html

ROOT = Path('.')
BASE = 'https://orivector.jp/aws-study/'


def replace_meta(text, name, value, prop=False):
    key = 'property' if prop else 'name'
    pattern = rf'<meta\s+{key}="{re.escape(name)}"\s+content="[^"]*"\s*/?>'
    tag = f'<meta {key}="{name}" content="{html.escape(value, quote=True)}">'
    if re.search(pattern, text, flags=re.I):
        return re.sub(pattern, tag, text, count=1, flags=re.I)
    return text.replace('</title>', '</title>\n' + tag, 1)


def set_canonical(text, url):
    tag = f'<link rel="canonical" href="{url}">'
    if re.search(r'<link\s+rel="canonical"[^>]*>', text, flags=re.I):
        return re.sub(r'<link\s+rel="canonical"[^>]*>', tag, text, count=1, flags=re.I)
    return text.replace('</title>', '</title>\n' + tag, 1)


def set_title(text, title):
    if re.search(r'<title>.*?</title>', text, flags=re.I | re.S):
        return re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)}</title>', text, count=1, flags=re.I | re.S)
    return text.replace('<head>', '<head>\n<title>' + html.escape(title) + '</title>', 1)


def add_robots(text):
    if 'name="robots"' not in text:
        text = text.replace('</title>', '</title>\n<meta name="robots" content="index,follow,max-image-preview:large">', 1)
    return text


def clean_text(s):
    s = re.sub(r'<[^>]+>', '', s)
    return html.unescape(re.sub(r'\s+', ' ', s)).strip()


def get_h1(text, fallback):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', text, flags=re.I | re.S)
    return clean_text(m.group(1)) if m else fallback


def add_schema(text, schema, marker='seo-v4-schema'):
    if marker in text:
        return text
    tag = f'\n<!-- {marker} -->\n<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(",", ":"))}</script>\n'
    return text.replace('</head>', tag + '</head>', 1)


def normalize_counts(text):
    replacements = {
        '無料300問': '無料250問',
        '問題集300問': '問題集250問',
        '全300問': '全250問',
        '300問の無料問題集': '250問の無料問題集',
        '300問を収録': '250問を収録',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


# ---------- main page ----------
p = ROOT / 'index.html'
text = p.read_text(encoding='utf-8')
text = normalize_counts(text)
text = re.sub(r'ver\s+3\.\d+\.\d+', 'ver 4.0.0', text, count=1)

# Answer-revealing questions -> requirement-based questions.
question_replacements = {
    'IAM Identity Centerは複数AWSアカウントやビジネスアプリへの従業員アクセスを一元管理します。この説明に最も当てはまる選択肢はどれか。':
        '複数のAWSアカウントやビジネスアプリケーションに対する従業員のアクセスを、一元的に管理したい。この要件を満たすAWSサービスはどれか。',
    'IAM Identity Centerは複数AWSアカウントやビジネスアプリへの従業員アクセスを一元管理します。この説明に最も当てはまる選択肢はどれですか？':
        '複数のAWSアカウントやビジネスアプリケーションに対する従業員のアクセスを、一元的に管理したい。この要件を満たすAWSサービスはどれですか？',
    'クラウド移行を進めるチームが要件を整理している。 iAM Identity Centerは複数AWSアカウントやビジネスアプリへの従業員アクセスを一元管理します。この説明に最も当てはまる選択肢はどれか。':
        'クラウド移行を進める企業が、複数のAWSアカウントと業務アプリへの従業員アクセスを1か所から管理したい。最も適切なAWSサービスはどれか。',
    '新しいワークロードをAWSで運用することになった。 次の状況について判断する。iAM Identity Centerは複数AWSアカウントやビジネスアプリへの従業員アクセスを一元管理します。この説明に最も当てはまる選択肢はどれか。':
        'ある企業では複数のAWSアカウントを利用している。従業員が各アカウントや業務アプリへアクセスするための認証・アクセス管理を集約したい。最も適切なAWSサービスはどれか。',
    'Secrets ManagerはDBパスワードやAPIキーなどのシークレットを安全に保存・ローテーションします。この説明に最も当てはまる選択肢はどれか。':
        'データベースのパスワードやAPIキーを安全に保存し、定期的なローテーションも自動化したい。最も適切なAWSサービスはどれか。',
    'Secrets ManagerはDBパスワードやAPIキーなどのシークレットを安全に保存・ローテーションします。この説明に最も当てはまる選択肢はどれですか？':
        'データベースのパスワードやAPIキーを安全に保存し、定期的なローテーションも自動化したい。最も適切なAWSサービスはどれですか？',
    'AWSを利用する組織で次の要件が生じた。 secrets ManagerはDBパスワードやAPIキーなどのシークレットを安全に保存・ローテーションします。この説明に最も当てはまる選択肢はどれか。':
        'AWSを利用する組織で、アプリケーションが使用する認証情報をコードへ直接埋め込まず、安全に保管・更新したい。最も適切なAWSサービスはどれか。',
}
for old, new in question_replacements.items():
    text = text.replace(old, new)

main_title = 'AWS Cloud Practitioner（CLF-C02）無料問題集250問｜模擬試験・図解解説｜ORIVECTOR'
main_desc = 'AWS Certified Cloud Practitioner（CLF-C02）対策の無料問題集250問。本番形式65問の模擬試験、図解学習、詳しい解説、間違い復習に対応。AWS初心者の独学・資格試験対策に。'
text = set_title(text, main_title)
text = set_canonical(text, BASE)
text = add_robots(text)
text = replace_meta(text, 'description', main_desc)
text = replace_meta(text, 'og:title', 'AWS Cloud Practitioner（CLF-C02）無料問題集250問｜ORIVECTOR', prop=True)
text = replace_meta(text, 'og:description', '無料250問＋本番形式65問の模擬試験＋図解学習でAWS Cloud Practitionerを対策。', prop=True)
text = replace_meta(text, 'og:url', BASE, prop=True)
if 'name="twitter:title"' not in text:
    text = text.replace('</head>', '<meta name="twitter:title" content="AWS Cloud Practitioner（CLF-C02）無料問題集250問｜ORIVECTOR">\n<meta name="twitter:description" content="無料250問・65問模試・図解解説でCLF-C02を対策。">\n</head>', 1)

text = text.replace('<h1>問題を解いて、AWSの基礎を固める。</h1>', '<h1>AWS Cloud Practitioner（CLF-C02）無料問題集250問</h1>')

main_schema = {
    '@context': 'https://schema.org',
    '@graph': [
        {'@type': 'Organization', '@id': 'https://orivector.jp/#organization', 'name': 'ORIVECTOR', 'url': 'https://orivector.jp/'},
        {'@type': 'WebSite', '@id': 'https://orivector.jp/#website', 'url': 'https://orivector.jp/', 'name': 'ORIVECTOR', 'publisher': {'@id': 'https://orivector.jp/#organization'}, 'inLanguage': 'ja'},
        {'@type': ['WebApplication', 'LearningResource'], '@id': BASE + '#app', 'name': 'AWS Cloud Practitioner（CLF-C02）無料問題集250問', 'url': BASE, 'description': main_desc, 'applicationCategory': 'EducationalApplication', 'operatingSystem': 'Any', 'isAccessibleForFree': True, 'educationalUse': '試験対策', 'learningResourceType': ['問題集', '模擬試験', '学習ガイド'], 'inLanguage': 'ja', 'publisher': {'@id': 'https://orivector.jp/#organization'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'ORIVECTOR', 'item': 'https://orivector.jp/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'AWS Cloud Practitioner 無料問題集', 'item': BASE}
        ]}
    ]
}
text = add_schema(text, main_schema)

if 'id="seo-faq-v4"' not in text:
    faq = '''<section class="card" id="seo-faq-v4" style="margin-top:16px"><h2>AWS Cloud Practitioner 無料問題集のFAQ</h2><h3>問題は何問ありますか？</h3><p style="color:var(--muted);line-height:1.8">無料問題集は250問を収録しています。本番形式を意識した65問の模擬試験も利用できます。</p><h3>スマホでも使えますか？</h3><p style="color:var(--muted);line-height:1.8">スマートフォンのブラウザから利用できます。</p><h3>どう勉強するのがおすすめですか？</h3><p style="color:var(--muted);line-height:1.8">基礎学習→問題演習→間違い復習→65問模試の順で進め、苦手分野は図解記事やAWS公式資料で補強するのがおすすめです。</p></section>'''
    marker = '<section id="categorySelect"'
    if marker in text:
        text = text.replace(marker, faq + '\n' + marker, 1)

p.write_text(text, encoding='utf-8')

# ---------- child pages ----------
exclude = {'.github', 'tools'}
page_urls = [BASE]
for d in sorted(x for x in ROOT.iterdir() if x.is_dir() and x.name not in exclude and not x.name.startswith('.')):
    page = d / 'index.html'
    if not page.exists():
        continue
    t = page.read_text(encoding='utf-8')
    t = normalize_counts(t)
    slug = d.name
    url = BASE + slug + '/'
    h1 = get_h1(t, slug.replace('-', ' '))
    if slug == 'guide':
        title = 'AWS Cloud Practitioner 図解学習ガイド｜CLF-C02対策｜ORIVECTOR'
        desc = 'AWS Cloud Practitioner（CLF-C02）の頻出テーマを図解で無料学習。AWSサービスの役割、違い、試験キーワード、ひっかけポイントを初心者向けに解説。'
    elif slug == 'roadmap':
        title = 'AWS Cloud Practitioner 勉強法・学習ロードマップ｜CLF-C02｜ORIVECTOR'
        desc = 'AWS Cloud Practitioner（CLF-C02）の学習ロードマップ。基礎学習、問題演習、模擬試験までの進め方を初心者向けに整理。'
    elif slug == 'about':
        title = 'ORIVECTOR AWS Cloud Practitioner学習サイトについて'
        desc = 'ORIVECTORのAWS Cloud Practitioner（CLF-C02）無料学習サイトについて、提供コンテンツと利用方法を紹介します。'
    else:
        title = f'{h1}とは？AWS Cloud Practitioner（CLF-C02）対策｜ORIVECTOR'
        desc = f'{h1}をAWS Cloud Practitioner（CLF-C02）試験向けに初心者にもわかりやすく解説。役割、使いどころ、似たAWSサービスとの違い、試験ポイントを整理。'
    t = set_title(t, title)
    t = set_canonical(t, url)
    t = add_robots(t)
    t = replace_meta(t, 'description', desc)
    t = replace_meta(t, 'og:title', title, prop=True)
    t = replace_meta(t, 'og:description', desc, prop=True)
    t = replace_meta(t, 'og:url', url, prop=True)
    schema = {
        '@context': 'https://schema.org',
        '@graph': [
            {'@type': ['Article', 'LearningResource'], '@id': url + '#article', 'headline': h1, 'description': desc, 'url': url, 'inLanguage': 'ja', 'isAccessibleForFree': True, 'educationalUse': '試験対策', 'publisher': {'@type': 'Organization', 'name': 'ORIVECTOR', 'url': 'https://orivector.jp/'}},
            {'@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'ORIVECTOR', 'item': 'https://orivector.jp/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'AWS Cloud Practitioner', 'item': BASE},
                {'@type': 'ListItem', 'position': 3, 'name': h1, 'item': url}
            ]}
        ]
    }
    t = add_schema(t, schema)
    page.write_text(t, encoding='utf-8')
    page_urls.append(url)

# ---------- robots + sitemap ----------
(ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: https://orivector.jp/aws-study/sitemap.xml\n', encoding='utf-8')
urls = sorted(set(page_urls))
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{html.escape(u)}</loc></url>\n' for u in urls) + '</urlset>\n'
(ROOT / 'sitemap.xml').write_text(xml, encoding='utf-8')
print(f'SEO v4 applied: {len(urls)} URLs')
