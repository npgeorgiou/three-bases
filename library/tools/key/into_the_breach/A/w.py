import json,sys
def save(name,d):
    json.dump(d,open('/home/claude/three-bases/library/tools/key/into_the_breach/A/%s.json'%name,'w'),ensure_ascii=False,indent=0)
    open('/home/claude/three-bases/library/tools/key/into_the_breach/A/progress.txt','a').write('done %s\n'%name)
