"""Motor de recomendações da Parte 3.

Recebe uma campanha (uma linha do dataset original) e devolve as mudanças no criativo que mais
sobem a nota, em ordem de impacto. O notebook 3_motor_de_recomendacoes mostra cada passo por extenso.

Uso pela linha de comando:  python -m src.recomendacoes KLK-0123
"""
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from src.features import COLUNAS_A, voltar_vazios
from src.limpeza import carregar, limpar, separar_treino_teste

RAIZ = Path(__file__).resolve().parents[1]
GANHO_MINIMO = 1.0  # pontos de nota; abaixo disso, a mudança aparece marcada como "ganho pequeno"
MINIMO_CRIATIVOS = 15  # a mesma regra das Partes 1 e 2: grupos menores não sustentam conclusão
VOZ_ALVO = 0.3  # música/voz sugerida quando há música demais (0 = só voz, 1 = só música)
# Métrica que cada objetivo quer mover (Parte 1, pergunta 1.2, passo 9). Conversão: o criativo não mexe
# no custo por conversão, então o efeito mostrado é no clique, a etapa anterior.
METRICA_DO_OBJETIVO = {"awareness": "Retenção", "engagement": "Engajamento", "traffic": "CTR",
                       "conversions": "CTR", "app_install": "CTR"}
NOMES_TEXTO = {"low": "pouco", "medium": "médio", "high": "muito"}
ARTIGO = {"CTR": "o CTR", "Engajamento": "o engajamento", "Retenção": "a retenção"}


def carregar_motor():
    """Tudo o que o motor usa, aprendido só com o treino: modelo da Parte 2 e efeitos da Parte 1."""
    treino_bruto, _ = separar_treino_teste(carregar(RAIZ / "data/raw/klike_challenge_dataset.csv"))
    treino = limpar(treino_bruto)
    contagem_formatos = pd.crosstab(treino["platform"], treino["format"])
    return {
        "treino_bruto": treino_bruto,
        "modelo": joblib.load(RAIZ / "models/modelo_A.joblib"),
        "efeitos": pd.read_csv(RAIZ / "data/processed/efeitos_por_plataforma.csv"),
        # só sugiro um formato que a rede já usa com pelo menos 15 criativos
        "formatos_da_rede": {rede: list(linha.index[linha >= MINIMO_CRIATIVOS]) for rede, linha in contagem_formatos.iterrows()},
    }


def preparar(linha_bruta, motor):
    """A mesma limpeza das Partes 1 e 2 para uma linha do dataset original."""
    return voltar_vazios(limpar(pd.DataFrame([linha_bruta]), referencia=motor["treino_bruto"])).iloc[0]


def mudancas_possiveis(campanha, motor):
    """Cada mudança: (o que fazer, colunas alteradas, atributo na tabela da Parte 1, direção)."""
    mudancas = []
    if not campanha["has_hook"]:
        mudancas.append(("Adicionar um gancho nos 3 primeiros segundos", {"has_hook": 1}, "Gancho (hook)", "adicionar"))
    if not campanha["has_face"]:
        mudancas.append(("Mostrar um rosto humano no vídeo", {"has_face": 1}, "Rosto", "adicionar"))
    if not campanha["has_cta"]:
        mudancas.append(("Terminar com uma chamada para ação (CTA)", {"has_cta": 1}, "CTA", "adicionar"))
    if campanha["has_subtitle"] != "sim":
        mudancas.append(("Colocar legenda", {"has_subtitle": "sim"}, "Legenda", "adicionar"))
    if campanha["text_density"] != "medium":
        atributo = "Muito texto" if campanha["text_density"] == "high" else None
        mudancas.append((f"Mudar o texto na tela de '{NOMES_TEXTO[campanha['text_density']]}' para 'médio'",
                         {"text_density": "medium"}, atributo, "tirar"))
    # Música só pesa no TikTok (Parte 2): lá, qualquer excesso de música sobre o alvo custa pontos
    if campanha["music_voice_ratio"] > (VOZ_ALVO if campanha["platform"] == "TikTok" else 0.5):
        mudancas.append((f"Trocar parte da música por voz (música/voz de {campanha['music_voice_ratio']:.1f} para {VOZ_ALVO})",
                         {"music_voice_ratio": VOZ_ALVO}, "Mais música que voz", "tirar"))
    if not campanha["is_retargeting"]:  # decisão de público, não de vídeo, mas está nas mãos do time
        mudancas.append(("Rodar o criativo também para quem já conhece a marca (retargeting)", {"is_retargeting": 1}, None, None))
    for formato in motor["formatos_da_rede"][campanha["platform"]]:
        if formato != campanha["format"]:
            mudancas.append((f"Mudar o formato de {campanha['format']} para {formato}", {"format": formato}, None, None))
    return mudancas


def efeito_na_metrica(campanha, atributo, direcao, motor):
    """Efeito observado na Parte 1 (diferença das medianas) na métrica do objetivo, na rede da campanha.

    Só aparece se for confiável (intervalo de 95% de um lado do zero) e com 15 criativos ou mais em cada grupo:
    um "indício" pode até ter o sinal oposto ao da nota, e confundiria quem lê.
    """
    metrica = METRICA_DO_OBJETIVO[campanha["objective"]]
    efeitos = motor["efeitos"]
    linha = efeitos[(efeitos["plataforma"] == campanha["platform"]) & (efeitos["atributo"] == str(atributo))
                    & (efeitos["metrica"] == metrica)]
    if linha.empty or min(linha["n_com"].iloc[0], linha["n_sem"].iloc[0]) < MINIMO_CRIATIVOS or not linha["confiavel"].iloc[0]:
        return None
    linha = linha.iloc[0]
    # "adicionar": mediana com ÷ sem − 1; "tirar": o caminho inverso, sem ÷ com − 1
    variacao = linha["diferenca_pct"] if direcao == "adicionar" else (linha["mediana_sem"] / linha["mediana_com"] - 1) * 100
    return metrica, variacao


def boas_praticas_presentes(campanha):
    """O que o criativo já faz bem: (o que manter, o que seria perder isso, como ficaria sem isso)."""
    presentes = [("o gancho nos 3 primeiros segundos", "tirá-lo", {"has_hook": 0}, campanha["has_hook"]),
                 ("o rosto humano", "tirá-lo", {"has_face": 0}, campanha["has_face"]),
                 ("a chamada para ação (CTA)", "tirá-la", {"has_cta": 0}, campanha["has_cta"]),
                 ("a legenda", "tirá-la", {"has_subtitle": "nao"}, campanha["has_subtitle"] == "sim"),
                 ("o texto na tela em nível médio", "passar para 'muito'", {"text_density": "high"},
                  campanha["text_density"] == "medium")]
    return [(nome, perder, colunas) for nome, perder, colunas, tem in presentes if tem]


def recomendar(linha_bruta, motor, quantas=3):
    """As `quantas` recomendações de maior impacto na nota prevista, em ordem.

    Primeiro as melhorias. Se o criativo já segue quase tudo e sobram menos de `quantas`, completa com
    o que ele deve manter (quanto perderia se tirasse), para nunca inventar uma melhoria sem base.
    """
    campanha = preparar(linha_bruta, motor)
    prever = lambda c: float(np.clip(motor["modelo"].predict(pd.DataFrame([c])[COLUNAS_A])[0], 0, 100))

    def com(colunas):
        alterada = campanha.copy()
        alterada.update(pd.Series(colunas))  # o mesmo criativo, só com a mudança
        return prever(alterada)

    nota_hoje = prever(campanha)
    melhorias = []
    for acao, colunas, atributo, direcao in mudancas_possiveis(campanha, motor):
        nota_depois = com(colunas)
        ganho = nota_depois - nota_hoje
        if ganho <= 0:
            continue
        texto = f"{acao} pode aumentar a nota Klike em ~{ganho:.0f} pontos (de {nota_hoje:.0f} para {nota_depois:.0f})"
        efeito = efeito_na_metrica(campanha, atributo, direcao, motor) if atributo else None
        if efeito:
            metrica, variacao = efeito
            texto += f" e {ARTIGO[metrica]} em ~{variacao:+.0f}% no {campanha['platform']}"
        texto += ", com base nos padrões do dataset."
        if ganho < GANHO_MINIMO:
            texto += " Ganho pequeno: só vale se a mudança for barata."
        melhorias.append({"tipo": "melhorar", "recomendação": texto, "impacto na nota": ganho})
    melhorias = sorted(melhorias, key=lambda r: -r["impacto na nota"])[:quantas]

    manter = []
    for nome, perder, colunas in boas_praticas_presentes(campanha):
        perda = nota_hoje - com(colunas)
        manter.append({"tipo": "manter", "impacto na nota": perda,
                       "recomendação": f"Manter {nome}: {perder} custaria ~{perda:.0f} pontos de nota (de {nota_hoje:.0f} para {nota_hoje - perda:.0f})."})
    manter = sorted(manter, key=lambda r: -r["impacto na nota"])[:quantas - len(melhorias)]

    resultado = pd.DataFrame(melhorias + manter, columns=["tipo", "recomendação", "impacto na nota"])
    resultado.index = pd.RangeIndex(1, len(resultado) + 1, name="prioridade")
    return resultado


if __name__ == "__main__":
    motor = carregar_motor()
    bruto = carregar(RAIZ / "data/raw/klike_challenge_dataset.csv")
    if len(sys.argv) > 1:
        linha = bruto.loc[bruto["campaign_id"] == sys.argv[1]]
        if linha.empty:
            sys.exit(f"Campanha {sys.argv[1]} não encontrada.")
        linha = linha.iloc[0]
        print(f"{linha['campaign_id']} | {linha['platform']} | {linha['category']} | {linha['objective']}")
        for prioridade, texto in recomendar(linha, motor)["recomendação"].items():
            print(f"{prioridade}. {texto}")
    else:  # autoconferência
        sem_nada = bruto.iloc[0].copy()
        sem_nada[["has_hook", "has_face", "has_cta", "has_subtitle"]] = False
        sem_nada["text_density"] = "high"
        recomendacoes = recomendar(sem_nada, motor)
        assert len(recomendacoes) == 3 and recomendacoes["impacto na nota"].is_monotonic_decreasing
        assert recomendacoes["recomendação"].iloc[0].startswith("Adicionar um gancho")
        perfeita = bruto.iloc[0].copy()
        perfeita[["has_hook", "has_face", "has_cta", "has_subtitle", "is_retargeting"]] = True
        assert (recomendar(perfeita, motor)["tipo"] == "manter").sum() >= 1  # já segue tudo: completa com "manter"
        print("recomendacoes ok")
