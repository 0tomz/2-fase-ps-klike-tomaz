"""Limpeza do dataset Klike.

Usada pelos notebooks da Parte 1 e, depois, pelas Partes 2 e 3. Cada função resolve um
problema, e o notebook 1_1 mostra cada passo antes de usar estas funções.
"""
import pandas as pd
from sklearn.model_selection import train_test_split

SEMENTE = 42
LIMITE_ERRO = 0.5  # uma conta "não bate" se o valor informado difere mais de 50% do calculado
COLUNAS_PREENCHIDAS = ["video_duration_s", "music_voice_ratio", "avg_watch_time_s", "engagement_rate"]
FAIXAS_DURACAO = [0, 10, 15, 20, 30, float("inf")]
NOMES_FAIXAS_DURACAO = ["até 10s", "10–15s", "15–20s", "20–30s", "30s ou mais"]


def carregar(caminho):
    """Lê o CSV original e transforma a data em data (o resto fica como veio)."""
    dados = pd.read_csv(caminho)
    dados["date"] = pd.to_datetime(dados["date"])
    return dados


def separar_treino_teste(dados):
    """80% treino e 20% teste, com a mesma proporção de cada plataforma nos dois."""
    return train_test_split(dados, test_size=0.2, random_state=SEMENTE, stratify=dados["platform"])


def conta_nao_bate(calculado, informado):
    """True quando o valor informado foge mais de 50% da conta.

    Arredondamento muda poucos por cento; os erros deste dataset são de dezenas a centenas de vezes.
    """
    return (calculado / informado - 1).abs() > LIMITE_ERRO


def corrigir_impressions(dados):
    """Se clicks e ctr concordam e impressions não, o errado é impressions: impressions = clicks / ctr."""
    dados = dados.copy()
    errado = conta_nao_bate(dados["clicks"] / dados["impressions"], dados["ctr"])
    dados.loc[errado, "impressions"] = (dados["clicks"] / dados["ctr"])[errado].round().astype("int64")
    return dados


def corrigir_cpc_ou_spend(dados):
    """Quando cpc não bate com spend / clicks, o roas desempata ("voto da maioria").

    Se revenue / roas dá o spend informado, o spend está certo e o errado é o cpc.
    Senão, o errado é o spend: spend = cpc × clicks, e o roas é recalculado.
    """
    dados = dados.copy()
    cpc_nao_bate = dados["cpc"].notna() & conta_nao_bate(dados["spend"] / dados["clicks"], dados["cpc"])
    spend_confirmado = (dados["roas"] > 0) & ~conta_nao_bate(dados["revenue"] / dados["roas"], dados["spend"])
    erro_no_cpc = cpc_nao_bate & spend_confirmado
    erro_no_spend = cpc_nao_bate & ~spend_confirmado

    dados.loc[erro_no_cpc, "cpc"] = (dados["spend"] / dados["clicks"])[erro_no_cpc].round(2)
    dados.loc[erro_no_spend, "spend"] = (dados["cpc"] * dados["clicks"])[erro_no_spend].round(2)
    dados.loc[erro_no_spend, "roas"] = (dados["revenue"] / dados["spend"])[erro_no_spend].round(2)
    return dados


def calcular_derivadas_faltantes(dados):
    """cpc e revenue vazios são calculados pela definição: cpc = spend / clicks, revenue = roas × spend."""
    dados = dados.copy()
    dados["cpc"] = dados["cpc"].fillna((dados["spend"] / dados["clicks"]).round(2))
    dados["revenue"] = dados["revenue"].fillna((dados["roas"] * dados["spend"]).round(2))
    return dados


def criar_indicadores_faltante(dados):
    """Para cada coluna que vai ser preenchida, uma coluna 0/1: 1 = o valor original estava vazio."""
    dados = dados.copy()
    for coluna in COLUNAS_PREENCHIDAS:
        dados[f"{coluna}_faltava"] = dados[coluna].isna().astype(int)
    return dados


def preencher_faltantes(dados, referencia):
    """Preenche os vazios com valores aprendidos na `referencia` (o treino), nunca no teste.

    - duração, música/voz e engajamento: mediana da plataforma;
    - a duração preenchida nunca fica menor que o tempo assistido daquele vídeo;
    - tempo assistido: duração × fração mediana assistida na plataforma;
    - legenda: "desconhecido" (não sabemos se tem; não é o mesmo que não ter).
    """
    dados = dados.copy()
    for coluna in ["video_duration_s", "music_voice_ratio", "engagement_rate"]:
        mediana_da_plataforma = dados["platform"].map(referencia.groupby("platform")[coluna].median())
        dados[coluna] = dados[coluna].fillna(mediana_da_plataforma)

    menor_que_assistido = dados["video_duration_s"] < dados["avg_watch_time_s"]
    dados.loc[menor_que_assistido, "video_duration_s"] = dados.loc[menor_que_assistido, "avg_watch_time_s"]

    tem_os_dois = referencia["video_duration_s"].notna() & referencia["avg_watch_time_s"].notna()
    fracao_assistida = (referencia["avg_watch_time_s"] / referencia["video_duration_s"])[tem_os_dois]
    fracao_mediana = fracao_assistida.groupby(referencia.loc[tem_os_dois, "platform"]).median()
    estimativa = (dados["video_duration_s"] * dados["platform"].map(fracao_mediana)).round(1)
    dados["avg_watch_time_s"] = dados["avg_watch_time_s"].fillna(estimativa)

    dados["has_subtitle"] = dados["has_subtitle"].map({True: "sim", False: "nao", "True": "sim", "False": "nao"})
    dados["has_subtitle"] = dados["has_subtitle"].fillna("desconhecido")
    return dados


def criar_colunas_novas(dados):
    """Colunas novas que deixam as métricas comparáveis entre vídeos de tamanhos diferentes."""
    dados = dados.copy()
    dados["retencao"] = dados["avg_watch_time_s"] / dados["video_duration_s"]
    dados["taxa_conversao"] = dados["conversions"] / dados["clicks"]
    dados["cpm"] = dados["spend"] / dados["impressions"] * 1000
    dados["cpa"] = dados["spend"] / dados["conversions"].where(dados["conversions"] > 0)  # sem conversão: vazio
    dados["n_boas_praticas"] = (dados["has_hook"].astype(int) + dados["has_cta"].astype(int)
                                + dados["has_face"].astype(int) + (dados["has_subtitle"] == "sim").astype(int))
    dados["faixa_duracao"] = pd.cut(dados["video_duration_s"], FAIXAS_DURACAO, labels=NOMES_FAIXAS_DURACAO)
    dados["mes"] = dados["date"].dt.month
    return dados


def limpar(dados, referencia=None):
    """Todos os passos, na ordem do notebook 1_1. `referencia` = treino (de onde vêm as medianas)."""
    referencia = dados if referencia is None else referencia
    dados = corrigir_impressions(dados)
    dados = corrigir_cpc_ou_spend(dados)
    dados = calcular_derivadas_faltantes(dados)
    dados = criar_indicadores_faltante(dados)
    dados = preencher_faltantes(dados, referencia)
    return criar_colunas_novas(dados)


if __name__ == "__main__":
    bruto = carregar("data/raw/klike_challenge_dataset.csv")
    treino, teste = separar_treino_teste(bruto)
    limpo = limpar(treino)
    assert len(limpo) == len(treino), "a limpeza não pode perder linhas"
    assert limpo[COLUNAS_PREENCHIDAS + ["cpc", "revenue"]].notna().all().all(), "sobrou vazio"
    assert not conta_nao_bate(limpo["clicks"] / limpo["impressions"], limpo["ctr"]).any()
    assert not conta_nao_bate(limpo["spend"] / limpo["clicks"], limpo["cpc"]).any()
    assert (limpo["avg_watch_time_s"] <= limpo["video_duration_s"]).all()
    assert (limpo["cpa"].dropna() < float("inf")).all(), "CPA infinito (divisão por zero conversões)"
    assert limpar(teste, referencia=treino)[COLUNAS_PREENCHIDAS].notna().all().all()
    print("limpeza ok")
