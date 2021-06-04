import string
import json

def split_letters(old_string):
    index = -1
    for i, char in enumerate(old_string):
        if char in string.ascii_lowercase or char in 'BR':
            index = i
            break
    else:
        raise ValueError("No letters found") # or return old_string
    return [old_string[:index].strip(), old_string[index:].strip()]

words = []

with open('vocab\\chapter1p1.txt', 'r', encoding='utf-8-sig') as f:
    data = f.readlines()
data = [x.strip() for x in data]

for l in data:
    a = split_letters(l)
    words.append({"english": a[1], "russian": a[0], "chapter": 1, "part": 1})

with open('vocab\\chapter1.json', 'w', encoding='utf-8-sig') as f:
    json.dump(words, f, ensure_ascii=False)
