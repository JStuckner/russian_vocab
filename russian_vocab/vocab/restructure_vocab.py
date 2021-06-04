import json

with open('vocab.json', encoding='utf-8-sig') as j:
    foundations = json.load(j)

with open('vocab_data.json', encoding='utf-8-sig') as j:
    troika = json.load(j)

vocab = {}
vocab['Troika'] = {}
vocab['Foundations'] = {}

for c in troika["allChapterData"]:
    vocab['Troika'][c['name']] = {}
    vocab['Troika'][c['name']]['Part 1'] = c['words']

for c in ['Chapter 1', 'Chapter 2']:
    vocab['Foundations'][c] = {}
    for p in ['Part 1', 'Part 2']:
        vocab['Foundations'][c][p] = {}
vocab['Foundations']['Chapter 1']['Part 3'] = {}

c = ['0', 'Chapter 1', 'Chapter 2']
p = ['0', 'Part 1', 'Part 2', 'Part 3']
for v in foundations:
    vocab['Foundations'][c[v['chapter']]][p[v['part']]] = []
for v in foundations:
    vocab['Foundations'][c[v['chapter']]][p[v['part']]].append({'english':v['english'], 'russian':v['russian']})

with open('all_vocab.json', 'w', encoding='utf-8-sig') as f:
    json.dump(vocab, f, ensure_ascii=False)
