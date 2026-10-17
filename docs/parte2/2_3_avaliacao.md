# 2.3 O modelo é bom? Como medir?

> Pergunta do case: use métricas apropriadas (RMSE, MAE, R², etc.) e interprete os resultados.
>
> Notebook: [`2_3_avaliacao.ipynb`](../../notebooks/parte2/2_3_avaliacao.ipynb) · Código: [`src/avaliacao.py`](../../src/avaliacao.py)

## Resposta curta

Testei o modelo uma única vez, no fim, nos 100 vídeos guardados desde a Parte 1, que ele nunca tinha visto. Antes de postar, ele erra em média **6,7 pontos** numa nota de 0 a 100; quem chutasse a nota média erraria 11,7. Ele explica cerca de dois terços de por que um vídeo tem nota diferente do outro. Em 3 de cada 4 vídeos, a previsão fica a até 10 pontos da nota real. O modelo que também vê os resultados da campanha erra só 1 ponto a menos (5,7).

## Por que isso importa

O modelo serve para **comparar e ordenar criativos**, mais do que para cravar a nota exata de um vídeo. A ordem que ele dá acompanha bem a ordem real. Entre os 20 melhores vídeos do teste, ele colocou 15 também entre os 20 melhores (no chute, acertaria 4). Mas 20 vídeos é pouco para um número preciso: na avaliação com o treino, feita com 80 vídeos, o acerto foi de 68%. A leitura honesta é "acha a maioria dos melhores", e não "acha exatamente 3 em cada 4".

## Como cheguei lá

**Escolhi métricas para públicos diferentes.** O enunciado cita três, e usei mais oito, num total de 11. O **erro** de um vídeo é a nota real menos a prevista.

- **MAE:** o erro médio ("em média, erra X pontos"), a mais fácil de entender.
- **RMSE:** também mede o erro, mas pesa mais os erros grandes.
- **R²:** quanto da diferença entre as notas o modelo explica, de 0 (nada) a 1 (tudo).
- **As outras oito:**
  - o R² ajustado;
  - o erro mediano e o erro máximo;
  - o erro em % da nota;
  - quantas previsões ficam a até 5 e a até 10 pontos;
  - o erro que só 10% das previsões passam;
  - se a ordem prevista bate com a real;
  - quantos dos melhores vídeos o modelo também põe entre os melhores.

A banca quer o RMSE e o R²; o marketing entende "3 em cada 4 com erro abaixo de 10 pontos"; e o Klike, que serve para escolher entre vídeos, precisa saber se a ordem está certa.

**Usei o teste só no fim.** Se eu olhasse os 100 vídeos guardados a cada decisão, acabaria escolhendo o que funciona neles, e a nota final deixaria de ser honesta. Antes disso, medi tudo com a validação cruzada (os 15 simulados do 2.1).

**Procurei sinal de decoreba.** Um modelo que decora erra pouco nos vídeos que viu e muito nos novos, como um aluno que decora a lista de exercícios e vai mal na prova. Aqui, ele erra 6,5 pontos nos vídeos que viu e 6,9 nos que não viu, só 7% a mais: não decorou.

**Procurei onde ele erra.** Os erros não têm direção: em média, ele não erra para cima nem para baixo. Mas erra mais nos extremos (8,2 pontos nos 25% piores vídeos e 7,2 nos 25% melhores, contra cerca de 6 no meio), porque tende a puxar as previsões para a média. Isso é esperado: vídeos muito bons ou muito ruins têm algo que as informações disponíveis não contam, como se o gancho é bom ou só existe. Por rede, erra mais no LinkedIn (7,9, contra 6,6 no Meta), a rede com menos vídeos.

**Perguntei se mais vídeos ajudariam.** O erro cai rápido até uns 200 vídeos e depois quase para (6,9 com 320). Para errar menos, o caminho é ter informações melhores sobre cada vídeo, não mais vídeos do mesmo tipo.

**Conferi se o resultado depende do sorteio.** Com cinco sorteios diferentes, o erro médio ficou entre 6,9 e 7,0. No teste, o erro caiu um pouco em relação ao treino (de 6,9 para 6,7), mas o R² também caiu (de 0,70 para 0,66). Não é contradição: as notas do teste variam menos entre si, e o R² mede o erro em relação a quanto as notas variam.

| | Treino (validação) | **Teste** | Chute pela média (teste) |
|---|---|---|---|
| erro médio (pontos) | 6,9 | **6,7** | 11,7 |
| explica da variação da nota | 70% | **66%** | 0% |
| previsões a até 10 pontos | 73% | **74%** | 48% |

## Limites

O teste tem só 100 vídeos, então diferenças pequenas entre o teste e o treino estão dentro do esperado; a validação com 15 provas é a medida mais estável. O modelo tende a subestimar os campeões e a superestimar os piores, mas, para ordenar criativos, isso pesa pouco. E, com dados reais em vez de simulados, os erros devem ser maiores.
