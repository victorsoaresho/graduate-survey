#!/bin/bash
# Baixa os microdados do Censo da Educação Superior (INEP) e as planilhas do Enade.
# Os arquivos são grandes (até ~450 MB por ano). Use http se o https do INEP falhar.
set -e
mkdir -p dados/zip csv enade
for y in $(seq 2015 2024); do
  curl -L -C - -o dados/zip/censo_$y.zip "http://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_$y.zip"
  unzip -j -o -q dados/zip/censo_$y.zip "*CADASTRO_CURSOS*" -d csv/
done
cd enade
curl -L -O "http://download.inep.gov.br/educacao_superior/indicadores/resultados/2021/conceito_enade_2021.xlsx"
curl -L -O "http://download.inep.gov.br/educacao_superior/indicadores/resultados/2021/IDD_2021.xlsx"
curl -L -O "http://download.inep.gov.br/educacao_superior/indicadores/legislacao/2018/resultados_conceito_enade_2017.xlsx"
