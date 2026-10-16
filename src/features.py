"""Features da Parte 2 (modelagem do klike_score).

O notebook 2_1 mostra cada passo por extenso antes de usar estas funções; os notebooks
2_2 a 2_4 (e a Parte 3) só as reaproveitam.
"""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

from src.limpeza import COLUNAS_PREENCHIDAS, carregar, limpar, separar_treino_teste

ALVO = "klike_score"

# Modelo A, "pré-lançamento": só o que se sabe antes de postar
SIM_NAO = ["has_hook", "has_face", "has_cta", "is_retargeting"]
NUMERICAS = ["video_duration_s", "music_voice_ratio"]
# Coluna de texto: seus níveis. O primeiro é a referência (fica de fora do one-hot).
CATEGORIAS = {
    "has_subtitle": ["nao", "sim", "desconhecido"],
    "format": ["quadrado", "vertical", "horizontal"],          # quadrado: o único presente nas 3 redes
    "text_density": ["medium", "low", "high"],                 # médio: o melhor nível na Parte 1
    "platform": ["Meta", "TikTok", "LinkedIn"],                # nas outras, a referência é o nível mais comum
    "category": ["E-commerce", "Lead Gen", "SaaS", "App Install", "Branding"],
    "objective": ["conversions", "traffic", "engagement", "awareness", "app_install"],
    "target_audience_age": ["25-34", "18-24", "35-44", "45+"],
}

# Modelo B, "completo": o A + métricas que só existem depois que o anúncio roda
POS_LANCAMENTO = ["ctr", "engagement_rate", "retencao", "taxa_conversao", "cpm", "log_conversoes"]

# Conjuntos finais, escolhidos no notebook 2_1 (category sai: repete objective)
CATEGORIAS_A = [c for c in CATEGORIAS if c != "category"]
NOVAS_A = ["musica_x_tiktok"]
COLUNAS_A = SIM_NAO + NUMERICAS + CATEGORIAS_A
COLUNAS_B = COLUNAS_A + POS_LANCAMENTO
NUMERICAS_B = NUMERICAS + POS_LANCAMENTO


def carregar_treino_teste(caminho):
    """Mesma divisão e mesma limpeza da Parte 1; os valores que a limpeza preencheu voltam a vazio.

    Quem preenche agora é o Pipeline, só com o treino de cada rodada da validação cruzada.
    """
    treino, teste = separar_treino_teste(carregar(caminho))
    return voltar_vazios(limpar(treino)), voltar_vazios(limpar(teste, referencia=treino))


def voltar_vazios(dados):
    """Desfaz o preenchimento da Parte 1 (o indicador `_faltava` diz quais eram vazios)."""
    dados = dados.copy()
    for coluna in COLUNAS_PREENCHIDAS:
        dados.loc[dados[f"{coluna}_faltava"] == 1, coluna] = np.nan
    dados["retencao"] = dados["avg_watch_time_s"] / dados["video_duration_s"]  # vazia se um dos dois era vazio
    dados["log_conversoes"] = np.log1p(dados["conversions"])  # conversões têm cauda longa
    dados[SIM_NAO] = dados[SIM_NAO].astype(int)
    return dados


# Colunas novas que podem ser testadas. Cada uma é calculada depois do preenchimento dos vazios.
COLUNAS_NOVAS = {
    "n_boas_praticas": lambda X: X["has_hook"] + X["has_face"] + X["has_cta"] + (X["has_subtitle"] == "sim"),
    "musica_x_tiktok": lambda X: X["music_voice_ratio"] * (X["platform"] == "TikTok"),
    "gancho_x_tiktok": lambda X: X["has_hook"] * (X["platform"] == "TikTok"),
    "gancho_x_linkedin": lambda X: X["has_hook"] * (X["platform"] == "LinkedIn"),
    "duracao_ao_quadrado": lambda X: X["video_duration_s"] ** 2,
    "musica_ao_quadrado": lambda X: X["music_voice_ratio"] ** 2,
    "texto_em_ordem": lambda X: X["text_density"].map({"low": 0, "medium": 1, "high": 2}),
    "duracao_ate_10s": lambda X: X["video_duration_s"] <= 10,
    "duracao_10_a_20s": lambda X: X["video_duration_s"].between(10, 20, inclusive="right"),
    "duracao_mais_de_30s": lambda X: X["video_duration_s"] > 30,
}


def criar_colunas_novas(X, novas):
    """Acrescenta as colunas novas pedidas; "texto_em_ordem" substitui o texto como categoria."""
    X = X.copy()
    for nome in novas:
        X[nome] = COLUNAS_NOVAS[nome](X).astype(float)
    if "texto_em_ordem" in novas:
        X = X.drop(columns="text_density")
    return X


def montar_pipeline(modelo, numericas, categorias, novas=()):
    """Preencher vazios → colunas novas → one-hot → padronizar → modelo, tudo aprendido só no treino."""
    preencher = ColumnTransformer(
        [("numericas", SimpleImputer(strategy="median", add_indicator=True), numericas)],
        remainder="passthrough", verbose_feature_names_out=False)
    if "texto_em_ordem" in novas:
        categorias = [c for c in categorias if c != "text_density"]
    codificar = ColumnTransformer(
        [("categorias", OneHotEncoder(categories=[CATEGORIAS[c] for c in categorias], drop="first",
                                      sparse_output=False), categorias)],
        remainder="passthrough", verbose_feature_names_out=False)
    return Pipeline([
        ("preencher", preencher),
        ("colunas_novas", FunctionTransformer(criar_colunas_novas, kw_args={"novas": list(novas)})),
        ("codificar", codificar),
        ("padronizar", StandardScaler()),
        ("modelo", modelo),
    ]).set_output(transform="pandas")


def efeitos_em_pontos(pipeline, X):
    """Peso de cada coluna em pontos de nota (desfaz a padronização: peso ÷ desvio da coluna)."""
    colunas = pipeline[:-1].transform(X.head()).columns
    return pd.Series(pipeline[-1].coef_ / pipeline["padronizar"].scale_, index=colunas)


if __name__ == "__main__":
    from sklearn.linear_model import LinearRegression

    treino, teste = carregar_treino_teste("data/raw/klike_challenge_dataset.csv")
    assert (len(treino), len(teste)) == (400, 100)
    assert treino["video_duration_s"].isna().any(), "os vazios deveriam ter voltado"
    colunas = SIM_NAO + NUMERICAS + list(CATEGORIAS)
    modelo = montar_pipeline(LinearRegression(), NUMERICAS, list(CATEGORIAS), ["musica_x_tiktok"]).fit(treino[colunas], treino[ALVO])
    previsto = modelo.predict(teste[colunas])
    assert previsto.shape == (100,) and not np.isnan(previsto).any()
    assert "musica_x_tiktok" in efeitos_em_pontos(modelo, treino[colunas]).index
    print("features ok")
