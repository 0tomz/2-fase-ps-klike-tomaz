# 1.3 Existem padrões diferentes por plataforma?

> Pergunta do case: existem padrões diferentes por plataforma? O que funciona no TikTok funciona no LinkedIn (por exemplo)?
>
> Notebook: [`1_3_padroes_por_plataforma.ipynb`](../../notebooks/parte1/1_3_padroes_por_plataforma.ipynb)

## Resposta curta

Sim, as redes são diferentes, mas a diferença está mais no **ambiente** de cada uma do que no **que funciona** nelas. Um clique custa R$0,51 no TikTok, R$0,80 no Meta e R$2,49 no LinkedIn, cerca de cinco vezes mais. O TikTok engaja quase o dobro das outras. Já o que anda junto com nota maior é quase igual nas três: gancho, rosto e evitar excesso de texto. A exceção é a voz: no TikTok, vídeos só com música e sem voz têm nota cerca de 13 pontos menor, comparando vídeos parecidos; no Meta e no LinkedIn, a música não faz diferença. Respondendo ao exemplo do enunciado: o que funciona no TikTok funciona no LinkedIn na mesma direção.

## Por que isso importa

Não é preciso um manual diferente para cada rede. O básico vale nas três: gancho nos primeiros segundos, rosto humano e texto na medida. O ajuste que muda é um só: **no TikTok, use voz**. Os custos, por outro lado, são muito diferentes, e comparar o custo de uma campanha do LinkedIn com o de uma do TikTok não faz sentido. No LinkedIn, cada venda sai cerca de quatro vezes mais cara (R$70 contra R$16), mas a taxa de conversão é a mesma nas três redes (cerca de 3%). A venda lá é cara porque o clique é caro, não porque as pessoas compram menos.

## Como cheguei lá

**Tratei o "TikTok × LinkedIn" como exemplo** e comparei as três redes, duas a duas. Olhar só aquele par deixaria de fora o Meta, a rede com mais vídeos e, portanto, a mais bem medida.

**Medi o efeito de cada atributo dentro de cada rede**, com a mesma comparação de medianas e o mesmo teste de confiança da pergunta 1.2 (refazer a conta com milhares de sorteios dos mesmos vídeos).

**Comparei a diferença entre os efeitos, e não só cada efeito.** Este é o cuidado principal. Dizer "o rosto é confiável no TikTok e não no LinkedIn" não prova que o rosto funciona diferente nas duas redes; pode ser só que o LinkedIn tem menos vídeos e uma medida mais incerta. Para afirmar que um efeito muda de rede para rede, calculei a diferença entre os dois efeitos e perguntei se essa diferença é confiável. Das 72 comparações, só uma foi: o rosto anda junto com mais retenção no Meta, mas não no TikTok. É menos do que o acaso produziria, então não há sinal de que o que funciona mude de rede para rede.

**Usei a regressão dentro de cada rede** (a conta "comparando vídeos parecidos" da pergunta 1.2). Ela separa atributos que vêm juntos e que a comparação simples mistura. Foi assim que a voz apareceu: na comparação simples, vídeos com mais música que voz tinham só 3,8 pontos a menos no TikTok; comparando vídeos parecidos, são 13,4. É o que mostra a figura 2 da pergunta 1.4. A mesma conta sugere que o gancho pesa um pouco mais no LinkedIn (cerca de 25 pontos, contra 17 nas outras redes), mas essa diferença está no limite do confiável e foi medida em poucos vídeos.

**Ignorei grupos com menos de 15 vídeos**, que mudam muito por acaso. Por isso algumas comparações não puderam ser feitas: o TikTok não tem vídeo horizontal, e o LinkedIn tem só 9 verticais.

Dentro de cada rede, o formato quase não importa, e também não há duração ideal. O excesso de texto anda junto com nota menor nas três redes; nos cliques, a queda só é confiável no Meta (−32%), justamente o exemplo que o enunciado dava. A tabela completa dos efeitos por rede ficou salva para o motor de recomendações da Parte 3.

## Limites

Não achar diferença não prova que os efeitos são iguais: com estes tamanhos, só diferenças grandes apareceriam. O LinkedIn tem só 66 vídeos, então os números dele indicam uma direção, não um valor preciso. E, como em toda a Parte 1, é o que anda junto, não necessariamente o que causa.
