import json
import os

dict_path = r'c:\Users\Rakua\Documents\VScode\Java script\ブラウザ拡張機能\Github_translate_Japanease\data\dictionary.json'

new_entries = {
    # Security & Sessions
    "Active sessions": "アクティブなセッション",
    "This is a list of devices that have logged into your account. Revoke any sessions that you do not recognize.": "あなたのカウントにログインしているデバイスの一覧です。心当たりのないセッションは取り消してください。",
    "Revoke all": "すべて取り消す",
    "Revoke session": "セッションを取り消す",
    "Current session": "現在のセッション",
    "Last accessed on": "最終アクセス日:",
    "Seen in": "所在地:",
    "Two-factor authentication": "二要素認証",
    "Two-factor authentication adds an additional layer of security to your account by requiring more than just a password to log in.": "二要素認証は、ログイン時にパスワード以上のものを要求することで、アカウントにセキュリティの層を追加します。",
    "Security log": "セキュリティログ",
    "This is a log of security events related to your account.": "あなたのアカウントに関連するセキュリティイベントのログです。",
    
    # Billing & Usage details
    "7 requests": "7 リクエスト",
    "Gemini 3 Pro": "Gemini 1.5 Pro", # Correction to likely real name or keeping as is if specifically displayed
    "Copilot Premium Request": "Copilot プレミアムリクエスト",
    "Usage Monday, 1 Dec 2025": "2025年12月1日(月)の使用量",
    
    # Missing Countries & Regions
    "Australia": "オーストラリア",
    "Austria": "オーストリア",
    "Azerbaijan": "アゼルバイジャン",
    "Bahamas": "バハマ",
    "Bahrain": "バーレーン",
    "Bangladesh": "バングラデシュ",
    "Barbados": "バルバドス",
    "Belarus": "ベラルーシ",
    "Belgium": "ベルギー",
    "Belize": "ベリーズ",
    "Benin": "ベナン",
    "Bermuda": "バミューダ",
    "Bhutan": "ブータン",
    "Bolivia": "ボリビア",
    "Bosnia and Herzegovina": "ボスニア・ヘルツェゴビナ",
    "Botswana": "ボツワナ",
    "Brazil": "ブラジル",
    "Bulgaria": "ブルガリア",
    "Canada": "カナダ",
    "Chile": "チリ",
    "China": "中国",
    "Colombia": "コロンビア",
    "Costa Rica": "コスタリカ",
    "Croatia": "クロアチア",
    "Cyprus": "キプロス",
    "Czech Republic": "チェコ共和国",
    "Denmark": "デンマーク",
    "Egypt": "エジプト",
    "Finland": "フィンランド",
    "France": "フランス",
    "Germany": "ドイツ",
    "Greece": "ギリシャ",
    "Hong Kong": "香港",
    "Hungary": "ハンガリー",
    "Iceland": "アイスランド",
    "India": "インド",
    "Indonesia": "インドネシア",
    "Ireland": "アイルランド",
    "Israel": "イスラエル",
    "Italy": "イタリア",
    "Korea, Republic of": "大韓民国",
    "Luxembourg": "ルクセンブルク",
    "Malaysia": "マレーシア",
    "Mexico": "メキシコ",
    "Netherlands": "オランダ",
    "New Zealand": "ニュージーランド",
    "Norway": "ノルウェー",
    "Philippines": "フィリピン",
    "Poland": "ポーランド",
    "Portugal": "ポルトガル",
    "Singapore": "シンガポール",
    "South Africa": "南アフリカ",
    "Spain": "スペイン",
    "Sweden": "スウェーデン",
    "Switzerland": "スイス",
    "Taiwan": "台湾",
    "Thailand": "タイ",
    "Turkey": "トルコ",
    "United Kingdom": "イギリス",
    "Vietnam": "ベトナム",
}

with open(dict_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for k, v in new_entries.items():
    if k not in data:
        data[k] = v

with open(dict_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Dictionary updated with {len(new_entries)} items for v1.1.18.")
