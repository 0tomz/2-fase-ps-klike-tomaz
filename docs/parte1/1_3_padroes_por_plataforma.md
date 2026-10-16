# Pergunta 1.3: existem padrões diferentes por plataforma?

Notebook: [`notebooks/parte1/1_3_padroes_por_plataforma.ipynb`](../../notebooks/parte1/1_3_padroes_por_plataforma.ipynb).

## Pergunta

Existem padrões diferentes por plataforma? O que funciona no TikTok funciona no LinkedIn (por exemplo)?

Li o "TikTok × LinkedIn" como um exemplo. Por isso comparei as três redes da base (Meta, TikTok e LinkedIn), duas a duas.

## Resposta curta

Sim, as redes são diferentes, mas a diferença está mais no **ambiente** de cada uma do que no **que funciona** nelas.

O ambiente muda muito:

- um clique custa R$0,51 no TikTok, R$0,80 no Meta e R$2,49 no LinkedIn;
- cada venda custa R$15,9, R$24,2 e R$70,2, nessa ordem. A taxa de conversão é a mesma nas três (cerca de 3%): no LinkedIn, a venda é mais cara porque o clique é mais caro, não porque as pessoas compram menos;
- o TikTok engaja quase o dobro das outras;
- o TikTok é quase todo vertical e curto, e o LinkedIn é horizontal ou quadrado e mais longo.

Já o que funciona é quase o mesmo nas três redes: gancho (cerca de +17 pontos de nota), rosto (+9 a +12) e evitar muito texto (−12 a −16). Comparei o efeito de cada atributo entre as redes, duas a duas, e só 1 de 72 diferenças foi confiável. É menos do que o acaso produziria.

Apareceram dois indícios de diferença. No TikTok, tirar a voz e deixar só música custa cerca de 12 pontos a mais do que no Meta. E o gancho parece pesar um pouco mais no LinkedIn. Respondendo ao exemplo do enunciado: o que funciona no TikTok funciona no LinkedIn na mesma direção. Não achei nenhuma diferença confiável entre essas duas redes, mas o LinkedIn tem poucos vídeos para enxergar diferenças pequenas.

## O que fiz, passo a passo

**1. Descrevi cada rede:** custos, cliques, engajamento, retenção, conversão, retorno e nota, além do tipo de vídeo que cada uma usa. Também medi quanto de cada métrica se explica só por saber a rede.

**2. Medi o efeito de cada atributo dentro de cada rede.** É a mesma comparação da pergunta 1.2 (vídeos com e sem o atributo, com o teste de confiança por sorteios repetidos), feita separadamente no Meta, no TikTok e no LinkedIn.

**3. Comparei as redes duas a duas.** Aqui está o cuidado principal. Dizer "o rosto é confiável no TikTok e não no LinkedIn" não prova que o rosto funciona diferente nas duas. Pode ser só que o LinkedIn tem menos vídeos, e por isso a medida dele é mais incerta. Para afirmar que um efeito muda de uma rede para outra, calculei a **diferença entre os efeitos** e perguntei se essa diferença é confiável.

**4. Usei uma regressão linear dentro de cada rede** (a conta "mantendo todo o resto igual" da pergunta 1.2). Ela separa atributos que vêm juntos e que a comparação simples mistura.

**5. Olhei duração, formato e quantidade de texto em cada rede**, sempre com o número de vídeos de cada grupo. Grupos com menos de 15 vídeos ficaram de fora, porque mudam muito por acaso.

**6. Montei um manual por rede:** o que mais sobe e o que mais derruba a nota em cada uma. Salvei a tabela completa para o motor de recomendações da Parte 3.

## Por que fiz assim

**Comparar todos os pares responde à pergunta geral.** Olhar só TikTok × LinkedIn deixaria de fora o Meta, a rede com mais vídeos e, portanto, a mais bem medida.

**Testar a diferença entre os efeitos, e não só cada efeito.** Sem esse cuidado, eu confundiria "falta de dados numa rede" com "a rede funciona diferente".

**Usar a regressão por rede**, porque a comparação simples mistura atributos. Um exemplo: na comparação simples, "mais música que voz" no TikTok tirava só 3,8 pontos, porque esses vídeos também diferiam em outras coisas. Mantendo o resto igual, o efeito aparece de verdade: −13,4 pontos.

## O que descobri

**O custo depende muito da rede.** A rede explica 77% da variação do custo por clique. Comparar custos entre redes sem levar isso em conta é injusto. O CTR, por outro lado, é quase igual nas três (de 6,0% a 6,6%).

**Os atributos funcionam do mesmo jeito nas três redes.** O gancho sobe a nota em 17 a 18 pontos e a retenção em 32% a 42%, nas três. O rosto sobe a nota em 9 a 12 pontos, nas três. Muito texto derruba a nota em 12 a 16 pontos, nas três. A chamada para ação e a legenda também sobem a nota nas três, mas só são confiáveis no Meta, a rede com mais vídeos.

**Comparando os efeitos de rede para rede, quase nada muda.** Das 72 comparações, só uma foi confiável: o rosto segura a retenção no Meta (+32%), mas não no TikTok (−6%). Isso não prova que os efeitos sejam iguais. As medidas são incertas o bastante para que só diferenças grandes apareçam. Mas não há sinal de diferença.

**Na regressão por rede, apareceram dois indícios.** Vídeo só com música, sem voz, perde 13,4 pontos no TikTok, e quase nada no Meta (−1,2) e no LinkedIn (−1,8). A diferença entre TikTok e Meta é confiável. O gancho vale 24,7 pontos no LinkedIn, contra 17,1 no Meta, uma diferença no limite do confiável. Como fiz 21 comparações, uma delas poderia ser sorte. Por isso trato as duas como indícios, e a da voz como a mais forte.

**Não há duração ideal por rede.** A "melhor faixa" muda de uma métrica para outra, e os grupos são pequenos.

**O formato quase não importa dentro de cada rede.** Na nota e nos cliques, nenhum formato ganha de outro. A única diferença confiável: no Meta, o vertical engaja 57% mais que o horizontal.

**Muito texto atrapalha nas três redes.** Nos cliques, a queda só é confiável no Meta (−32%), justamente o exemplo que o enunciado dava.

**O manual por rede.** No Meta, as melhores escolhas são gancho (+18 pontos), rosto (+12) e chamada para ação (+8). No TikTok, gancho (+17), rosto (+9) e legenda (+5). No LinkedIn, gancho (+17), rosto (+12) e legenda (+11). Nas três, o que mais derruba é muito texto (de −12 a −17). No TikTok, também derruba o vídeo só com música, sem voz. O manual quase se repete, e isso diz algo importante para a Parte 3: o motor pode usar regras comuns às três redes e acrescentar poucos ajustes, como a voz no TikTok.

## Limites

Não achar diferença não prova igualdade: com estes tamanhos, só diferenças grandes seriam detectadas. O LinkedIn tem só 66 vídeos, então os números dele indicam uma direção, não um valor preciso. Algumas comparações não puderam ser feitas, porque o TikTok não tem vídeo horizontal e o LinkedIn tem só 9 verticais. E, como em toda a Parte 1, são dados observados e simulados: o que anda junto, não necessariamente o que causa.
