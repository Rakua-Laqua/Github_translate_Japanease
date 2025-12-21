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
dict_values = set(dictionary.values())

# Aggregate counts for each text
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

# Filter and sort
missing_all = []
for text, total_count in counts.most_common():
    if text in dict_keys or text in dict_values:
        continue
    
    # Exclusions (Refined)
    if re.search(r'[ぁ-んァ-ヶー一-龠]', text): continue # Japanese
    if '(GMT' in text or 'UTC' in text or 'AM GMT' in text or 'PM GMT' in text: continue # Time
    if not any(c.isalpha() for c in text): continue # No letters
    
    # Specific noise (Highly improved for larger batch)
    if '/' in text and len(text.split('/')) == 2: continue # Repo names
    if re.search(r'\d{1,2} [A-Z][a-z]{2} \d{4}', text): continue # Date formats
    if re.search(r'[A-M][a-z]{2} \d{1,2}(st|nd|rd|th)?,? \d{4}', text): continue # Date formats
    if re.search(r'\b[a-f0-9]{40}\b', text): continue # Commit hash
    if text.startswith('Created with '): continue # Metadata (Highcharts etc already added mostly)
    
    # Exclude technical IDs
    if '_' in text and not ' ' in text and len(text) > 15: continue 
    
    missing_all.append({
        "text": text,
        "count": total_count,
        "hint": hints[text],
        "url": urls[text]
    })

# Output top 500 to catch everything
print(json.dumps(missing_all[:500], ensure_ascii=False, indent=2))
