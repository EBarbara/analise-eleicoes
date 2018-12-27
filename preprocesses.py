import pandas as pd
import numpy as np

tabela_candidato = pd.read_csv('datasets/candidatos.csv', dtype={
    "ano_eleicao": int,
    "codigo_eleicao": float,  # NAN
    "codigo_tipo_eleicao": float,  # NAN
    "data_eleicao": object,
    "descricao_eleicao": object,
    "nome_tipo_eleicao": object,
    "tipo_abrangencia_eleicao": object,
    "codigo_totalizacao_turno": float,  # NAN
    "descricao_totalizacao_turno": object,
    "numero_turno": int,
    "descricao_ue": object,
    "sigla_ue": object,
    "sigla_uf": object,
    "codigo_cor_raca": float,  # NAN
    "codigo_estado_civil": int,
    "codigo_genero": int,
    "codigo_grau_instrucao": int,
    "codigo_municipio_nascimento": int,
    "codigo_nacionalidade": int,
    "codigo_ocupacao": int,
    "cpf": int,
    "data_nascimento": object,
    "descricao_cor_raca": object,
    "descricao_estado_civil": object,
    "descricao_genero": object,
    "descricao_grau_instrucao": object,
    "descricao_nacionalidade": object,
    "descricao_ocupacao": object,
    "email": object,
    "nome": object,
    "nome_municipio_nascimento": object,
    "nome_social": object,
    "sigla_uf_nascimento": object,
    "titulo_eleitoral": float,  # NAN
    "codigo_legenda": float,  # NAN
    "composicao_legenda": object,
    "nome_legenda": object,
    "nome_partido": object,
    "numero_partido": int,
    "sigla_legenda": object,
    "sigla_partido": object,
    "tipo_agremiacao": object,
    "codigo_cargo": int,
    "codigo_detalhe_situacao_candidatura": float,  # NAN
    "codigo_situacao_candidatura": int,
    "concorre_reeleicao": object,
    "declara_bens": object,
    "descricao_cargo": object,
    "descricao_detalhe_situacao_candidatura": object,
    "descricao_situacao_candidatura": object,
    "despesa_maxima_campanha": float,
    "idade_data_eleicao": float,  # NAN
    "idade_data_posse": float,  # NAN
    "nome_urna": object,
    "numero_processo_candidatura": object,
    "numero_protocolo_candidatura": float,  # NAN
    "numero_sequencial": int,
    "numero_urna": float,  # NAN
    "pergunta": object})

df_ordinarias_deferidas = tabela_candidato.loc[
    (tabela_candidato['codigo_tipo_eleicao'] == 2.0) &
    (tabela_candidato['codigo_situacao_candidatura'] == 12) &
    (~tabela_candidato['codigo_cargo'].isin([2, 4, 12])) &
    (tabela_candidato['idade_data_posse'].between(10, 200, inclusive=True)) &
    (tabela_candidato['codigo_totalizacao_turno'] != 6.0)
]
df_work = df_ordinarias_deferidas.drop([
    "ano_eleicao",
    "codigo_eleicao",
    "data_eleicao",
    "descricao_eleicao",
    "tipo_abrangencia_eleicao",
    "codigo_tipo_eleicao",
    "nome_tipo_eleicao",
    "nome",
    "nome_social",
    "nome_urna",
    "numero_urna",
    "email",
    "cpf",
    "titulo_eleitoral",
    "numero_processo_candidatura",
    "numero_protocolo_candidatura",
    "numero_sequencial",
    "pergunta",
    "codigo_detalhe_situacao_candidatura",
    "codigo_situacao_candidatura",
    "descricao_detalhe_situacao_candidatura",
    "descricao_situacao_candidatura",
    "sigla_ue",
    "descricao_ue",
    "sigla_uf",
    "sigla_uf_nascimento",
    "codigo_municipio_nascimento",
    "nome_municipio_nascimento",
    "descricao_grau_instrucao",
    "descricao_nacionalidade",
    "codigo_legenda",
    "nome_legenda",
    "sigla_legenda",
    "idade_data_eleicao",
    "data_nascimento",
    "tipo_agremiacao"
], axis=1)
df_work.rename(columns={
    'codigo_grau_instrucao':'grau_instrucao',
    'codigo_nacionalidade':'nacionalidade',
}, inplace=True)

df_work.loc[df_work['concorre_reeleicao'] == 'N', 'concorre_reeleicao'] = '0'
df_work.loc[df_work['concorre_reeleicao'] == 'S', 'concorre_reeleicao'] = '1'
df_work.loc[df_work['declara_bens'] == 'N', 'declara_bens'] = '0'
df_work.loc[df_work['declara_bens'] == 'S', 'declara_bens'] = '1'
df_work[["concorre_reeleicao", "declara_bens"]] = df_work[["concorre_reeleicao", "declara_bens"]].apply(pd.to_numeric)

df_work.loc[df_work['numero_partido'] == 15, 'nome_partido'] = 'MOVIMENTO DEMOCRATICO BRASILEIRO'
df_work.loc[df_work['numero_partido'] == 15, 'sigla_partido'] = 'MDB'
df_work.loc[df_work['numero_partido'] == 19, 'nome_partido'] = 'PODEMOS'
df_work.loc[df_work['numero_partido'] == 19, 'sigla_partido'] = 'PODE'
df_work.loc[df_work['numero_partido'] == 27, 'nome_partido'] = 'DEMOCRACIA CRISTA'
df_work.loc[df_work['numero_partido'] == 27, 'sigla_partido'] = 'DC'
df_work.loc[df_work['numero_partido'] == 51, 'nome_partido'] = 'PATRIOTA'
df_work.loc[df_work['numero_partido'] == 51, 'sigla_partido'] = 'PATRI'
df_work.loc[df_work['numero_partido'] == 70, 'nome_partido'] = 'AVANTE'
df_work.loc[df_work['numero_partido'] == 70, 'sigla_partido'] = 'AVANTE'
df_work.loc[df_work['numero_partido'] == 77, 'sigla_partido'] = 'SD'

df_work['eleito'] = np.where(df_work['codigo_totalizacao_turno'].between(1.0, 3.0, inclusive=True), 1, 0)
df_work = df_work.drop(["codigo_totalizacao_turno", "descricao_totalizacao_turno", "numero_turno"], axis=1)

df_work = pd.concat([df_work,pd.get_dummies(df_work['descricao_cor_raca'], prefix='cor_raca')],axis=1)
df_work = pd.concat([df_work,pd.get_dummies(df_work['descricao_estado_civil'], prefix='estado_civil')],axis=1)
df_work = pd.concat([df_work,pd.get_dummies(df_work['descricao_genero'], prefix='genero')],axis=1)
df_work = pd.concat([df_work,pd.get_dummies(df_work['descricao_ocupacao'], prefix='ocupacao')],axis=1)
df_work = pd.concat([df_work,pd.get_dummies(df_work['sigla_partido'], prefix='partido')],axis=1)
df_work = pd.concat([df_work,pd.get_dummies(df_work['descricao_cargo'], prefix='cargo')],axis=1)
df_work.drop([
    'codigo_cor_raca', 'descricao_cor_raca',
    'codigo_genero', 'descricao_genero',
    'codigo_ocupacao', 'descricao_ocupacao',
    'codigo_estado_civil','descricao_estado_civil',
    'nome_partido', 'numero_partido', 'sigla_partido',
    'codigo_cargo', 'descricao_cargo'
],axis=1, inplace=True)

df_work.to_csv('datasets/candidatos_work.csv')
