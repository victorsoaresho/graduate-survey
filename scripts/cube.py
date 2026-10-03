import pandas as pd, json, itertools
yrs=list(range(2015,2025)); parts=[]
for y in yrs:
    df=pd.read_csv(f"csv/MICRODADOS_CADASTRO_CURSOS_{y}.CSV",sep=';',encoding='latin1',
      usecols=['TP_NIVEL_ACADEMICO','CO_CINE_AREA_GERAL','NO_CINE_ROTULO','TP_GRAU_ACADEMICO','TP_MODALIDADE_ENSINO','QT_CONC','QT_CONC_18_24','QT_ING'],low_memory=False)
    df=df[df.TP_NIVEL_ACADEMICO==1].copy()
    df['g']=df.TP_GRAU_ACADEMICO.map({1:'B',2:'L',3:'T',4:'B'}).fillna('B')
    df['m']=df.TP_MODALIDADE_ENSINO.map({1:'P',2:'E'})
    df['tic']=df.CO_CINE_AREA_GERAL.astype(str).str.lstrip('0').str.split('.').str[0]=='6'
    a=df.groupby(['NO_CINE_ROTULO','tic','g','m'])[['QT_CONC','QT_CONC_18_24','QT_ING']].sum().reset_index(); a['ano']=y; parts.append(a)
A=pd.concat(parts); A.to_pickle('cube.pkl')
print(A.groupby('ano').QT_CONC.sum().tolist())
