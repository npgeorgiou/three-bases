import json,re
y="5154 5155 5156 5157 5158 5159 5162 5310 5314 5315 5316 5352 5727 5731 5732 5799 5903 6061 6065 6236 6237 6238 6241 6460 6606 6950 6951 7097 7527 7528 7529 7530 7531 7532 7533 7534 7535 7536 7751 7955 8203 8228 8429".split()
ids=[l.split(' | ')[0].rstrip('*') for l in open('settle_001.txt') if re.match(r'^\d+\*? \|',l)]
json.dump({i:("yes" if i in y else "no") for i in ids},open('C/settle_001.json','w'))
print(len(ids))
