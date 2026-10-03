import pandas as pd, json, numpy as np
AREAS={'CIÊNCIA DA COMPUTAÇÃO (BACHARELADO)':('Ciência da computação','B'),'SISTEMAS DE INFORMAÇÃO':('Sistemas de informação','B'),
'TECNOLOGIA EM ANÁLISE E DESENVOLVIMENTO DE SISTEMAS':('Análise e desenv. de sistemas','T'),'TECNOLOGIA EM GESTÃO DA TECNOLOGIA DA INFORMAÇÃO':('Gestão da TI','T'),'TECNOLOGIA EM REDES DE COMPUTADORES':('Redes de computadores','T')}
def load(f,sheet=0):
    d=pd.read_excel(f,sheet); d.columns=[str(s).strip().replace('  ',' ') for s in d.columns]
    d['Área de Avaliação']=d['Área de Avaliação'].astype(str).str.strip()
    if 'Grau Acadêmico' in d: d.loc[(d['Área de Avaliação']=='CIÊNCIA DA COMPUTAÇÃO')&(d['Grau Acadêmico'].astype(str).str.contains('Bach')),'Área de Avaliação']='CIÊNCIA DA COMPUTAÇÃO (BACHARELADO)'
    d=d[d['Área de Avaliação'].isin(AREAS)].copy()
    d['area']=d['Área de Avaliação'].str.strip().map(lambda x:AREAS[x][0]); d['grau']=d['Área de Avaliação'].str.strip().map(lambda x:AREAS[x][1])
    d['mod']=np.where(d['Modalidade de Ensino'].str.contains('Dist'),'E','P')
    d['pub']=d['Categoria Administrativa'].astype(str).str.contains('Pública|Publica|Federal|Estadual|Municipal',case=False)
    d['ins']=pd.to_numeric(d['Nº de Concluintes Inscritos'],errors='coerce').fillna(0)
    d['n']=pd.to_numeric(d['Nº de Concluintes Participantes'],errors='coerce').fillna(0)
    for c in ['Nota Bruta - FG','Nota Bruta - CE','Conceito Enade (Contínuo)']: d[c]=pd.to_numeric(d[c],errors='coerce')
    d['geral']=0.25*d['Nota Bruta - FG']+0.75*d['Nota Bruta - CE']
    d['faixa']=d['Conceito Enade (Faixa)'].astype(str).str.strip()
    return d
d21=load('conceito_enade_2021.xlsx','PLANILHA_ENADE'); d17=load('resultados_conceito_enade_2017.xlsx')
print(d21['Categoria Administrativa'].unique())
def summ(d,keys):
    out=[]
    for k,g in d.groupby(keys):
        v=g[g.geral.notna()&(g.n>0)]
        w=v.n.sum()
        cf=g[g.faixa.isin(['1','2','3','4','5'])]
        wc=cf.n.sum()
        out.append(dict(zip(keys if isinstance(keys,list) else [keys],k if isinstance(k,tuple) else (k,)),cursos=len(g),part=int(g.n.sum()),taxa=round(g.n.sum()/g.ins.sum()*100,1),
          geral=round((v.geral*v.n).sum()/w,1) if w else None, ce=round((v['Nota Bruta - CE']*v.n).sum()/w,1) if w else None, fg=round((v['Nota Bruta - FG']*v.n).sum()/w,1) if w else None,
          low=round(cf[cf.faixa.isin(['1','2'])].n.sum()/wc*100,1) if wc else None, high=round(cf[cf.faixa.isin(['4','5'])].n.sum()/wc*100,1) if wc else None,
          cursos_high=round((cf.faixa.isin(['4','5'])).mean()*100,1) if len(cf) else None))
    return pd.DataFrame(out)

pd.set_option('display.width',250); pd.set_option('display.max_columns',20)
for nm,d,k in [('21 area',d21,['area','mod']),('21 grau',d21,['grau','mod']),('21 mod',d21,['mod']),('21 priv area',d21[~d21.pub],['area','mod']),('21 priv grau',d21[~d21.pub],['grau','mod']),('21 mod pub',d21,['mod','pub']),('17 area',d17,['area','mod']),('17 mod',d17,['mod']),('17 priv mod',d17[~d17.pub],['mod'])]:
    print(nm); print(summ(d,k).to_string())
d21.to_pickle('d21.pkl'); d17.to_pickle('d17.pkl')

import json
Q={}
for ed,d in [('2021',d21),('2017',d17)]:
    Q[ed]={}
    for rede,f in [('all',d),('pub',d[d.pub]),('priv',d[~d.pub])]:
        Q[ed][rede]={}
        for by,key in [('area','area'),('grau','grau'),('tot',None)]:
            t=summ(f,[key,'mod'] if key else ['mod'])
            Q[ed][rede][by]=[{k:(None if (isinstance(v,float) and np.isnan(v)) else v) for k,v in r.items()} for r in t.to_dict('records')]
json.dump(Q,open('quality.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(open('quality.json').read()))
