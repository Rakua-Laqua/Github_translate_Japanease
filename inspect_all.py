import json
import re
from collections import Counter

dict_path = r'c:\Users\Rakua\Documents\VScode\Java script\ブラウザ拡張機能\Github_translate_Japanease\data\dictionary.json'
log_path = r'c:\Users\Rakua\Documents\VScode\Java script\ブラウザ拡張機能\Github_translate_Japanease\未翻訳ログ.json'

def normalize(text):
    if not text: return ""
    return re.sub(r'\s+', ' ', text.strip())

with open(dict_path, 'r', encoding='utf-8') as f:
    dictionary = json.load(f)
    dict_keys = set(normalize(k) for k in dictionary.keys())

with open(log_path, 'r', encoding='utf-8') as f:
    logs = json.load(f)

# dict_keys = set(dictionary.keys()) # Deleted

url_counts = Counter()
text_counts = Counter()
text_to_url = {}

for log in logs:
    text = normalize(log['text'])
    if not text: continue
    url = log.get('url', 'unknown')
    url_counts[url] += 1
    
    if text not in dict_keys:
        text_counts[text] += log.get('count', 1)
        if text not in text_to_url:
            text_to_url[text] = url

print("--- URL Summary ---")
for url, count in url_counts.most_common(20):
    print(f"{count:4} | {url}")

print("\n--- Remaining Missing Texts (All) ---")
# Very loose filtering to catch everything the user might be seeing
sorted_missing = sorted(text_counts.items(), key=lambda x: x[1], reverse=True)
for text, count in sorted_missing:
    if re.search(r'[ぁ-んァ-ヶー一-龠]', text): continue
    if not any(c.isalpha() for c in text): continue
    # Skip very obvious repo names or hashes
    if '/' in text and ' ' not in text: continue
    if re.search(r'\b[a-f0-9]{40}\b', text): continue
    
    print(f"{count:3} | {text} (URL: {text_to_url[text]})")
