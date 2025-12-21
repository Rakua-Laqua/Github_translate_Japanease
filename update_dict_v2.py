import json
import os

dict_path = r'c:\Users\Rakua\Documents\VScode\Java script\ブラウザ拡張機能\Github_translate_Japanease\data\dictionary.json'

new_entries = {
    "Japanese consumption tax (JCT) is not included in the amounts shown above.": "上記の金額には、日本の消費税（JCT）は含まれておりません。",
    "(repo:mona/a OR repo:mona/b) AND lang:python": "(repo:mona/a または repo:mona/b) かつ lang:python",
    "Watch: Participating in Rakua-Laqua/Github_translate_Japanease": "ウォッチ：Rakua-Laqua/Github_translate_Japanease のアクティビティを購読中",
    "Fork your own copy of Rakua-Laqua/Github_translate_Japanease": "Rakua-Laqua/Github_translate_Japanease をフォークして自分のコピーを作成",
    "Upgrade to Pro": "Pro にアップグレード",
    "Manage subscription": "サブスクリプションを管理",
    "Payment method": "支払い方法",
    "Payment methods": "支払い方法",
    "Billing information": "請求情報",
    "Invoices": "請求書",
    "Cost centers": "コストセンター",
    "Azure subscription": "Azure サブスクリプション",
    "Coupons": "クーポン",
    "Merged": "マージ済み",
    "Draft": "ドラフト",
    "Approved": "承認済み",
    "Changes requested": "修正リクエスト済み",
    "Review changes": "コードレビューを変更",
    "Commit details": "コミット詳細",
    "View details": "詳細を表示",
    "Compare & pull request": "比較してプルリクエストを作成",
    "Open a pull request": "プルリクエストを作成",
    "Create a new pull request": "新しいプルリクエストを作成",
    "Confirm merge": "マージを確定",
    "Delete branch": "ブランチを削除",
    "Restore branch": "ブランチを復元",
    "Pull request successfully merged and closed": "プルリクエストが正常にマージされ、クローズされました",
    "You’re all set—the {branch} branch can be safely deleted.": "準備が整いました。{branch} ブランチは安全に削除できます。",
    "Manage subscriptions": "サブスクリプションを管理",
    "Billing cycle": "請求サイクル",
    "Next payment due": "次回お支払い期限",
    "View all billing history": "すべての支払い履歴を表示",
    "Billed history": "支払い履歴",
}

with open(dict_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for k, v in new_entries.items():
    if k not in data:
        data[k] = v

with open(dict_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Dictionary updated successfully with incremental items.")
