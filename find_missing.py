import json
import re

dict_path = r'c:\Users\Rakua\Documents\VScode\Java script\ブラウザ拡張機能\Github_translate_Japanease\data\dictionary.json'
log_path = r'c:\Users\Rakua\Documents\VScode\Java script\ブラウザ拡張機能\Github_translate_Japanease\未翻訳ログ.json'

with open(dict_path, 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

with open(log_path, 'r', encoding='utf-8') as f:
    logs = json.load(f)

unique_texts = sorted(list(set(log['text'] for log in logs)))

missing = []
for text in unique_texts:
    # 既存辞書にあるか確認
    if text in dictionary:
        continue
    
    # 日本語が含まれているか確認（既訳または日本語コンテンツ）
    if re.search(r'[ぁ-んァ-ヶー一-龠]', text):
        continue
        
    # タイムゾーン除外
    if '(GMT' in text or 'UTC' in text or 'AM GMT' in text or 'PM GMT' in text:
        continue
    
    # 言語名除外（一部重要そうなものは残すかもしれないが基本除外）
    # 主要な言語名をリストアップして除外
    languages = [
        "Abkhazian", "Afar", "Afrikaans", "Akan", "Albanian", "Amharic", "Arabic", "Aragonese", 
        "Armenian", "Assamese", "Avaric", "Avestan", "Aymara", "Azerbaijani", "Bambara", "Bashkir", 
        "Basque", "Belarusian", "Bengali", "Bislama", "Bosnian", "Breton", "Bulgarian", "Burmese", 
        "Catalan", "Chamorro", "Chinese", "Chuvash", "Cornish", "Corsican", "Cree", "Croatian", 
        "Czech", "Danish", "Dutch", "Dzongkha", "English", "Esperanto", "Estonian", "Ewe", 
        "Faroese", "Fijian", "Finnish", "French", "Fulah", "Galician", "Ganda", "Georgian", 
        "German", "Greek", "Guarani", "Gujarati", "Hausa", "Hebrew", "Herero", "Hindi", "Hungarian", 
        "Icelandic", "Ido", "Igbo", "Indonesian", "Interlingua", "Interlingue", "Inuktitut", 
        "Inupiaq", "Irish", "Italian", "Japanese", "Javanese", "Kalaallisut", "Kannada", "Kanuri", 
        "Kashmiri", "Kazakh", "Kinyarwanda", "Kirghiz", "Komi", "Kongo", "Korean", "Kuanyama", 
        "Kurdish", "Lao", "Latin", "Latvian", "Lingala", "Lithuanian", "Luxembourgish", "Macedonian", 
        "Malagasy", "Malay", "Malayalam", "Maltese", "Manx", "Maori", "Marathi", "Marshallese", 
        "Mongolian", "Nauru", "Nepali", "Ndonga", "Norwegian", "Occitan", "Ojibwa", "Oriya", 
        "Oromo", "Ossetian", "Pali", "Persian", "Polish", "Portuguese", "Quechua", "Romansh", 
        "Rundi", "Russian", "Samoan", "Sango", "Sanskrit", "Sardinian", "Serbian", "Shona", 
        "Sindhi", "Sinhala", "Slovak", "Slovenian", "Somali", "Spanish", "Sundanese", "Swahili", 
        "Swati", "Swedish", "Tagalog", "Tahitian", "Tajik", "Tamil", "Tatar", "Telugu", "Thai", 
        "Tibetan", "Tigrinya", "Tsonga", "Tswana", "Turkish", "Turkmen", "Twi", "Uighur", 
        "Ukrainian", "Urdu", "Uzbek", "Venda", "Vietnamese", "Volapük", "Walloon", "Welsh", 
        "Wolof", "Xhosa", "Yiddish", "Yoruba", "Zhuang", "Zulu"
    ]
    if text in languages:
        continue

    # 記号のみ、数字のみ、短すぎる、長すぎる、などはとりあえず除外
    if not any(c.isalpha() for c in text): continue
    if len(text) < 2: continue
    
    # 特定のサービス名やユーザー名、リポジトリ名っぽいやつを除外
    if 'Rakua-Laqua' in text or 'Github_translate_Japanease' in text:
        continue
    if text.startswith('repo:'):
        continue
    
    missing.append(text)

with open('missing_texts.json', 'w', encoding='utf-8') as f:
    json.dump(missing, f, ensure_ascii=False, indent=2)

print(f"Found {len(missing)} missing texts.")
