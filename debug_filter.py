import json
import re
from collections import Counter

dict_path = r'c:\Users\Rakua\Documents\VScode\Java script\ブラウザ拡張機能\Github_translate_Japanease\data\dictionary.json'
log_path = r'c:\Users\Rakua\Documents\VScode\Java script\ブラウザ拡張機能\Github_translate_Japanease\未翻訳ログ.json'

with open(dict_path, 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

with open(log_path, 'r', encoding='utf-8') as f:
    logs = json.load(f)

dict_keys = set(dictionary.keys())

counts = Counter()
for log in logs:
    text = log['text'].strip()
    if not text: continue
    counts[text] += log.get('count', 1)

ignored = []
candidates = []

for text, count in counts.most_common():
    if text in dict_keys:
        continue
    
    # Check why it might be ignored
    is_japanese = bool(re.search(r'[ぁ-んァ-ヶー一-龠]', text))
    is_time = '(GMT' in text or 'UTC' in text or 'AM GMT' in text or 'PM GMT' in text
    no_alpha = not any(c.isalpha() for c in text)
    is_repo = '/' in text and len(text.split('/')) == 2 and ' ' not in text
    is_date = bool(re.search(r'\d{1,2} [A-Z][a-z]{2} \d{4}', text))
    is_hash = bool(re.search(r'\b[a-f0-9]{40}\b', text))
    
    if is_japanese or is_time or no_alpha or is_repo or is_date or is_hash:
        ignored.append({"text": text, "reason": "filter"})
    else:
        candidates.append({"text": text, "count": count})

print("--- Ignored Items (First 50) ---")
for item in ignored[:50]:
    print(f"[{item['reason']}] {item['text']}")

print("\n--- Candidates to translate (All remaining) ---")
for item in candidates:
    print(f"Count: {item['count']} | Text: {item['text']}")
