from Levenshtein import ratio
import re

def normalize_title(title):
    # Remove 【】 and its content
    title = re.sub(r'【[^】]+】', '', title)
    # Remove punctuation
    title = re.sub(r'[！？?!\s「」『』…、。]', '', title)
    return title.strip()

t1 = "【話題】なぜ？日本も民間も「AI導入」がガチ勢に？導入に動く行政と企業の思惑とは"
t2 = "【話題】「もう待ったなし！」行政と民間企業がAI活用に奔走する理由とは？"

n1 = normalize_title(t1)
n2 = normalize_title(t2)

print(f"Original 1: {t1}")
print(f"Original 2: {t2}")
print(f"Normalized 1: {n1}")
print(f"Normalized 2: {n2}")

sim = ratio(n1, n2)
print(f"Levenshtein Similarity (Normalized): {sim:.2f}")

# Keyword overlap
def keyword_overlap(s1, s2):
    # Very simple keyword check
    words1 = set([s1[i:i+2] for i in range(len(s1)-1)]) # Bigrams as keywords
    words2 = set([s2[i:i+2] for i in range(len(s2)-1)])
    overlap = words1.intersection(words2)
    if not words1: return 0
    return len(overlap) / len(words1)

overlap = keyword_overlap(n1, n2)
print(f"Bigram Overlap: {overlap:.2f}")
