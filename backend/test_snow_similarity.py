from Levenshtein import ratio
import re

def normalize_title(title):
    if not title: return ""
    title = re.sub(r'【[^】]+】', '', title)
    title = re.sub(r'\[[^\]]+\]', '', title)
    title = re.sub(r'[！？?!\s「」『』…、。・：:;]', '', title)
    return title.strip().lower()

# Based on the reported slugs and common patterns
t1 = "【話題】最強寒波で日本海側は「ドカ雪」警戒！帰省ラッシュへの影響は？"
t2 = "【話題】日本海側で記録的な大雪、交通機関に乱れも...帰省や旅行は計画的に"

n1 = normalize_title(t1)
n2 = normalize_title(t2)

print(f"Normalized 1: {n1}")
print(f"Normalized 2: {n2}")

sim = ratio(n1, n2)
print(f"Levenshtein Similarity: {sim:.2f}")

# Keyword overlap (important words)
keywords = ["雪", "大雪", "日本海", "帰省", "交通", "影響"]
match1 = [k for k in keywords if k in n1]
match2 = [k for k in keywords if k in n2]
common = set(match1).intersection(set(match2))
print(f"Common Keywords: {common}")
