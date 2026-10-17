# 2.4 O que mais pesa na nota? Faz sentido para o negócio?

> Pergunta do case: feature importance: quais variáveis mais influenciam o score? Isso faz sentido do ponto de vista de negócio?
>
> Notebook: [`2_4_feature_importance.ipynb`](../../notebooks/parte2/2_4_feature_importance.ipynb) · Figuras: `reports/figures/parte2_fig1_o_que_pesa_na_nota.png` e `parte2_fig2_video_pesa_mais_que_campanha.png`

## Resposta curta

O que mais pesa na nota é o **conteúdo do vídeo**, e não a campanha em que ele roda. Comparando vídeos parecidos:

- vídeos com gancho nos 3 primeiros segundos têm cerca de **18 pontos** a mais;
- os com muito texto na tela, em vez de uma quantidade média, cerca de **15** a menos;
- os com rosto humano, cerca de **12** a mais;
- os com legenda e com chamada para ação, cerca de **8** a mais cada;
- os com pouco texto, cerca de 8 a menos.

No TikTok, vídeos só com música e sem voz têm cerca de 11 pontos a menos (o número exato é incerto: de 8 a 15); nas outras redes, a música não faz diferença. A rede social, o objetivo e o público pesam bem menos. Medi a importância de três jeitos, e os três concordam entre si e com a Parte 1.

## Por que isso importa

Os resultados fazem sentido para quem trabalha com anúncios. Os primeiros segundos decidem se a pessoa para de rolar o feed; um rosto prende a atenção e passa confiança; texto demais transforma o vídeo num "slide"; muita gente assiste sem som, e por isso a legenda ajuda; e dizer o que fazer no fim (a chamada para ação) anda junto com mais ação. Em uma frase: **comece pelo gancho, mostre um rosto, use texto na medida, legende, termine com uma chamada para ação e, no TikTok, use voz.**

## Como cheguei lá

**Li o peso de cada característica na regressão** (pergunta 2.2), em pontos de nota. É a leitura que o motor da Parte 3 usa.

**Medi a importância de um segundo jeito, embaralhando.** Peguei uma característica, por exemplo o gancho, sorteei de novo quem tem e quem não tem, e vi quanto o erro do modelo piorou. Se piora muito, o modelo dependia dela. É como tirar uma peça de um motor e ver o quanto ele perde força. Esse método se chama **importância por permutação**. Ele responde a uma pergunta diferente da do peso: o peso diz quanto vale ter o atributo; o embaralhamento diz quanto o modelo depende dele para acertar. Sem o gancho, o erro quase dobra. Depois vêm o rosto, o texto, a legenda e a chamada para ação, e só então a campanha.

**Conferi com a Random Forest** (o modelo de árvores do 2.2). Medida do mesmo jeito, ela dá o mesmo ranking. A medida de importância que ela traz pronta discorda, mas tem um defeito conhecido: favorece informações com muitos valores diferentes, como a duração, que embaralhada não faz diferença nenhuma.

**Conferi se os pesos são estáveis**, treinando o modelo nas 15 provas da validação cruzada. O gancho fica entre 17,4 e 18,4 pontos em todas. A exceção é a música no TikTok, que varia de −8 a −15, porque anda junto com a informação "é TikTok" e as duas dividem o crédito. Por isso, esse efeito deve ser apresentado como "cerca de 11 pontos, podendo ser de 8 a 15", e não como um número exato.

**Rosto e texto trocam de lugar conforme a medida, e isso ensina algo.** Em pontos, o excesso de texto (−15) pesa mais que o rosto (+12). Embaralhando, o rosto ganha, porque aparece em metade dos vídeos, e o excesso de texto em só 17%. A importância de uma característica depende do tamanho do efeito e de quantos vídeos a têm.

**Olhei o Modelo B**, que também vê os resultados da campanha. Mesmo com a taxa de cliques disponível, os atributos do vídeo vêm antes dela. Isso indica que os resultados acrescentam pouco ao que o vídeo já explica, uma boa notícia para um produto que avalia antes de postar.

## Limites

É associação, não causa: "vídeos com gancho têm 18 pontos a mais" não prova que colocar o gancho faz a nota subir; só um teste A/B provaria. Os dados são simulados, e a nota provavelmente foi gerada a partir destas mesmas características, o que explica por que um modelo simples explica tanto e os pesos são tão estáveis. E "tem gancho" não diz se o gancho é bom: o terço da nota que o modelo não explica provavelmente está na qualidade da execução.
