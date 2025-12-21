import json
import os

dict_path = r'c:\Users\Rakua\Documents\VScode\Java script\ブラウザ拡張機能\Github_translate_Japanease\data\dictionary.json'
log_path = r'c:\Users\Rakua\Documents\VScode\Java script\ブラウザ拡張機能\Github_translate_Japanease\未翻訳ログ.json'

with open(dict_path, 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

with open(log_path, 'r', encoding='utf-8') as f:
    logs = json.load(f)

# Collect all keys and all values to check against
dict_keys = set(dictionary.keys())
dict_values = set(dictionary.values())

missing = {}
for log in logs:
    text = log['text'].strip()
    if not text: continue
    
    # If the text is already a key or already a value (translated), skip it
    if text in dict_keys or text in dict_values:
        continue
    
    # Filter out common noise
    if '(GMT' in text or 'UTC' in text or 'AM GMT' in text or 'PM GMT' in text:
        continue
    
    # Filter out anything with Japanese characters already (it's likely a content string or already translated)
    import re
    if re.search(r'[ぁ-んァ-ヶー一-龠]', text):
        continue

    # Filter out likely dynamic IDs/Names (has numbers or is just a name)
    if text.startswith('Rakua-Laqua'): continue
    
    missing[text] = log.get('type', 'unknown')

print(json.dumps(missing, ensure_ascii=False, indent=2))
