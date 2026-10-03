# Quem se forma no Brasil: dez anos de graduação e a virada da tecnologia

Artigo interativo sobre os concluintes de graduação no Brasil entre 2015 e 2024, com foco nos cursos de tecnologia (área CINE "Computação e TIC") e na qualidade medida pelo Enade.

Site: https://victorsoaresho.github.io/graduate-survey/

Autor: [Victor Soares](https://www.linkedin.com/in/victorsoaresho/) · [GitHub](https://github.com/victorsoaresho)

## Estrutura

- `index.html`: o artigo completo, com textos, estilos, gráficos e dados embutidos em um único arquivo.
- `scripts/baixar_dados.sh`: baixa os microdados do INEP e as planilhas do Enade.
- `scripts/cube.py`: agrega os concluintes por curso, grau, modalidade e ano (2015 a 2024).
- `scripts/mkjson.py`: gera o JSON usado nas figuras 1 a 3.
- `scripts/tic.py`: conferência dos totais da área de TIC.
- `scripts/enade_qualidade.py`: calcula as médias do Enade 2017 e 2021 por curso, modalidade e rede.

## Como reproduzir

```bash
pip install pandas openpyxl
./scripts/baixar_dados.sh
python scripts/cube.py
python scripts/mkjson.py        # gera page_data.json
cd enade && python ../scripts/enade_qualidade.py   # gera quality.json
```

Os JSONs gerados correspondem às constantes `DATA` e `Q` dentro do `index.html`.

## Fontes

1. INEP, Microdados do Censo da Educação Superior: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior
2. INEP, CINE Brasil: https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/cine-brasil
3. INEP, Indicadores de Qualidade da Educação Superior: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/indicadores-de-qualidade-da-educacao-superior
