import unicodedata
import sys

results = []
for codepoint in range(sys.maxunicode + 1):
    char = chr(codepoint)

    if char.isascii():
        continue

    normalised = unicodedata.normalize('NFKD', char)

    if normalised.isascii() and len(normalised) > 1:
        results.append(char + " " + normalised)

with open("ligatures.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(results))
