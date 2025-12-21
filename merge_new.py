import json
import os

# ファイルパス
DICT_PATH = "data/dictionary.json"
NEW_PATH = "new_translations.json"

# 辞書を読み込み
with open(DICT_PATH, 'r', encoding='utf-8') as f:
    dictionary = json.load(f)

# 新しい翻訳を読み込み
with open(NEW_PATH, 'r', encoding='utf-8') as f:
    new_translations = json.load(f)

# 既存件数
old_count = len(dictionary)

# マージ
dictionary.update(new_translations)

# 新件数
new_count = len(dictionary)
added = new_count - old_count

# 保存
with open(DICT_PATH, 'w', encoding='utf-8') as f:
    json.dump(dictionary, f, ensure_ascii=False, indent=2)

print(f"マージ完了: {old_count} -> {new_count} ({added}件追加)")

# 一時ファイル削除
os.remove(NEW_PATH)
print(f"{NEW_PATH} を削除しました")
