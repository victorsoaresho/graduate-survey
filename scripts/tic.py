import pandas as pd
rows=[]
for y in range(2015,2025):
    df=pd.read_csv(f"csv/MICRODADOS_CADASTRO_CURSOS_{y}.CSV",sep=';',encoding='latin1',
      usecols=['TP_NIVEL_ACADEMICO','CO_CINE_AREA_GERAL','NO_CINE_AREA_GERAL','NO_CINE_ROTULO','TP_GRAU_ACADEMICO','TP_MODALIDADE_ENSINO','QT_CONC','QT_CONC_18_24','QT_MAT','QT_ING'],low_memory=False)
    g=df[(df.TP_NIVEL_ACADEMICO==1)&(df.CO_CINE_AREA_GERAL.astype(str).str.lstrip('0')=='6')].copy()
    g['ano']=y; rows.append(g)
    if y in (2015,2024): print(y, g.NO_CINE_AREA_GERAL.unique()[:2], g.TP_GRAU_ACADEMICO.value_counts().to_dict())
a=pd.concat(rows)
a.to_pickle('tic.pkl')
print(a.groupby('ano')[['QT_CONC','QT_ING','QT_MAT']].sum())
print(a.groupby(['ano','TP_GRAU_ACADEMICO','TP_MODALIDADE_ENSINO']).QT_CONC.sum().unstack([1,2]))
