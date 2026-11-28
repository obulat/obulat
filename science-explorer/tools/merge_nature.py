#!/usr/bin/env python3
"""Merge nature_*.js data files (const NAT_n={...}) into app.html between /*NATURE*/ markers."""
import sys,re,glob,os
app=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'app.html')
parts=[]
for f in sorted(sys.argv[1:]):
    t=open(f,encoding='utf8').read().strip()
    body=t[t.index('{')+1:t.rindex('}')].strip().rstrip(',')
    parts.append(body)
s=open(app,encoding='utf8').read()
a=s.index('/*NATURE*/');b=s.index('/*NATURE-END*/')
s=s[:a]+'/*NATURE*/\nconst NAT={\n'+',\n'.join(parts)+'\n};\n'+s[b:]
open(app,'w',encoding='utf8').write(s)
print('merged',len(parts),'files')
