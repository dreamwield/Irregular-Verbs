"""
Bundle verbs_data.json and lyrics JSONs into a standalone data.js
ensuring index.html works with zero CORS restrictions even when opened directly via file://
"""
import json

with open("verbs_data.json", "r", encoding="utf-8") as f:
    verbs_data = json.load(f)

with open("rhymes_lyrics.json", "r", encoding="utf-8") as f:
    rhymes_lyrics = json.load(f)

with open("atoz_lyrics.json", "r", encoding="utf-8") as f:
    atoz_lyrics = json.load(f)

with open("quiz_lyrics.json", "r", encoding="utf-8") as f:
    quiz_lyrics = json.load(f)

js_content = f"""// Auto-generated data bundle for offline & file:// compatibility
const VERBS_DATA = {json.dumps(verbs_data, ensure_ascii=False, indent=2)};

const RHYMES_LYRICS = {json.dumps(rhymes_lyrics, ensure_ascii=False, indent=2)};

const ATOZ_LYRICS = {json.dumps(atoz_lyrics, ensure_ascii=False, indent=2)};

const QUIZ_LYRICS = {json.dumps(quiz_lyrics, ensure_ascii=False, indent=2)};
"""

with open("data.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("Successfully generated data.js bundle!")
