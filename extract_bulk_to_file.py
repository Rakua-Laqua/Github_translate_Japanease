import json
import re
from collections import Counter

dict_path = r'c:\Users\Rakua\Documents\VScode\Java script\ブラウザ拡張機能\Github_translate_Japanease\data\dictionary.json'
log_path = r'c:\Users\Rakua\Documents\VScode\Java script\ブラウザ拡張機能\Github_translate_Japanease\未翻訳ログ.json'
output_path = r'c:\Users\Rakua\Documents\VScode\Java script\ブラウザ拡張機能\Github_translate_Japanease\missing_full.json'

with open(dict_path, 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

with open(log_path, 'r', encoding='utf-8') as f:
    logs = json.load(f)

dict_keys = set(dictionary.keys())
dict_values = set(dictionary.values())

counts = Counter()
hints = {}
urls = {}
for log in logs:
    text = log['text'].strip()
    if not text: continue
    counts[text] += log.get('count', 1)
    if text not in hints:
        hints[text] = log.get('hint', '')
        urls[text] = log.get('url', '')

missing_all = []
for text, total_count in counts.most_common():
    if text in dict_keys or text in dict_values:
        continue
    
    if re.search(r'[ぁ-んァ-ヶー一-龠]', text): continue
    if '(GMT' in text or 'UTC' in text or 'AM GMT' in text or 'PM GMT' in text: continue
    if not any(c.isalpha() for c in text): continue
    
    if '/' in text and len(text.split('/')) == 2: continue
    if re.search(r'\d{1,2} [A-Z][a-z]{2} \d{4}', text): continue
    if re.search(r'[A-M][a-z]{2} \d{1,2}(st|nd|rd|th)?,? \d{4}', text): continue
    if re.search(r'\b[a-f0-9]{40}\b', text): continue
    
    # Technical IDs like content_scripts[0].js
    if '[' in text and ']' in text and ('.js' in text or '.css' in text): continue
    
    missing_all.append({
        "text": text,
        "count": total_count,
        "hint": hints[text],
        "url": urls[text]
    })

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(missing_all, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(missing_all)} items to {output_path}")
