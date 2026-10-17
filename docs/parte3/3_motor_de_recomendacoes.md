# 3. Motor de recomendações

> Pergunta do case: usando os insights das Partes 1 e 2, construa um sistema simples de recomendações que analisa uma campanha e gera sugestões de melhoria: pelo menos 3 recomendações, acionáveis, quantificadas, contextuais e ordenadas por impacto, num protótipo que funcione.
>
> Notebook: [`3_motor_de_recomendacoes.ipynb`](../../notebooks/parte3/3_motor_de_recomendacoes.ipynb) · Código: [`src/recomendacoes.py`](../../src/recomendacoes.py)

## Resposta curta

O motor funciona como um **simulador de "e se"**. Ele pega o vídeo, muda uma coisa (por exemplo, acrescenta um gancho) e pergunta ao modelo da Parte 2 qual seria a nota. A diferença é o ganho estimado. Ele faz isso para cada mudança possível e entrega as três de maior ganho, em ordem. Quando a Parte 1 tem um padrão confiável, acrescenta a faixa do efeito na métrica que a campanha quer mover, na rede dela. Por fim, se a campanha não usa retargeting, sugere isso à parte, porque é uma decisão de público, e não do vídeo. Um exemplo real, de uma campanha de tráfego no LinkedIn que o modelo nunca viu:

```
1. Adicionar um gancho nos 3 primeiros segundos: vídeos parecidos com essa mudança têm nota ~18 pontos maior
   (de 49 para ~67); no LinkedIn, vídeos com gancho têm CTR entre +25% e +355% maior (comparação simples, 66 vídeos).
2. Mostrar um rosto humano no vídeo: vídeos parecidos com essa mudança têm nota ~12 pontos maior (de 49 para ~61).
3. Manter o texto na tela em nível médio: vídeos parecidos sem isso têm nota ~15 pontos menor (de 49 para ~34).
4. Sugestão de público (não é mudança no vídeo): campanhas que também miram quem já conhece a marca
   (retargeting) têm nota ~4 pontos maior.
```

Para rodar com qualquer campanha: `python -m src.recomendacoes KLK-0479`.

## Por que isso importa

Cada recomendação diz o que mudar e quanto isso anda junto com a nota, em pontos. Quando há um padrão confiável, diz também a faixa do efeito na métrica da campanha. A faixa larga do exemplo ("entre +25% e +355%") é proposital: a direção é clara (vídeos com gancho têm mais cliques no LinkedIn), mas o tamanho exato foi medido em poucos vídeos e é incerto. Se o vídeo já faz quase tudo certo, o motor não inventa melhoria: diz o que manter e quanto custaria mudar.

## Como cheguei lá

**Usei o modelo da Parte 2 como simulador.** Ele só usa o que existe antes de postar, então as recomendações valem antes de publicar. E, por ser uma regressão linear, o ganho de cada mudança é o próprio peso dela, comparando vídeos parecidos.

**Só considero o que o vídeo ainda não faz:** acrescentar gancho, rosto, chamada para ação ou legenda; levar o texto para o nível médio; trocar música por voz; mudar para um formato que a rede usa. Mudanças que somam menos de 1 ponto de nota não entram, porque pedir ao time um trabalho que não muda nada não é uma recomendação útil.

**A métrica mostrada depende do objetivo.** A Parte 1 mostrou que cada objetivo tem a sua métrica de sucesso: retenção para campanhas feitas para serem vistas, engajamento para as de engajamento, cliques para as de tráfego. Nas de venda e de instalação de app, o vídeo não anda junto com o custo por venda, então mostro o efeito nos cliques, a etapa anterior. O número vem da tabela por rede da Parte 1 e é uma comparação simples. Por isso aparece como faixa, com o número de vídeos, e só quando é confiável. Um efeito fraco pode até apontar para o lado contrário da nota, e confundiria quem lê.

**Não recomendo mudar a duração.** O enunciado dá esse exemplo ("reduzir de 45 s para 20 s"), mas nestes dados não existe duração ideal (Parte 1), e a duração quase não pesa na nota (Parte 2). Recomendar isso seria inventar.

**O contexto entra, mas com um limite que é preciso dizer.** O ganho na nota é quase o mesmo em qualquer rede, objetivo ou categoria: o gancho soma cerca de 18 pontos no Meta, no TikTok e no LinkedIn, porque o modelo soma os efeitos. É coerente com a Parte 1, que mostrou que o que funciona é quase igual nas três redes. O contexto entra de três jeitos: a voz só é sugerida no TikTok (onde vídeos sem voz têm nota menor); a métrica mostrada depende da rede e do objetivo; e as mudanças possíveis respeitam a rede (o LinkedIn nunca recebe "mude para vertical", formato que lá quase não existe). A categoria do produto não entra, porque repete o objetivo da campanha.

## O que descobri

Nas 100 campanhas de teste, todas receberam 3 recomendações para o vídeo: 63 com três melhorias, 20 com duas, 12 com uma e 5 com nenhuma, que já seguiam quase tudo e foram completadas com "manter". 80 receberam também a sugestão de público. Em 1º lugar apareceram quase sempre os maiores efeitos: acrescentar um gancho (metade das campanhas), mostrar um rosto, reduzir o texto e colocar legenda.

As campanhas em que o motor vê mais espaço para melhorar são as de nota real mais baixa (nota mediana de 48, contra 80 nas de menos espaço). Mas isso **não prova** que as recomendações funcionam: o ganho é calculado pelo próprio modelo, e por isso acompanha a nota prevista quase por construção. Ele acompanha a nota real só porque o modelo acerta bem a nota. Mostra que o motor é consistente com o modelo, e não mais que isso.

## Limites

É associação, não causa: o motor diz que vídeos parecidos com gancho têm nota maior, e só um teste A/B provaria que acrescentar o gancho faz a nota subir. Cada ganho é calculado sozinho; várias mudanças juntas tendem a somar, mas a nota não passa de 100. "Tem gancho" não diz se o gancho é bom. E os dados são simulados: com dados reais, os ganhos devem ser menores e menos limpos.
