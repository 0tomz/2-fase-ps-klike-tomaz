# Técnicas conhecidas (régua: Projeto_carros, Insper AI)

Levantamento do que aparece no `projeto_carros.ipynb` (e no `referencia_rede_gbm.ipynb`). É a régua da Parte 1: se uma técnica está aqui, eu já usei e sei explicar. Se não está, a Parte 1 não usa (ou explica do zero, quando for só um parâmetro novo de uma função conhecida).

> **Decisões tomadas na auditoria:** além do que está no Projeto_carros, você liberou para a Parte 1: bootstrap com intervalo de 95%, indicador de faltante, Spearman, seaborn (heatmap e boxplot), eta², regressão linear, V de Cramér, heatmap de vazios, experimento de preenchimento (MAE, KNN, Iterative), regra do IQR e z-score. Continuam proibidos: o cálculo automático do número de barras do histograma e os termos técnicos de "mecanismo de faltante".

## Bibliotecas

| Biblioteca | Para quê |
|---|---|
| `pandas` | ler CSV, limpar, agrupar, tabelas |
| `numpy` | contas (`log`, `log1p`, `exp`, `where`, `isinf`, `percentile`) |
| `matplotlib` | todos os gráficos (`plt.subplots`, `hist`, `hexbin`, `barh`, `bar`, `plot`) |
| `scikit-learn` | divisão treino/teste, imputer, one-hot, regressão linear e logística, validação cruzada, métricas |
| `warnings`, `time`, `pathlib`, `io` | utilidades |

**Não aparecem:** `seaborn`, `scipy`, `statsmodels`, `missingno`.

## pandas

- **Leitura e visão geral:** `read_csv(dtype=str, keep_default_na=False)`, `shape`, `head()`, `dtypes`, `isna().mean()`, `nunique()`, `describe(percentiles=[...])`, `value_counts(normalize=True)`.
- **Texto:** `.str.strip()`, `.str.extract(regex)`, `.str.replace`, `.str.endswith`, `.str.removesuffix`, `.str.contains`.
- **Seleção e filtros:** máscaras booleanas, `between(min, max)`, `isin`, `notna`, `loc`, `iloc`, `select_dtypes("number")`.
- **Agrupar:** `groupby(...).agg(nome=("coluna", "função"))`, `groupby().median()`, `groupby().transform("mean")`, `groupby().size()`, `groupby(...)` com `observed=True`.
- **Faixas:** `pd.cut(coluna, limites, labels=[...])` (faixas fixas) e `pd.qcut(coluna, 20)` (faixas com o mesmo número de linhas).
- **Correlação:** `corrwith(alvo)`, `corrwith(alvo, method="spearman")`, `.corr()` (matriz), `np.triu` para listar pares acima da diagonal.
- **Outros:** `quantile(0.999)`, `clip(lower=...)`, `skew()`, `pct_change()`, `nlargest`, `nsmallest`, `concat`, `drop_duplicates`, `map(dicionário)`, `assign`, `sample(random_state=...)`, `round`.
- **Conferências:** `assert` em toda etapa importante ("a limpeza não pode perder linhas", "pct_of_list não volta", "o erro não pode ser bom demais").

## Limpeza

- Ler tudo como texto e converter coluna a coluna com regex; valor fora do padrão vira erro (ou `NaN` com aviso).
- Valores impossíveis viram `NaN` por **faixas fisicamente possíveis** (`anular_fora_da_faixa`: mês 17, ano 1900, comprimento 0, quilometragem acima de 500 mil milhas).
- Corrigir unidade errada com regra (cilindrada em cc acima de 50 dividida por 1000).
- Juntar categorias que são a mesma coisa escrita diferente (mapa de combustível, 13 → 6).
- Remover coluna que contém o alvo (**vazamento**: `pct_of_list`).
- Tabela de decisões "coluna → problema → o que fazemos".
- Separar **erro** (quilometragem de 6,4 milhões: vira `NaN`) de **valor raro mas real** (300 a 500 mil milhas, táxi: fica).

## Divisão treino/teste

- `train_test_split(test_size=0.2, random_state=42, stratify=...)`, com a explicação de semente fixa e de estratificação.
- Conferir que treino e teste não têm linha em comum e têm a mesma proporção (`value_counts(normalize=True)` lado a lado).
- **A EDA olha só o treino.**
- Teste extra "futuro" (anúncios de 2019 em diante) para simular uma composição diferente.

## Faltantes

- `% faltante` por coluna (tabela de visão geral).
- Preencher numéricas com a **mediana** (`SimpleImputer(strategy="median")`, dentro do `Pipeline`) e texto com a categoria **"ausente"** (`SimpleImputer(strategy="constant", fill_value="ausente")`).
- "Os faltantes têm padrão?": comparar a % de faltantes de outras colunas entre o grupo sem câmbio e o grupo com câmbio (os sem câmbio eram "cadastros incompletos").
- Linhas sem o alvo saem só do modelo que precisa daquele alvo.

## Distribuições

- Histograma com **número fixo de bins** (`bins=80`), linha da mediana e da média (`axvline`), corte no percentil 99,9 só no gráfico.
- **Skew** (assimetria) antes e depois do log.
- **Média × mediana** ("68% dos carros custam menos que a média").
- **log** e **log1p** (`log(1 + x)`, para não dar −infinito com zero), com a explicação de que o log transforma diferença em proporção.

## Relações entre variáveis

- **Correlação de Pearson** (−1 a +1; perto de 0 = sem relação *linear*), com a ressalva de que perto de 0 não prova que a coluna é inútil.
- **Spearman** (a mesma ideia, calculada sobre a ordem dos valores; Spearman ≫ Pearson = relação forte mas curva).
- **Multicolinearidade:** listar pares de features com |correlação| > 0,6 e explicar que os pesos ficam instáveis.
- **Hexbin** (nuvem de pontos em hexágonos, cor = quantidade) para relações numéricas com muitas linhas.
- **Mediana por faixa** (`qcut` em 20 faixas) + reta e parábola (`np.polyfit`) + R² de cada uma.
- **Comparar dentro de grupos para tirar o efeito de outra variável:** a inclinação da quilometragem calculada por faixa de idade e "dentro do mesmo modelo de carro" (cada anúncio menos a média do seu `ref_code`). É a ideia de confundimento, sem o nome.
- **eta²:** fração da variação de uma métrica explicada só por saber a categoria (0 = nada, 1 = tudo), para colunas de texto.
- **Redundância entre categóricas:** "% dos anúncios em que a categoria é a mais comum do seu `ref_code`".
- **AUC de uma coluna sozinha** para ver se ela separa automático de manual.
- **Barras horizontais** de mediana por categoria, com o n entre parênteses e o valor escrito na barra (`bar_label`).

## Features

- Criar colunas por conta: idade, milhas por ano, log, termo ao quadrado, interação (produto de duas colunas).
- Cuidar de divisão por zero (`clip(lower=1)`) e conferir que não sobrou infinito.
- Julgar cada feature pela correlação antes/depois, com um **corte de relevância próprio** (ganho > 0,02).

## Modelagem (Partes 2 e 3 do projeto de carros)

- `Pipeline` + `ColumnTransformer`: imputer, `StandardScaler`, `OneHotEncoder(handle_unknown="ignore", min_frequency=...)`.
- `LinearRegression` com alvo em log (`TransformedTargetRegressor`), **peso lido como % "mantendo todo o resto igual"**: `e^w − 1`.
- `LogisticRegression` (sigmoid, regularização como "freio"), `DummyRegressor` / `DummyClassifier` como baseline.
- `KFold`, `StratifiedKFold`, `GroupKFold`, `cross_val_predict`.
- Métricas: MAE, RMSE, erro % mediano, viés % mediano, log-loss, AUC, acurácia, precision, recall, matriz de confusão, calibração por faixa de probabilidade.
- Regra de decisão própria: uma coluna entra se reduzir o MAE em pelo menos 1%.
- Rede neural (`MLPRegressor`) e GBM (`HistGradientBoosting`) só como referência.
- Escopo de validade: situações de risco, faixa de 1% a 99% dos dados conhecidos.

## Jeito de escrever as conclusões

- Markdown curto depois de cada tabela ou gráfico, com títulos como **"Lendo a tabela"**, **"Pelo gráfico"**, **"Comparando..."**.
- Bullets com o número que sustenta cada frase.
- Bloco **"Decisão:"** depois da análise, às vezes em tabela "coluna → decisão → como".
- Linguagem de negócio ("o carro perde uma porcentagem do valor por ano").
- Transparência sobre limites ("isto pode ser otimista porque...").

## Estilo dos gráficos

- Uma cor principal (`AZUL = "#2a78d6"`) e cinza (`"#52514e"`) para referência.
- Função `estilo_limpo(ax)`: tira bordas de cima e da direita, grade clara.
- `plt.tight_layout()` + `plt.show()`. Os gráficos não são salvos em arquivo.

## Decisões da auditoria

| Item | Está no Projeto_carros? | Decisão |
|---|---|---|
| Bootstrap com intervalo de 95% | sim (câmbio, passo 10) | **usar** |
| Indicador de faltante (`add_indicator`) | sim (câmbio, passo 4, teste C) | **usar**, com o nome `<coluna>_faltava` |
| Spearman | sim (EDA, passo 3) | **usar**, ao lado do Pearson |
| seaborn (heatmap, boxplot) | não | **usar** |
| eta² | sim (EDA, passos 6 e 7) | **usar** para colunas com mais de dois níveis |
| Regressão linear | sim (Modelo 1) | **usar**, com `get_dummies` e alvo em pontos |
| V de Cramér | não | **usar** na estrutura (1.1) |
| Heatmap de vazios e de "faltam juntos" | não | **usar** |
| Experimento de preenchimento (MAE, KNN, Iterative) | não | **usar** |
| Regra do IQR e z-score | não | **usar** |
| "Os buracos têm padrão?" | sim (a ideia: sem câmbio × com câmbio) | **usar**, com a régua do acaso (grupos sorteados) |
| Testes estatísticos de comparação de grupos e correção para muitos testes | não | **removidos** (substituídos por medianas + bootstrap + eta²) |
| Cálculo automático do número de barras do histograma | não | **proibido**: 30 barras fixas |
| Termos técnicos de mecanismo de faltante | não | **proibidos** |
| Colunas `ctr_capped` e `roas_applicable` | não | **removidas**: o teto aparece no histograma; Branding é filtrado na hora |
| statsmodels, scipy, missingno | não | **removidos** |
