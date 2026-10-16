"""Avaliação dos modelos da Parte 2.

O notebook 2_2 mostra a validação cruzada por extenso e o 2_3 mostra cada métrica antes de usar
estas funções.
"""
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate

SEMENTE = 42


def dobras(X, repeticoes=3, semente=SEMENTE):
    """5 dobras × 3 repetições, cada dobra com a mesma proporção de plataformas.

    Os mesmos 15 cortes servem para todos os modelos: a comparação fica justa (todos fazem a mesma prova).
    """
    cortes = RepeatedStratifiedKFold(n_splits=5, n_repeats=repeticoes, random_state=semente)
    return list(cortes.split(X, X["platform"]))


def validar(pipeline, X, y, cortes):
    """MAE, RMSE e R² em cada um dos cortes (sempre medidos na parte que o modelo não viu)."""
    resultado = cross_validate(pipeline, X, y, cv=cortes,
                               scoring={"MAE": "neg_mean_absolute_error", "RMSE": "neg_root_mean_squared_error",
                                        "R²": "r2"})
    return pd.DataFrame({"MAE": -resultado["test_MAE"], "RMSE": -resultado["test_RMSE"], "R²": resultado["test_R²"]})


def resumir(por_corte):
    """Média ± desvio de cada métrica entre os cortes."""
    return {f"{metrica}": f"{por_corte[metrica].mean():.2f} ± {por_corte[metrica].std():.2f}" for metrica in por_corte}


def metricas(real, previsto, n_colunas=None):
    """Todas as métricas do notebook 2_3 para um conjunto de previsões."""
    real, previsto = np.asarray(real), np.clip(np.asarray(previsto), 0, 100)  # a nota vai de 0 a 100
    erro = np.abs(real - previsto)
    n = len(real)
    r2 = r2_score(real, previsto)
    top_real = real >= np.quantile(real, 0.8)
    # os k criativos com maior previsão (empates, como num chute constante, não viram "todos no top")
    top_previsto = np.zeros(n, dtype=bool)
    top_previsto[np.argsort(-previsto, kind="stable")[:top_real.sum()]] = True
    constante = np.ptp(previsto) == 0
    resultado = {
        "MAE": mean_absolute_error(real, previsto),
        "RMSE": np.sqrt(mean_squared_error(real, previsto)),
        "R²": r2,
        "erro mediano": np.median(erro),
        "erro máximo": erro.max(),
        "MAPE (%)": np.mean(erro / real) * 100,
        "% dentro de ±5 pts": np.mean(erro <= 5) * 100,
        "% dentro de ±10 pts": np.mean(erro <= 10) * 100,
        "90% dos erros abaixo de": np.quantile(erro, 0.9),
        "Spearman": np.nan if constante else pd.Series(real).corr(pd.Series(previsto), method="spearman"),
        "acerto do top 20% (%)": (top_real & top_previsto).sum() / top_real.sum() * 100,
    }
    if n_colunas is not None:  # só faz sentido nos dados que o modelo viu (o treino)
        resultado["R² ajustado"] = 1 - (1 - r2) * (n - 1) / (n - n_colunas - 1)
    return resultado


if __name__ == "__main__":
    real = np.array([10, 50, 60, 90, 100])
    perfeito = metricas(real, real, n_colunas=1)
    assert perfeito["MAE"] == 0 and perfeito["R²"] == 1 and perfeito["% dentro de ±5 pts"] == 100
    assert metricas(real, real + 20)["MAE"] == 14  # 90 + 20 e 100 + 20 são cortados em 100
    assert metricas(real, np.full(5, 60.0))["acerto do top 20% (%)"] == 0  # chute constante não acha o top
    print("avaliacao ok")
