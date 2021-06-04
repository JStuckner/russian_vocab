import json

book = "Foundations"
chapter = "Chapter 4"
part = "Part 2"

with open('all_vocab.json', encoding='utf-8-sig') as j:
    vocab = json.load(j)

try:
    _ = vocab[book][chapter]
except KeyError:
    vocab[book][chapter] = {}

vocab[book][chapter][part] = []

with open('chapter 4\\p2.txt', 'r', encoding='utf-8-sig') as f:
    data = f.readlines()
    data = [x.strip() for x in data]

for l in data:
    a = l.split("_")
    r = a[0].strip()
    print(a[0])
    e = a[1].strip()
    vocab[book][chapter][part].append({"russian" : r, "english" : e})


with open('all_vocab.json', 'w', encoding='utf-8-sig') as f:
    json.dump(vocab, f, ensure_ascii=False)
