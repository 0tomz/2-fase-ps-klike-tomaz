# Pergunta 2.4: o que mais pesa na nota? Faz sentido para o negócio?

Notebook: [`notebooks/parte2/2_4_feature_importance.ipynb`](../../notebooks/parte2/2_4_feature_importance.ipynb). Figuras: `reports/figures/parte2_fig1_o_que_pesa_na_nota.png` e `parte2_fig2_video_pesa_mais_que_campanha.png`.

## Pergunta

Feature importance: quais variáveis mais influenciam o score? Isso faz sentido do ponto de vista de negócio?

## Resposta curta

O que mais pesa na nota é o **conteúdo do vídeo**, e não a campanha em que ele roda. Mantendo todo o resto igual:

- ter um gancho nos 3 primeiros segundos soma cerca de **18 pontos**;
- ter muito texto na tela, em vez de uma quantidade média, tira cerca de **15**;
- mostrar um rosto humano soma cerca de **12**;
- legenda e chamada para ação somam cerca de **8** cada;
- pouco texto também tira pontos (cerca de 8), porque o melhor é o meio.

No TikTok, um vídeo só com música e sem voz perde cerca de 11 pontos; nas outras redes, a música não faz diferença. A rede social, o objetivo da campanha e o público pesam bem menos.

Medi a importância de três jeitos diferentes, e os três concordam entre si e com a Parte 1. Os resultados fazem sentido para o marketing:

- os primeiros segundos decidem se a pessoa para de rolar o feed;
- um rosto prende a atenção e passa confiança;
- texto demais transforma o vídeo num "slide";
- muita gente assiste sem som, e por isso a legenda ajuda.

## O que fiz, passo a passo

**1. Li o peso de cada característica na regressão linear**, em pontos de nota. Para uma característica de sim/não, o peso é quanto a nota sobe (ou desce) por ter aquilo, mantendo todo o resto igual. Também calculei uma versão dos pesos na mesma escala para todas as colunas, que permite comparar uma característica medida em segundos com outra medida em sim/não.

**2. Conferi se os pesos são estáveis.** Treinei o modelo 15 vezes, cada vez com uma parte diferente dos vídeos, e anotei o peso de cada característica em cada vez. Se um peso muda muito, não dá para confiar no número exato.

**3. Medi a importância de outro jeito, embaralhando.** Peguei uma característica, por exemplo o gancho, e sorteei de novo quem tem e quem não tem, quebrando a ligação dela com a nota. Depois medi quanto o erro do modelo piorou. Se piorou muito, o modelo dependia dela. É como tirar uma peça de um motor e ver o quanto ele perde força. Esse método se chama **importância por permutação**. Ele tem duas vantagens: mede a característica inteira (os três níveis de texto juntos, por exemplo) e é medido em vídeos que o modelo não viu.

**4. Fiz o mesmo com a Random Forest** e comparei com a medida de importância que ela traz pronta.

**5. Comparei os rankings** da regressão linear, da Random Forest e da Parte 1.

**6. Repeti a medida no Modelo B**, que também recebe os resultados da campanha.

**7. Traduzi cada resultado para o negócio** e montei duas figuras de apresentação.

## Por que fiz assim

**Pesos em pontos**, porque é a leitura que a Parte 3 usa para recomendar: "adicione um gancho: +18 pontos".

**Embaralhar, além de ler os pesos**, porque são duas perguntas diferentes. O peso diz quanto vale ter o atributo. O embaralhamento diz quanto o modelo depende dele para acertar. Um atributo pode valer muito e aparecer em poucos vídeos.

**Desconfiar da medida pronta da Random Forest.** Ela é calculada nos próprios dados de treino e costuma favorecer colunas com muitos valores diferentes, como a duração, mesmo quando elas não ajudam a prever. Os números confirmaram essa desconfiança.

## O que descobri

**Embaralhando, o gancho é de longe o mais importante.** Sem ele, o erro do modelo quase dobra (sobe 5,6 pontos). Depois vêm o rosto (+2,7), o texto na tela (+2,4), a legenda (+1,2) e a chamada para ação (+1,0). Só então aparece a campanha: rede (+0,4), público que já conhece a marca (+0,3) e objetivo (+0,3). Formato, música, idade do público e duração quase não ajudam a prever.

**A Random Forest concorda,** quando medida do mesmo jeito: gancho, rosto e texto no topo. A medida pronta dela discorda, e mostra os seus defeitos. Dá 34% da importância para a contagem de boas práticas, que "rouba" o crédito do gancho, do rosto, da legenda e da chamada para ação, já que é a soma deles. E dá importância à duração e à música, que, embaralhadas, não fazem diferença nenhuma.

**Os pesos são estáveis.** O gancho fica entre 17,4 e 18,4 pontos nas 15 vezes. A exceção é a música no TikTok, que varia de −8 a −15 pontos, porque anda junto com a coluna "é TikTok" e as duas dividem o crédito. Por isso, essa recomendação deve ser apresentada como "cerca de 10 pontos", e não como um número exato.

**O rosto e o texto trocam de lugar conforme a medida, e isso ensina algo.** Em pontos, muito texto (−15) pesa mais que o rosto (+12). Embaralhando, o rosto ganha. A razão é que o rosto aparece em metade dos vídeos, e o excesso de texto em só 17% deles. A importância de uma característica depende do tamanho do efeito e também de quantos vídeos a têm.

**Mesmo com os resultados da campanha, o vídeo domina.** No Modelo B, gancho, rosto, texto, chamada para ação e legenda vêm antes da primeira métrica de resultado, a taxa de cliques. Eu esperava o contrário, porque a nota mede desempenho e os cliques são desempenho. Isso diz que os resultados acrescentam pouco ao que o vídeo já explica. Para um produto que avalia antes de postar, é uma boa notícia.

**Os números batem com a Parte 1:** gancho +17,9 (era +17,5), rosto +11,5 (+11,8), muito texto −15,1 (−15,1), legenda +8,1 (+7,9), chamada para ação +7,5 (+7,2), público que já conhece a marca +4,4 (+4,5).

## Limites

**É associação, não causa.** "O gancho vale +18 pontos" quer dizer que, nestes dados, vídeos com gancho têm nota maior que vídeos iguais sem gancho. Só um teste A/B provaria que colocar o gancho faz a nota subir.

**Os dados são simulados.** A nota provavelmente foi gerada a partir destas mesmas características, quase somando os efeitos. Isso explica por que um modelo simples explica tanto, por que os pesos são tão estáveis e por que os cliques pesam pouco. Com dados reais, os efeitos devem ser menores e menos limpos.

**"Tem gancho" não diz se o gancho é bom.** O terço da nota que o modelo não explica provavelmente está na qualidade de execução, que estes dados não medem.
