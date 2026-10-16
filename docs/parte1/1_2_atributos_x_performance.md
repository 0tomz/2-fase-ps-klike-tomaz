# Pergunta 1.2: quais atributos do criativo se associam a boa performance?

Notebook: [`notebooks/parte1/1_2_atributos_x_performance.ipynb`](../../notebooks/parte1/1_2_atributos_x_performance.ipynb). Termos em [`docs/glossario.md`](../glossario.md).

## Pergunta

Quais atributos do criativo mais se correlacionam com boas métricas de performance (CTR, ROAS, conversões etc.)?

O "etc." importa: analisei **nove métricas**, do começo ao fim do funil. São elas: CTR, engajamento, retenção, taxa de conversão, conversões, ROAS, CPC, CPA e a nota `klike_score`, que é o alvo da Parte 2.

## Resposta curta

**Na nota, mantendo o resto igual (regressão):**

- **Gancho nos 3 primeiros segundos é o atributo mais forte:** +17,5 pontos (intervalo de 15,7 a 19,1). Funciona em todas as plataformas e objetivos.
- **Rosto humano é o segundo:** +11,8 pontos.
- **Legenda (+7,9) e CTA (+7,2)** também somam.
- **Texto na tela tem um ponto ótimo no meio:** muito texto tira 15,1 pontos; pouco texto tira 8,0.
- **Formato, duração e música/voz** não mudam a nota de forma clara.

**Em cada etapa do funil (mantendo o resto igual):**

| Atributo | Ver e interagir (CTR, engajamento, retenção) | Converter e vender (conversão, ROAS, CPC, CPA) |
|---|---|---|
| Gancho | **sobe tudo:** CTR +53%, engajamento +53%, retenção +41% | nada |
| Rosto | engajamento +41% | CPA −13% (indício) |
| Muito texto | **derruba:** CTR −25%, retenção −24% | **derruba:** taxa de conversão −14%, ROAS −20% |
| Formato horizontal (× quadrado) | nada | **mais caro:** CPA +32%, CPC +13%, ROAS −26% |
| Formato vertical (× quadrado) | CTR −21%, engajamento +50% | nada |
| CTA | nada | CPC −8% (indício) |
| Duração | nada | CPC +4% a cada 10 s |
| Música/voz | só música prende mais (retenção +55%) | nada |
| Legenda | nada | nada |

- **O criativo age principalmente no começo do funil:** 9 efeitos confiáveis em 30 no começo, contra 8 em 50 no fim.
- **Vender depende mais do público e da oferta:** o retargeting tem CPA 44% menor, ROAS 66% maior e quase 4 vezes mais conversões.
- **Exceções no fim do funil:** muito texto atrapalha do clique à venda, e o formato horizontal sai mais caro por conversão.
- **A boa métrica depende do objetivo:**
  - em traffic (CTR), gancho e rosto sobem o CTR em cerca de 80%;
  - em awareness (retenção), muito texto derruba a retenção em 32%;
  - em conversions e app install (CPA), nenhum atributo muda o CPA de forma confiável.

## O que fiz, passo a passo

1. **Separei as colunas em três grupos:**
   - atributos do vídeo (o que o time controla);
   - contexto da campanha (plataforma, público);
   - resultados (as nove métricas), que só existem **depois** de postar.

   A Klike promete dar a nota **antes** de postar. Por isso, na Parte 2, os resultados não podem ser usados para prever a nota: seria corrigir a prova olhando o gabarito.
2. **Usei só valores reais.** Os valores preenchidos na pergunta 1.1 voltam a vazio (o indicador de faltante diz quais são), porque todos iguais à mediana diluiriam as diferenças.
3. **Correlação de Pearson e de Spearman:**
   - Pearson mede o quanto duas colunas andam juntas em linha reta;
   - Spearman faz a mesma conta sobre a ordem dos valores, então pega relações curvas e não se deixa levar por um valor gigante.
4. **Diferença das medianas com e sem cada atributo**, em %, com o número de criativos (n) de cada grupo. Para saber se a diferença é confiável, usei o **bootstrap**, o mesmo do Projeto_carros:
   - sorteei 2.000 vezes, com reposição, grupos do mesmo tamanho dos reais;
   - recalculei a diferença em cada sorteio;
   - os 95% do meio desses resultados formam o **intervalo de 95%**. Se ele não cruza o zero, o efeito é confiável.
5. **Formato e texto** (três níveis cada): mediana de cada nível, boxplot e **eta²**, que diz quanto da variação se explica só por saber o grupo (0 = nada, 1 = tudo).
6. **Duração e música/voz:** gráfico de dispersão com a mediana por faixa por cima.
7. **Confundimento,** com três checagens:
   - (a) se os grupos com e sem gancho têm a mesma proporção de retargeting e de cada plataforma;
   - (b) a mesma diferença calculada **dentro** de cada plataforma e de cada tipo de público;
   - (c) uma **regressão linear** com `get_dummies` (o one-hot do Projeto_carros), que lê o peso de cada atributo "mantendo o resto igual", com intervalo de 95% por bootstrap.
8. **Interações:** a diferença do rosto em cada faixa de idade e a do gancho em cada objetivo, em heatmaps com o n de cada célula. Células com menos de 15 criativos ficam em branco.
9. **A mesma regressão para cada uma das outras oito métricas:**
   - o alvo é o **log da métrica**, como o preço no Projeto_carros;
   - o peso se lê em %: `e^peso − 1` = quanto a métrica muda, mantendo o resto igual;
   - intervalo de 95% com 500 sorteios do bootstrap.
10. **Métrica principal de cada objetivo:**
    - awareness → retenção;
    - engagement → engajamento;
    - traffic → CTR;
    - conversions e app install → CPA.

    Para cada objetivo, medi o efeito de cada atributo na sua métrica principal (diferença das medianas com intervalo de 95%).

## Por que fiz assim

- **Mediana:** as métricas têm cauda longa (pergunta 1.1).
- **Bootstrap:** com 400 criativos, outra amostra daria números um pouco diferentes. O bootstrap mostra o quanto, sem fórmulas que exigiriam dados "bem comportados".
- **Desconfiar de um resultado isolado:**
  - são 45 comparações simples (5 atributos × 9 métricas) e 80 na regressão por métrica (10 atributos × 8 métricas);
  - algumas pareceriam confiáveis por sorte (cerca de 2 e 4);
  - por isso, só destaco o que se repete em várias métricas ou grupos.
- **Confundimento:** quem já conhece a marca (retargeting) clica mais. Se os vídeos com gancho fossem mostrados mais para esse público, o gancho levaria um crédito que é do público. Comparar dentro de grupos e a regressão separam os dois efeitos.
- **Regressão em todas as métricas, não só na nota:** o CPC e o CPA dependem muito da plataforma. Sem controle, um atributo comum numa rede barata pareceria "barato". A regressão compara criativos na mesma rede, categoria e público.
- **Nota em pontos, as outras métricas em log:**
  - a nota já é bem distribuída, então o peso se lê direto ("+17 pontos");
  - as outras métricas têm cauda longa, e no log o peso vira "%".
- **Métrica por objetivo:** cobrar venda de uma campanha de awareness seria injusto. Cada objetivo foi julgado pelo que ele quer.

## O que descobri

- **O gancho funciona dentro de todos os grupos:**
  - +53% de CTR no Meta, +83% no TikTok, +133% no LinkedIn, todos confiáveis;
  - na regressão, +17,5 pontos (intervalo de 15,7 a 19,1).
- **O retargeting não infla o gancho:** 22% dos vídeos com gancho são de retargeting, contra 27% dos sem gancho.
- **Na regressão da nota, mantendo o resto igual:**
  - rosto +11,8, legenda +7,9 (contra não ter), CTA +7,2;
  - muito texto −15,1 e pouco texto −8,0 (contra texto médio);
  - formato, duração e música/voz: sem efeito claro.
- **R² de 0,74:** só com o que se sabe antes de postar, a regressão explica 74% da variação da nota no treino. É otimista, porque foi medido nos mesmos dados; a Parte 2 confere no teste.
- **A densidade de texto tem correlação perto de zero com a nota, mas importa muito:** o meio é melhor que os extremos (forma de morro). Correlação perto de zero não quer dizer que não há relação.
- **Não há duração ideal:** a nota mediana fica entre 58 e 62 em todas as faixas.
- **O efeito do rosto no CTR parece mudar de rede para rede** (+66% no TikTok, +3% no Meta). Mas a pergunta 1.3 compara as redes diretamente e mostra que essa diferença **não é confiável**.
- **O gancho é o atributo mais forte no começo do funil, mas não mexe em nada no fim:** de −4% a +2% em taxa de conversão, ROAS, CPC e CPA.
- **Muito texto é o único atributo que pesa no funil inteiro:** CTR −25%, retenção −24%, taxa de conversão −14%, ROAS −20%.
- **O formato horizontal sai mais caro** que o quadrado na mesma rede: CPA +32%, CPC +13%, ROAS −26%.
- **Quem move o fim do funil é o público:** o retargeting tem CPA 44% menor, ROAS 66% maior e quase 4 vezes mais conversões.
- **Por objetivo:**
  - traffic: gancho +80% e rosto +85% de CTR;
  - awareness: muito texto −32% de retenção;
  - engagement: rosto +93% de engajamento, mas no limite do confiável;
  - conversions e app install: nenhum atributo muda o CPA de forma confiável.

## Limites

- **Dados observados, não experimento:** é associação, não causa. A prova seria um teste A/B (o mesmo anúncio com e sem gancho, para públicos sorteados).
- **Muitas comparações:** algumas parecem confiáveis por sorte. Os efeitos isolados (rosto no CPA, CTA no CPC, duração no CPC) são indícios.
- **Log de zero não existe:** na regressão por métrica, os criativos com 0 conversões (16) ou ROAS 0 fora de Branding (10) ficam de fora.
- **Grupos pequenos por objetivo:** de 36 a 129 criativos por objetivo, e vários grupos ficam abaixo de 15.
- **CTR cortado em 0,15:** o efeito do gancho no CTR está subestimado.
- **"Tem gancho" não diz se o gancho é bom:** medir a qualidade do criativo é justamente o papel do Klike.
- **Dados simulados:** a retenção que não cai com a duração parece uma simplificação.
