import json
import os

dict_path = r'c:\Users\Rakua\Documents\VScode\Java script\ブラウザ拡張機能\Github_translate_Japanease\data\dictionary.json'

new_entries = {
    # Billing & Plan
    "20GB of Codespaces storage": "20GB の Codespaces ストレージ",
    "180 core-hours of Codespaces compute": "180 コア時間の Codespaces コンピューティング",
    "2GB of Packages storage": "2GB の Packages ストレージ",
    "3,000 Actions minutes/month": "月間 3,000 分の Actions 実行時間",
    "Hide Usage Breakdown": "使用内訳を非表示",
    "Copilot Premium Request": "Copilot プレミアムリクエスト",
    "Units": "単位",
    "and more": "など",
    
    # Address/Payment Form
    "(Apartment, suite, unit)": "(アパート、部屋番号、ユニット)",
    "(Street, P.O. box)": "(通り、私書箱)",
    "First name": "名",
    "Last name": "姓",
    "Company": "会社名",
    "Address line 1": "住所 1",
    "Address line 2": "住所 2",
    "City": "市区町村",
    "State / Province": "都道府県 / 州",
    "Zip / Postal code": "郵便番号",
    "Country / Region": "国 / 地域",
    "Phone number": "電話番号",
    "Primary email": "メインのメールアドレス",
    
    # Countries (Common ones seen in logs)
    "Japan": "日本",
    "United States": "アメリカ合衆国",
    "Afghanistan": "アフガニスタン",
    "Albania": "アルバニア",
    "Algeria": "アルジェリア",
    "Andorra": "アンドラ",
    "Angola": "アンゴラ",
    "Anguilla": "アンギラ",
    "Antarctica": "南極大陸",
    
    # Long explanation in Billing
    "Billable spend for Actions and Actions Runners for the selected timeframe. Applicable discounts cover Actions usage in public repositories and included usage for Actions minutes and storage.": "選択した期間内の Actions および Actions ランナーの課金対象支出です。適用される割引には、パブリックリポジトリでの Actions の使用、および Actions の実行時間とストレージの含まれる使用量が含まれます。",
}

with open(dict_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for k, v in new_entries.items():
    if k not in data:
        data[k] = v

with open(dict_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Dictionary updated with {len(new_entries)} items for v1.1.17.")
