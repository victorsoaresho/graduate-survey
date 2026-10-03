import pandas as pd, json, itertools
A=pd.read_pickle('cube.pkl'); yrs=list(range(2015,2025))
combos=['BP','BE','LP','LE','TP','TE']
def series(df,col):
    out={}
    for c in combos:
        s=df[(df.g==c[0])&(df.m==c[1])].groupby('ano')[col].sum()
        out[c]=[int(s.get(y,0)) for y in yrs]
    return out
# general totals
gen_tot={'c':series(A,'QT_CONC'),'j':series(A,'QT_CONC_18_24')}
# select courses: union of top 12 across filter combos
sel=set()
grauopts=[['B','L','T'],['B'],['L'],['T']]; modopts=[['P','E'],['P'],['E']]
for col in ['QT_CONC','QT_CONC_18_24']:
  for gs in grauopts:
    for ms in modopts:
      f=A[A.g.isin(gs)&A.m.isin(ms)]
      p=f.groupby(['ano','NO_CINE_ROTULO'])[col].sum()
      for y in yrs: sel|=set(p.loc[y].sort_values(ascending=False).head(12).index)
print(len(sel))
gen={}
for k in sorted(sel):
    f=A[A.NO_CINE_ROTULO==k]
    gen[k]={'c':series(f,'QT_CONC'),'j':series(f,'QT_CONC_18_24')}
    for t in ['c','j']:
        gen[k][t]={c:v for c,v in gen[k][t].items() if any(v)}
T=A[A.tic]
ticc={}
for k in sorted(T.NO_CINE_ROTULO.unique()):
    f=T[T.NO_CINE_ROTULO==k]
    ticc[k]={t:{c:v for c,v in series(f,col).items() if any(v)} for t,col in [('c','QT_CONC'),('j','QT_CONC_18_24'),('i','QT_ING')]}
json.dump({'years':yrs,'genTot':gen_tot,'gen':gen,'tic':ticc},open('page_data.json','w'),ensure_ascii=False,separators=(',',':'))
import os; print(os.path.getsize('page_data.json'))
print(list(ticc.keys()))
