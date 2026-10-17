# 1.2 Quais atributos do criativo se associam a boa performance?

> Pergunta do case: quais atributos do criativo mais se correlacionam com boas métricas de performance (CTR, ROAS, conversões etc.)?
>
> Notebook: [`1_2_atributos_x_performance.ipynb`](../../notebooks/parte1/1_2_atributos_x_performance.ipynb)

## Resposta curta

O atributo mais forte é o **gancho nos 3 primeiros segundos**, um começo feito para a pessoa parar de rolar o feed. Comparando vídeos parecidos em todo o resto, vídeos com gancho têm nota cerca de **18 pontos** maior (numa escala de 0 a 100), cerca de **50% mais cliques** e cerca de 40% mais retenção. Depois vêm o **rosto humano** (cerca de 12 pontos) e a **legenda** e a **chamada para ação** (cerca de 7 a 8 pontos cada). A quantidade de **texto na tela** tem um ponto ideal no meio: vídeos com muito texto têm cerca de 15 pontos a menos, e os com pouco texto, cerca de 8 a menos. Duração, formato e mistura de música e voz quase não fazem diferença.

## Por que isso importa

Olhei nove métricas, do primeiro contato até a venda, e não só as três que a pergunta cita. Elas mostraram em que etapa do caminho do cliente cada atributo aparece. **Vídeos com gancho têm mais cliques e mais retenção, mas não convertem mais**: a taxa de conversão, o custo por venda e o retorno deles são praticamente iguais aos dos vídeos sem gancho. Já as **campanhas de retargeting** (que miram quem já conhece a marca) convertem 89% mais e com custo por venda 44% menor. Isso vem de uma comparação simples, que não controla rede nem objetivo. A leitura prática é: o criativo é a vitrine, e se espera dele atenção e clique; para a venda, olhe também o público e a oferta. A exceção é o excesso de texto, que anda junto com resultados piores do clique até a venda.

## Como cheguei lá

**Separei o que se sabe antes de postar do que só se sabe depois.** O vídeo e a campanha existem antes; os cliques, as vendas e a nota só depois. Os resultados são o que eu quero explicar e nunca podem servir de pista para prever a nota, porque seria como corrigir a prova olhando o gabarito.

**Comparei vídeos com e sem cada atributo, pela mediana** (o valor do meio, que não se deixa puxar por campanhas gigantes, como na pergunta 1.1).

**Medi se cada diferença é confiável.** Com 400 vídeos, qualquer número oscila. Para saber quanto, refiz cada comparação 2.000 vezes, cada vez com um sorteio diferente dos mesmos vídeos (técnica chamada **bootstrap**). É como repetir uma pesquisa de opinião várias vezes para ver o quanto o resultado muda. Se, em 95% das repetições, a diferença fica do mesmo lado do zero, chamo o efeito de **confiável**. Como fiz dezenas de comparações, e cerca de 1 em cada 20 parece confiável só por sorte, só destaco o que se repete em várias métricas, redes ou públicos.

**Usei a correlação com cuidado.** A correlação diz, de −1 a +1, se duas coisas sobem e descem juntas. O texto na tela tem correlação quase zero com a nota e, mesmo assim, importa muito, porque a relação tem forma de morro: o meio é melhor que os dois extremos. Correlação perto de zero não quer dizer "sem relação".

**Conferi se o efeito é do vídeo ou do público.** Quem já conhece a marca clica mais. Se os vídeos com gancho fossem mostrados mais para esse público, o gancho levaria um crédito que não é dele. Esse problema se chama **confundimento**; o exemplo clássico é que vendas de sorvete e afogamentos sobem juntos por causa do verão, não um por causa do outro. Conferi de três jeitos. Os grupos com e sem gancho têm o mesmo tipo de público (22% e 27% de retargeting). O gancho continua funcionando dentro de cada rede e de cada público. E uma **regressão linear**, uma conta que mede o efeito de cada atributo "mantendo todo o resto igual", deu praticamente o mesmo número da comparação simples. Daqui em diante, quando digo "**comparando vídeos parecidos**", é dessa conta que estou falando.

**Repeti a conta para cada métrica e julguei cada objetivo pela sua.** Nas métricas de ver, interagir e clicar, encontrei 9 efeitos confiáveis em 30 comparações; nas de converter e vender, 8 em 50, quase todos pequenos. Nas campanhas de tráfego, vídeos com gancho ou rosto têm CTR cerca de 80% maior. Nas feitas para serem vistas, vídeos com muito texto têm retenção 32% menor. Nas de conversão e de instalação de app, nenhum atributo do vídeo anda junto com um custo por venda diferente.

Não existe duração ideal nestes dados: a nota mediana fica entre 58 e 62 em todas as faixas de duração.

## Limites

São dados observados, não um experimento: os resultados mostram o que anda junto, não o que causa. A prova de causa seria um teste A/B, o mesmo anúncio com e sem gancho, mostrado a públicos sorteados. O limite de 15% no CTR faz o efeito do gancho nos cliques parecer menor do que é. "Tem gancho" não diz se o gancho é bom. E os grupos por objetivo são pequenos (de 36 a 129 vídeos).
