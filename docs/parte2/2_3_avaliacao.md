# Pergunta 2.3: o modelo é bom? Como medir?

Notebook: [`notebooks/parte2/2_3_avaliacao.ipynb`](../../notebooks/parte2/2_3_avaliacao.ipynb). Funções reaproveitadas: [`src/avaliacao.py`](../../src/avaliacao.py).

## Pergunta

Use métricas apropriadas (RMSE, MAE, R², etc.) e interprete os resultados.

## Resposta curta

Testei o modelo uma única vez, no fim, nos 100 vídeos guardados desde a Parte 1, que ele nunca tinha visto. Antes de postar, ele erra em média **6,7 pontos** numa nota de 0 a 100. Quem chutasse a nota média erraria 11,7. O modelo explica cerca de dois terços de por que um vídeo tem nota diferente do outro.

Para o time de marketing, as duas frases que importam são estas. **Em 3 de cada 4 vídeos, a previsão fica a até 10 pontos da nota real.** E, entre os 20% melhores vídeos de verdade, o modelo acerta 3 em cada 4 (no chute, acertaria 1 em cada 5). Como o Klike serve para escolher entre criativos, acertar a ordem importa mais do que acertar a nota exata, e é nisso que ele é mais forte.

O modelo que também usa os resultados da campanha erra só 1 ponto a menos (5,7). Ou seja, o vídeo sozinho já explica quase tudo o que a nota mede, uma boa notícia para um produto que avalia antes de postar.

O modelo não "decorou" os dados de treino. Ele erra mais nos vídeos muito bons ou muito ruins, e no LinkedIn. Mais vídeos do mesmo tipo ajudariam pouco.

## O que fiz, passo a passo

**1. Escolhi as métricas.** O enunciado cita três, e usei mais oito, porque cada uma responde a uma pergunta de alguém diferente. O **erro** de um vídeo é a nota real menos a nota prevista.

- **MAE:** o tamanho médio do erro ("em média, erro X pontos"). É a mais fácil de entender.
- **RMSE:** também mede o erro, mas pesa mais os erros grandes. Se ela ficar muito acima do MAE, há alguns erros enormes.
- **R²:** quanto da diferença entre as notas o modelo explica, de 0 (nada) a 1 (tudo).
- **Erro mediano e erro máximo:** o erro típico e o pior caso.
- **Erro em % da nota:** faz sentido aqui, porque a nota nunca chega perto de zero.
- **Quantas previsões ficam a até 5 e a até 10 pontos da nota real:** a mais fácil de explicar ao marketing.
- **O erro que só 10% das previsões ultrapassam:** "em 9 de cada 10 vídeos, erro menos de X".
- **Se a ordem prevista bate com a real:** uma correlação calculada sobre a posição de cada vídeo no ranking.
- **Quantos dos 20% melhores o modelo também coloca entre os 20% melhores.**

**2. Medi tudo primeiro nos dados de treino, mas de forma honesta.** Para cada vídeo, usei a previsão de um modelo que não tinha visto aquele vídeo (a mesma divisão em 5 partes do notebook 2.1).

**3. Procurei sinal de decoreba.** Um modelo que decora erra muito pouco nos dados que viu e muito mais nos novos, como um aluno que decora a lista de exercícios e vai mal na prova. Comparei os dois erros.

**4. Procurei onde o modelo erra.** Olhei três gráficos dos erros e o erro por rede, categoria, formato, objetivo e faixa de nota.

**5. Perguntei se mais dados ajudariam.** Treinei o modelo com quantidades crescentes de vídeos e vi se o erro continuava caindo. Isso é a **curva de aprendizado**.

**6. Conferi se o resultado depende do sorteio,** repetindo a avaliação com cinco sorteios diferentes.

**7. Usei o teste uma única vez**, depois de todas as escolhas estarem feitas.

## Por que fiz assim

**Muitas métricas, porque há muitos públicos.** A banca quer ver as métricas técnicas. O marketing entende "3 em cada 4 vídeos com erro abaixo de 10 pontos". E o produto, que ordena criativos, precisa saber se a ordem está certa.

**O teste só no fim.** Se eu olhasse o teste a cada decisão, acabaria escolhendo o que funciona naqueles 100 vídeos, e a nota final deixaria de ser honesta.

**A conferência de sorteios só com o treino.** Refazer a divisão entre treino e teste misturaria os vídeos guardados com os de estudo.

## O que descobri

Os principais números, no treino (avaliação honesta) e no teste final:

| | Modelo A no treino | **Modelo A no teste** | Modelo B no teste | Chute pela média, no teste |
|---|---|---|---|---|
| erro médio (pontos) | 6,9 | **6,7** | 5,7 | 11,7 |
| explica da variação da nota | 70% | **66%** | 76% | 0% |
| previsões a até 10 pontos | 73% | **74%** | 85% | 48% |
| acerta os 20% melhores | 68% | **75%** | 75% | 20% |

**O teste confirmou a avaliação feita no treino:** 6,7 pontos de erro contra 6,9. No teste, o erro caiu um pouco, mas a parte explicada também caiu (de 70% para 66%). Parece contraditório, mas não é: as notas do teste variam menos entre si, e essa medida compara o erro com o quanto as notas variam.

**O modelo não decorou.** O erro nos vídeos que ele viu é 6,5, contra 6,9 nos que não viu, só 7% maior. Uma decoreba apareceria como uma diferença muito maior.

**Os erros não têm direção.** Em média, o modelo não erra para cima nem para baixo, e o tamanho do erro não muda com a nota prevista.

**O modelo erra mais nos extremos:** 8,2 pontos nos 25% piores vídeos e 7,2 nos 25% melhores, contra cerca de 6 no meio. Ele tende a puxar as previsões para a média. Isso é comum: vídeos muito bons ou muito ruins têm algo que as informações disponíveis não contam (por exemplo, se o gancho é bom ou só existe). Por rede, ele erra mais no LinkedIn (7,9, contra 6,6 no Meta), a rede com menos vídeos.

**Mais vídeos ajudariam pouco.** O erro cai rápido até uns 200 vídeos (de 9,8 para 7,0 pontos) e depois fica quase parado (6,9 com 320). Para errar bem menos, o caminho são informações melhores sobre o vídeo, não mais vídeos do mesmo tipo.

**O resultado não depende do sorteio:** com cinco sorteios diferentes, o erro médio fica entre 6,89 e 7,00 pontos.

## Limites

O teste tem só 100 vídeos, então diferenças pequenas entre o teste e o treino (66% contra 70%) estão dentro do esperado. A avaliação com 15 provas no treino é a medida mais estável, e o teste serve para confirmar que ela não estava otimista. O modelo tende a subestimar os campeões e a superestimar os piores, mas, para ordenar criativos, isso pesa pouco, porque a ordem se mantém. E, com dados reais em vez de simulados, os erros devem ser maiores.
