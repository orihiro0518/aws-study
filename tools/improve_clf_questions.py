from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

replacements={
'ルートユーザーは強力な権限を持つため日常利用を避け、MFAで保護します。この説明に最も当てはまる選択肢はどれですか？':'ある企業が新しいAWSアカウントを作成しました。ルートユーザーに対するセキュリティ上のベストプラクティスとして、最も適切な対応はどれですか？',
'ソースコードの変更を起点にビルド、テスト、デプロイを一連のCI/CDフローとして自動化したい。何を使うか。最も適切なのはどれですか？':'ある開発チームは、ソースコードの変更後にビルド、テスト、デプロイの各ステージを順番に実行しています。複数のリリース工程をつなぎ、ワークフロー全体を自動化するAWSサービスはどれですか？',
'クラウド型コンタクトセンターを構築し、問い合わせフローを自動化したい。何を使うか。最も適切なのはどれですか？':'ある企業は、顧客からの電話やチャットによる問い合わせを受け付ける窓口を、物理的なコンタクトセンター設備を購入せずに構築したいと考えています。最も適切なAWSサービスはどれですか？',
'EC2インスタンスにアタッチして利用するブロックストレージはどれですか？':'ある企業はAmazon EC2上のデータベースで、インスタンスから低レイテンシで利用でき、停止後もデータを保持できる永続ストレージを必要としています。最も適切なAWSサービスはどれですか？',
'複数ソースのデータを抽出・変換・ロードし、データカタログも管理したい。何を使うか。最も適切なのはどれですか？':'ある企業は複数のデータソースを分析基盤へ統合するため、ETL処理をサーバー管理なしで実行し、データのスキーマなどのメタデータも一元管理したいと考えています。最も適切なAWSサービスはどれですか？'
}
changed=0
for old,new in replacements.items():
    if old in s:
        s=s.replace(old,new)
        changed+=1

# Make the root-user distractors plausible while preserving A as the correct option.
s=s.replace('ルートアクセスキーを全員で共有する','ルートユーザーのアクセスキーを作成し、管理者だけで共有する')
s=s.replace('ルートユーザーを日常の管理作業に使う','ルートユーザーを管理者専用アカウントとして日常の管理作業に使う')
s=s.replace('MFAを無効にする','ルートユーザーのパスワードを定期変更し、MFAは設定しない')

# Avoid changing question count, answer indexes, domains, navigation or UI.
# Only bump patch version when at least one targeted question was found.
if changed:
    m=re.search(r'Ver\s+(\d+)\.(\d+)\.(\d+)',s)
    if m:
        a,b,c=map(int,m.groups())
        s=s[:m.start()]+f'Ver {a}.{b}.{c+1}'+s[m.end():]

p.write_text(s,encoding='utf-8')
print(f'targeted questions updated: {changed}')
if changed < 3:
    raise SystemExit('Safety stop: expected target questions were not found; refusing broad rewrite')
