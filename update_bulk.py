import json
import os

dict_path = r'c:\Users\Rakua\Documents\VScode\Java script\ブラウザ拡張機能\Github_translate_Japanease\data\dictionary.json'

new_entries = {
    # Access & Permissions
    "Access:": "アクセス:",
    "Read-only": "読み取り専用",
    "Read and write": "読み取りおよび書き込み",
    "Read-only access to public repositories.": "公開リポジトリへの読み取り専用アクセス。",
    "Full control of private repositories": "プライベートリポジトリの完全な制御",
    
    # Settings Navigation
    "Developer Settings": "開発者設定",
    "Personal access tokens": "個人アクセストークン",
    "Tokens (classic)": "トークン（従来版）",
    "Fine-grained tokens": "微細な制御トークン",
    "OAuth Apps": "OAuth アプリ",
    "GitHub Apps": "GitHub アプリ",
    "Resource owner": "リソース所有者",
    "Token name": "トークン名",
    "Expiration": "有効期限",
    "No expiration": "有効期限なし",
    
    # Categories / Types
    "Git SSH keys": "Git SSH キー",
    "SSH signing keys": "SSH 署名キー",
    "Email addresses": "メールアドレス",
    "Copilot Chat": "Copilot チャット",
    "Codespaces user secrets": "Codespaces ユーザーシークレット",
    "Block another user": "他のユーザーをブロック",
    "Private repository invitations": "プライベートリポジトリへの招待",
    "Plan": "プラン",
    "GPG keys": "GPG キー",
    "Followers": "フォロワー",
    "Events": "イベント",
    "Copilot Requests": "Copilot リクエスト",
    "Copilot Editor Context": "Copilot エディタコンテキスト",
    "Starring": "スター",
    "Watching": "ウォッチ",
    "Profile": "プロフィール",
    "Interaction limits": "インタラクション制限",
    "Gists": "Gist",
    "Models": "モデル",
    
    # Descriptions & Help Text (Long patterns)
    "Starring. More information available below.": "スター。詳細は以下をご参照ください。",
    "List and manage repositories a user is starring.": "ユーザーがスターを付けているリポジトリの一覧表示と管理。",
    "SSH signing keys. More information available below.": "SSH 署名キー。詳細は以下をご参照ください。",
    "View and manage a user's SSH signing keys.": "ユーザーの SSH 署名キーの表示と管理。",
    "Email addresses. More information available below.": "メールアドレス。詳細は以下をご参照ください。",
    "Manage a user's email addresses.": "ユーザーのメールアドレスの管理。",
    "Copilot Chat. More information available below.": "Copilot チャット。詳細は以下をご参照ください。",
    "Codespaces user secrets. More information available below.": "Codespaces ユーザーシークレット。詳細は以下をご参照ください。",
    "Manage Codespaces user secrets.": "Codespaces ユーザーシークレットの管理。",
    "Block another user. More information available below.": "他のユーザーをブロック。詳細は以下をご参照ください。",
    "View and manage users blocked by the user.": "ユーザーによってブロックされたユーザーの表示と管理。",
    "Watching. More information available below.": "ウォッチ。詳細は以下をご参照ください。",
    "List and change repositories a user is subscribed to.": "ユーザーが購読しているリポジトリの一覧表示と変更。",
    "Profile. More information available below.": "プロフィール。詳細は以下をご参照ください。",
    "Manage a user's profile settings.": "ユーザーのプロフィール設定の管理。",
    "Private repository invitations. More information available below.": "プライベートリポジトリへの招待。詳細は以下をご参照ください。",
    "View a user's invitations to private repositories": "プライベートリポジトリへの招待の表示。",
    "Plan. More information available below.": "プラン。詳細は以下をご参照ください。",
    "View a user's plan.": "ユーザーのプランの表示。",
    "Models. More information available below.": "モデル。詳細は以下をご参照ください。",
    "Allows access to GitHub Models.": "GitHub Models へのアクセスを許可します。",
    "Interaction limits. More information available below.": "インタラクション制限。詳細は以下をご参照ください。",
    "Interaction limits on repositories": "リポジトリのインタラクション制限。",
    "Git SSH keys. More information available below.": "Git SSH キー。詳細は以下をご参照ください。",
    "Gists. More information available below.": "Gist。詳細は以下をご参照ください。",
    "Create and modify a user's gists and comments.": "ユーザーの Gist やコメントの作成と修正。",
    "GPG keys. More information available below.": "GPG キー。詳細は以下をご参照ください。",
    "View and manage a user's GPG keys.": "ユーザーの GPG キーの表示と管理。",
    "Followers. More information available below.": "フォロワー。詳細は以下をご参照ください。",
    "A user's followers": "ユーザーのフォロワー。",
    "Events. More information available below.": "イベント。詳細は以下をご参照ください。",
    "View events triggered by a user's activity.": "ユーザーのアクティビティによってトリガーされたイベントの表示。",
    "Copilot Requests. More information available below.": "Copilot リクエスト。詳細は以下をご参照ください。",
    "Send Copilot requests.": "Copilot リクエストの送信。",
    "Copilot Editor Context. More information available below.": "Copilot エディタコンテキスト。詳細は以下をご参照ください。",
    "This token will be ready for use immediately.": "このトークンはすぐに使用できるようになります。",
    "Learn more about permissions.": "権限の詳細を見る。",
    "Choose the minimal permissions necessary for your needs.": "必要最低限の権限を選択してください。",
    "The token will expire on the selected date": "トークンは選択した日付に期限切れになります",
    "Expiration date can't be blank": "有効期限を空にすることはできません",
    "You may only select resource owners with fine-grained PATs enabled.": "微細な制御が可能な PAT が有効なリソース所有者のみを選択できます。",
    
    # UI Actions
    "Remove Starring": "スターを削除",
    "Remove SSH signing keys": "SSH 署名キーを削除",
    "Remove Email addresses": "メールアドレスを削除",
    "Remove Copilot Chat": "Copilot チャットを削除",
    "Remove Codespaces user secrets": "Codespaces ユーザーシークレットを削除",
    "Remove Block another user": "ブロックを解除",
    "Remove Watching": "ウォッチを解除",
    "Remove Profile": "プロフィールを削除",
    "Remove Private repository invitations": "招待を削除",
    "Remove Plan": "プランを削除",
    "Remove Models": "モデルを削除",
    "Remove Interaction limits": "制限を解除",
    "Remove Git SSH keys": "Git SSH キーを削除",
    "Remove Gists": "Gist を削除",
    "Remove GPG keys": "GPG キーを削除",
    "Remove Followers": "フォロワーを削除",
    "Remove Events": "イベントを削除",
    "Remove Copilot Requests": "Copilot リクエストを削除",
    "Remove Copilot Editor Context": "Copilot エディタコンテキストを削除",
    "Generate token": "トークンを生成",
    "Add permissions": "権限を追加",
    "Only select repositories": "リポジトリのみを選択",
    "Public repositories": "公開リポジトリ",
    "Repository access": "リポジトリへのアクセス",
    "Select date *": "日付を選択 *",
    "Select resource owner": "リソース所有者を選択",
    "Retry check": "再試行",
    
    # Status & Others
    "Permission Blank Slate": "権限が選択されていません",
    "Sorry, something went wrong.": "申し訳ありません。問題が発生しました。",
    "Something went wrong while checking. Please retry.": "確認中に問題が発生しました。再試行してください。",
    "for more information.": "詳細情報。",
    "See the documentation": "ドキュメントを見る",
    "Authorization check": "認証チェック",
    "Loading content...": "コンテンツを読み込み中...",
}

with open(dict_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for k, v in new_entries.items():
    if k not in data:
        data[k] = v

with open(dict_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Dictionary updated with {len(new_entries)} items for v1.1.15.")
