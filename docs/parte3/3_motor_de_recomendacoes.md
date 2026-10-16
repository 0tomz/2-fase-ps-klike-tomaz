# Parte 3: motor de recomendações

Notebook: [`notebooks/parte3/3_motor_de_recomendacoes.ipynb`](../../notebooks/parte3/3_motor_de_recomendacoes.ipynb). Motor: [`src/recomendacoes.py`](../../src/recomendacoes.py).

## Pergunta

Usando os insights das Partes 1 e 2, construa um sistema simples de recomendações que analisa uma campanha e gera sugestões de melhoria. Ele deve receber uma linha do dataset e gerar pelo menos 3 recomendações. Elas devem ser acionáveis e quantificadas, levar em conta o contexto (plataforma, categoria e outros atributos) e vir ordenadas por impacto. O sistema deve funcionar de verdade.

## Resposta curta

O motor funciona como um **simulador de "e se"**. Ele pega o vídeo, muda uma coisa (por exemplo, acrescenta um gancho) e pergunta ao modelo da Parte 2 qual seria a nova nota. A diferença entre a nota nova e a atual é o ganho estimado. Ele faz isso para cada melhoria possível e entrega as três de maior ganho, em ordem.

Quando a Parte 1 tem um padrão confiável, o motor acrescenta também o efeito na métrica que aquela campanha quer mover, na rede dela: os cliques para uma campanha de tráfego, a retenção para uma campanha feita para ser vista.

Um exemplo real, de uma campanha de tráfego no LinkedIn que o modelo nunca tinha visto:

> 1. Adicionar um gancho nos 3 primeiros segundos pode aumentar a nota Klike em ~18 pontos (de 49 para 67) e o CTR em ~+133% no LinkedIn.
> 2. Mostrar um rosto humano pode aumentar a nota em ~12 pontos (de 49 para 61).
> 3. Rodar o criativo também para quem já conhece a marca (retargeting) pode aumentar a nota em ~4 pontos (de 49 para 54).

As 100 campanhas de teste receberam 3 recomendações cada. E o motor é coerente: as campanhas em que ele vê mais espaço para melhorar são justamente as que têm nota real mais baixa.

Para usar, basta um comando com o código da campanha:

```bash
python -m src.recomendacoes KLK-0123
```

## O que fiz, passo a passo

**1. Preparo a campanha.** O motor aceita a linha tal como está no arquivo original e aplica a mesma limpeza das Partes 1 e 2.

**2. Listo as melhorias possíveis**, ou seja, só o que o vídeo ainda não faz:

- acrescentar gancho, rosto, chamada para ação ou legenda;
- levar o texto na tela para a quantidade média;
- trocar parte da música por voz;
- mostrar o anúncio também para quem já conhece a marca;
- mudar para um formato que a rede já usa bastante.

**3. Calculo o ganho de cada uma.** O modelo da Parte 2 prevê a nota do vídeo como ele é e, de novo, com a mudança. Descarto as mudanças que não sobem a nota.

**4. Acrescento o efeito na métrica da campanha**, buscado na tabela que a Parte 1 salvou para cada rede social. O número só aparece se o padrão for confiável e tiver sido medido em pelo menos 15 vídeos de cada lado.

**5. Ordeno pelo ganho na nota** e fico com as três primeiras.

**6. Cuido dos vídeos que já estão quase perfeitos.** Se um vídeo já faz quase tudo certo, não sobram três melhorias com base nos dados. Nesse caso, o motor completa a lista com o que o vídeo deve **manter**, também com número. Por exemplo: "manter o texto em quantidade média: passar para muito texto custaria ~15 pontos".

**7. Conferi o motor de quatro jeitos:** refazendo a conta à mão para uma campanha, rodando uma campanha de cada rede, simulando o mesmo vídeo nas três redes e rodando as 100 campanhas de teste.

## Por que fiz assim

**Usar o modelo da Parte 2 como simulador.** Ele só usa o que se sabe antes de postar, então as recomendações valem antes de o vídeo ir ao ar. E, por ser uma regressão linear, o ganho de cada mudança é o próprio efeito dela em pontos, mantendo todo o resto igual.

**Mostrar a métrica do objetivo, e não sempre os cliques.** A Parte 1 mostrou que cada tipo de campanha tem a sua métrica de sucesso. Nas campanhas de venda e de instalação de app, o vídeo não muda o custo por venda. Por isso o motor mostra o efeito nos cliques, a etapa anterior.

**Mostrar só padrões confiáveis.** Um efeito fraco pode até apontar para o lado contrário da nota. Por exemplo, a chamada para ação sobe a nota, mas, no engajamento do TikTok, o número aparecia negativo por acaso. Mostrar isso confundiria quem lê.

**Ordenar pela nota.** É o que a Klike quer prever, resume o caminho inteiro do cliente e vale para todo tipo de campanha.

**Não recomendar mudar a duração.** O enunciado dá como exemplo "reduzir de 45 para 20 segundos". Nestes dados, porém, não existe duração ideal (Parte 1), e a duração vale quase nada na nota (Parte 2). Recomendar isso seria inventar.

**Completar com "manter", em vez de inventar melhorias.** Um motor que sempre encontra três coisas para mudar, mesmo num vídeo ótimo, perde a confiança do usuário. Dizer o que não mexer, e quanto custaria mexer, continua sendo útil e honesto.

## O que descobri

**Nas 100 campanhas de teste, todas receberam 3 recomendações.** 81 receberam três melhorias, 15 receberam duas, 3 receberam uma e 1 não recebeu nenhuma. As que tinham menos de três melhorias foram completadas com "manter".

**A primeira recomendação foi, na maioria das vezes, um dos maiores efeitos das Partes 1 e 2:** acrescentar um gancho (em metade das campanhas), mostrar um rosto, reduzir o texto ou colocar legenda.

**O motor leva o contexto em conta.** Simulei o mesmo vídeo, com muita música e sem gancho, nas três redes.

- No TikTok, aparece a recomendação de trocar música por voz (+7 pontos). Nas outras redes, ela não aparece, porque lá a música não pesa.
- O efeito do gancho nos cliques muda de rede para rede: +53% no Meta, +83% no TikTok e +133% no LinkedIn.
- A recomendação de reduzir o texto vem com o efeito nos cliques só no Meta, a única rede em que esse efeito é confiável.

**O motor é coerente.** Dividi as 100 campanhas em quatro grupos, pelo ganho total que o motor vê. No grupo com menos espaço para melhorar, a nota real mediana é 80. No grupo com mais espaço, é 48. Ou seja, nas campanhas que nunca viu, o motor aponta problemas justamente onde a nota é baixa.

## Limites

**É associação, não causa.** O motor diz que vídeos parecidos com gancho têm nota cerca de 18 pontos maior. Só um teste A/B provaria que acrescentar o gancho faz a nota subir.

**Cada ganho é calculado sozinho.** Fazer várias mudanças juntas tende a somar os ganhos, mas a nota não passa de 100.

**"Tem gancho" não diz se o gancho é bom.** O motor recomenda que o vídeo tenha o atributo, não como executá-lo bem.

**A categoria do produto e a idade do público quase não entram.** A categoria saiu do modelo porque repete o objetivo, e a Parte 1 não encontrou padrão por idade.

**Os dados são simulados.** Com dados reais, os ganhos devem ser menores e menos limpos.
