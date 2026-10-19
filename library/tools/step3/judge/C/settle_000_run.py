import json
y="214 657 1267 1729 2070 2553 2605 2685 2686 2687 2884 3424 3797 3799 3801 4029 4261 4434 4896 4948 4949 4951".split()
import re
ids=[l.split(' | ')[0].rstrip('*') for l in open('settle_000.txt') if re.match(r'^\d+\*? \|',l)]
json.dump({i:("yes" if i in y else "no") for i in ids},open('C/settle_000.json','w'))
print(len(ids))
