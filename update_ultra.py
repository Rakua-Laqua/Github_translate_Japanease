import json
import os

dict_path = r'c:\Users\Rakua\Documents\VScode\Java script\ブラウザ拡張機能\Github_translate_Japanease\data\dictionary.json'

new_entries = {
    "Learn more": "詳細を見る",
    "No results found": "結果が見つかりません",
    "Select at least one repository. Max 50 repositories. Also includes public repositories (read-only).": "少なくとも1つのリポジトリを選択してください。最大50リポジトリまで選択可能です。公開リポジトリ（読み取り専用）も含まれます。",
    "This applies to all current and future repositories you own. Also includes public repositories (read-only).": "これは現在および将来あなたが所有するすべてのリポジトリに適用されます。公開リポジトリ（読み取り専用）も含まれます。",
    "GitHub strongly recommends that you set an expiration date for your token to help keep your information secure.": "情報の安全性を保つため、トークンには有効期限を設定することを強くお勧めします。",
    "The requires a maximum lifetime of 0 days for fine-grained personal access tokens. As an enterprise administrator you are exempted from this requirement.": "微細な制御が可能な個人アクセストークンに対して、最大有効期間を0日に設定する必要があります。エンタープライズ管理者の場合、この要件は免除されます。",
    "The token will only be able to make changes to resources owned by the selected resource owner. Tokens can always read all public repositories.": "このトークンは、選択したリソース所有者が所有するリソースに対してのみ変更を加えることができます。トークンは常にすべての公開リポジトリを読み取ることができます。",
    "A unique name for this token. May be visible to resource owners or users with possession of the token.": "このトークンの一意の名前です。リソース所有者やトークンを所持しているユーザーに表示される場合があります。",
    "Create a fine-grained, repository-scoped token suitable for personal API use and for using Git over HTTPS.": "個人の API 利用や HTTPS 経由での Git 利用に適した、微細な制御が可能なリポジトリスコープのトークンを作成します。",
    "This application will receive bits of Editor Context (e.g. currently opened file) whenever you send it a message through Copilot Chat.": "このアプリケーションは、Copilot チャットを通じてメッセージを送信するたびに、エディタコンテキスト（現在開いているファイルなど）の一部を受け取ります。",
    "This application will receive your GitHub ID, your GitHub Copilot Chat session messages (not including messages sent to another application), and timestamps of provided GitHub Copilot Chat session messages. This permission must be enabled for Copilot Extensions.": "このアプリケーションは、あなたの GitHub ID、GitHub Copilot チャットセッションメッセージ（他のアプリケーションに送信されたメッセージを除く）、および提供された GitHub Copilot チャットセッションメッセージのタイムスタンプを受け取ります。Copilot 拡張機能を利用するには、この権限を有効にする必要があります。",
    "Gist": "Gist",
    "30 days (Jan 20, 2026)": "30日間 (2026年1月20日まで)",
    "90 days (Mar 21, 2026)": "90日間 (2026年3月21日まで)",
    "60 days (Feb 19, 2026)": "60日間 (2026年2月19日まで)",
    "7 days (Dec 28, 2025)": "7日間 (2025年12月28日まで)",
}

with open(dict_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for k, v in new_entries.items():
    if k not in data:
        data[k] = v

with open(dict_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Dictionary updated with {len(new_entries)} items for v1.1.16.")
