# Pergunta 1.2: quais atributos do criativo se associam a boa performance?

Notebook: [`notebooks/parte1/1_2_atributos_x_performance.ipynb`](../../notebooks/parte1/1_2_atributos_x_performance.ipynb).

## Pergunta

Quais atributos do criativo mais se correlacionam com boas métricas de performance (CTR, ROAS, conversões etc.)?

## Resposta curta

O atributo mais forte é o **gancho nos 3 primeiros segundos**: um começo feito para a pessoa parar de rolar o feed. Vídeos com gancho têm nota cerca de 17 pontos maior (numa escala de 0 a 100), 53% mais cliques e 41% mais retenção, mesmo comparando com vídeos parecidos em todo o resto. Em segundo lugar vem o **rosto humano** (cerca de +12 pontos). Depois vêm a **legenda** e a **chamada para ação** (cerca de +7 a +8 cada).

A quantidade de **texto na tela** tem um ponto ideal no meio: muito texto tira cerca de 15 pontos, e pouco texto tira cerca de 8. A duração, o formato e a mistura de música e voz quase não fazem diferença na nota.

A pergunta cita CTR, ROAS e conversões "etc.". Por isso olhei nove métricas, do primeiro contato até a venda. O resultado mais interessante foi este: **o vídeo decide se a pessoa para e clica, mas quase não decide se ela compra.** O gancho não muda a taxa de conversão nem o custo por venda. Quem mexe na venda é o público: para quem já conhece a marca, cada venda sai 44% mais barata. A exceção é o excesso de texto, que atrapalha do clique até a venda.

## O que fiz, passo a passo

**1. Separei o que se sabe antes de postar do que só se sabe depois.** O vídeo (gancho, rosto, texto, duração) e a campanha (rede, público, objetivo) existem antes. Os resultados (cliques, engajamento, vendas, nota) só existem depois. A Klike promete avaliar o vídeo antes de ele ir ao ar. Então os resultados são o que eu quero explicar, e nunca podem ser usados para prever a nota. Seria como corrigir a prova olhando o gabarito.

**2. Usei só valores reais.** Os vazios que a pergunta 1.1 preencheu voltaram a ficar vazios aqui. Todos eles valiam a mediana, e isso diluiria as diferenças que eu queria medir.

**3. Medi o quanto cada atributo anda junto com cada métrica.** Usei a **correlação**, um número de −1 a +1 que diz se duas coisas sobem e descem juntas. Usei duas versões: uma mede relações em linha reta, a outra mede relações que sobem sempre, mesmo em curva.

**4. Comparei vídeos com e sem cada atributo.** Para cada atributo, separei os vídeos que têm e os que não têm, e comparei a mediana de cada métrica. Para saber se a diferença é confiável ou poderia ser sorte, refiz a comparação 2.000 vezes, cada vez com um sorteio diferente dos mesmos vídeos (técnica chamada **bootstrap**). É como repetir uma pesquisa de opinião várias vezes para ver o quanto o resultado oscila. Se, em 95% das repetições, a diferença fica do mesmo lado do zero, chamo o efeito de **confiável**.

**5. Olhei formato e quantidade de texto** (três níveis cada), comparando a mediana de cada nível.

**6. Olhei duração e música/voz** em gráficos de pontos, com a mediana por faixa desenhada por cima. Se existisse uma duração ideal, a linha subiria e depois desceria.

**7. Conferi se o efeito é mesmo do vídeo, ou do público.** Quem já conhece a marca clica mais. Se os vídeos com gancho fossem mostrados mais para esse público, o gancho levaria um crédito que não é dele. Esse problema se chama **confundimento**, e o exemplo clássico é que vendas de sorvete e afogamentos sobem juntos por causa do verão, não um por causa do outro. Conferi de três jeitos:

- se os grupos com e sem gancho têm o mesmo tipo de público;
- se o efeito continua dentro de cada rede e dentro de cada público;
- com uma **regressão linear**, uma conta que mede o efeito de cada atributo "mantendo todo o resto igual". É como comparar dois vídeos idênticos em tudo, menos no gancho.

**8. Testei se o efeito muda com o público:** o rosto por idade e o gancho por objetivo da campanha.

**9. Repeti a regressão para cada uma das nove métricas**, para ver em que etapa do caminho do cliente cada atributo age. Esse caminho é o **funil**: ver o anúncio, interagir, clicar, comprar.

**10. Julguei cada objetivo pela sua métrica:** retenção para as campanhas feitas para serem vistas, engajamento para as de engajamento, cliques para as de tráfego, custo por venda para as de conversão.

## Por que fiz assim

**Mediana e bootstrap**, porque as métricas têm campanhas gigantes misturadas (pergunta 1.1), e porque com 400 vídeos qualquer número oscila um pouco. O bootstrap mostra o quanto, sem exigir fórmulas complicadas.

**Desconfiar de resultado isolado.** Fiz dezenas de comparações, e algumas parecem confiáveis só por sorte (cerca de 1 em cada 20). Por isso só destaco o que se repete em várias métricas, redes ou públicos. O gancho, por exemplo, aparece em todas.

**Regressão para cada métrica, e não só para a nota.** O custo por clique depende muito da rede social. Sem comparar vídeos da mesma rede, um atributo comum numa rede barata pareceria "barato" por engano.

**Cada objetivo pela sua métrica.** Cobrar venda de uma campanha feita só para ser vista seria injusto.

## O que descobri

**O gancho funciona em todo lugar.** Ele sobe os cliques em 53% no Meta, 83% no TikTok e 133% no LinkedIn, sempre de forma confiável. Na regressão, vale +17,5 pontos de nota, quase o mesmo da comparação simples (+17,6). Isso mostra que o público não estava inflando o efeito. De fato, os vídeos com gancho até têm um pouco menos de público que já conhece a marca (22%, contra 27% dos sem gancho).

**Os outros atributos, mantendo o resto igual:** o rosto vale +11,8 pontos, a legenda +7,9 e a chamada para ação +7,2. Muito texto tira 15,1 pontos e pouco texto tira 8,0, sempre em comparação com o texto médio. Formato, duração e música/voz não têm efeito claro.

**Correlação perto de zero não quer dizer "sem relação".** A quantidade de texto tem correlação quase nula com a nota, mas importa muito. A relação tem forma de morro: o meio é o melhor, e os dois extremos perdem. A correlação só enxerga relações que sobem ou descem sempre, e não vê um morro.

**Não existe duração ideal nestes dados.** A nota mediana fica entre 58 e 62 em todas as faixas de duração.

**O vídeo age no começo do funil.** Nas métricas de ver, interagir e clicar, encontrei 9 efeitos confiáveis em 30 comparações. Nas de comprar, encontrei 8 em 50, e a maioria pequenos. O gancho, o mais forte no começo, não muda nada no fim. As exceções são duas:

- o excesso de texto, que derruba os cliques (−25%), a retenção (−24%), a taxa de conversão (−14%) e o retorno (−20%);
- o vídeo horizontal, que sai mais caro: cada venda custa 32% mais que no formato quadrado da mesma rede.

**Quem decide a venda é o público.** Para quem já conhece a marca, a conversão é 89% maior, cada venda sai 44% mais barata e o retorno é 66% maior.

**Por objetivo:** nas campanhas de tráfego, gancho e rosto sobem os cliques em cerca de 80%. Nas feitas para serem vistas, muito texto derruba a retenção em 32%. Nas de conversão e de instalação de app, nenhum atributo do vídeo muda o custo por venda de forma confiável.

O rosto parece ajudar muito os cliques no TikTok (+66%) e quase nada no Meta (+3%). A pergunta 1.3 compara as redes diretamente e mostra que essa diferença não é confiável.

## Limites

São dados observados, não um experimento. Por isso, os resultados mostram o que **anda junto**, não o que **causa**. A prova de causa seria um teste A/B: o mesmo anúncio com e sem gancho, mostrado a públicos sorteados. Além disso:

- o limite do CTR em 0,15 faz o efeito do gancho nos cliques parecer menor do que é;
- "tem gancho" não diz se o gancho é bom;
- os grupos por objetivo são pequenos (de 36 a 129 vídeos);
- nos dados simulados, a retenção não cai com vídeos mais longos, o que provavelmente é uma simplificação de quem gerou os dados.
