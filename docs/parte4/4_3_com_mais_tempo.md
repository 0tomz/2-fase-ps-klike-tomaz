# Pergunta 4.3: o que mais eu faria com mais tempo?

## Pergunta

O que mais você faria se tivesse mais tempo? Que análises, experimentos ou melhorias no engine ficaram de fora?

## Resposta curta

A primeira coisa seria **provar causa**. Em todas as partes, a mesma ressalva se repetiu: os dados mostram o que anda junto, não o que causa. "Vídeos com gancho têm nota maior" ainda não é o mesmo que "colocar um gancho aumenta a nota". Só um experimento resolve isso.

Depois, eu faria o modelo dizer **o quanto confia em cada previsão** ("nota entre 60 e 76", e não só "68"). Ensinaria o motor a **recomendar combinações de mudanças e a pesar o esforço de cada uma**. E repetiria tudo com **dados reais**, que provavelmente vão mostrar efeitos menores e menos limpos que os deste conjunto simulado.

## Experimentos

O experimento mais importante seria um **teste A/B** dos atributos principais. O mesmo anúncio é feito em duas versões, idênticas exceto pelo gancho, e cada versão é mostrada a um público sorteado. Como o sorteio garante que os públicos são parecidos, qualquer diferença nos cliques ou na retenção vem do gancho. Faria o mesmo com o rosto, com a quantidade de texto e com a voz no TikTok.

Faria também um teste A/B do próprio motor: metade dos clientes recebe recomendações, a outra metade não, e depois se comparam os resultados das campanhas. Esse teste responde à pergunta que mais importa para o produto: seguir as recomendações melhora a campanha?

Por fim, registraria se cada recomendação foi seguida e o que aconteceu depois. Com o tempo, isso mostra o ganho real de cada recomendação, e não só o estimado.

## Análises que ficaram de fora

**O limite do CTR.** A Parte 1 mostrou que os melhores vídeos ficaram presos no limite de 15% de cliques, o que faz o efeito do gancho parecer menor do que é. Existem métodos feitos para dados cortados num limite, que estimam o valor que passou dele.

**A retenção segundo a segundo.** Com ela, daria para ver em que momento as pessoas abandonam o vídeo e recomendar a duração com base nos dados. Hoje só temos o tempo médio assistido, e a Parte 1 não encontrou duração ideal.

**Combinações com mais dados.** Com 400 vídeos, e só 66 no LinkedIn, quase nenhuma combinação (gancho por rede, rosto por idade, texto por formato) passou no teste da Parte 2. Com mais vídeos, poderiam aparecer regras próprias de cada rede ou de cada público.

**O efeito do tempo.** As campanhas cobrem só 2024. Com mais anos, daria para ver se um estilo de vídeo "cansa" o público com o tempo.

**Diferenças entre clientes.** O que funciona para uma marca de software pode não funcionar para uma loja virtual. Com dados suficientes, cada cliente poderia ter ajustes próprios.

## Melhorias no modelo

**Uma nota com margem de erro.** Hoje o modelo diz "68". O ideal seria "68, provavelmente entre 60 e 76", aprendendo com os próprios erros nas avaliações. Para o usuário, saber o tamanho da incerteza é tão útil quanto o número.

**Um meio-termo entre um modelo único e um modelo por rede.** A Parte 2 mostrou que um modelo só para o LinkedIn erra mais, por falta de dados. Um meio-termo deixaria cada rede ter seus próprios efeitos, mas puxados para o efeito geral quando a rede tem poucos vídeos.

**Uma avaliação ainda mais rigorosa dos modelos concorrentes.** Na Parte 2, os ajustes da Random Forest e da rede neural foram escolhidos nas mesmas provas que mediram o erro delas, o que favorece um pouco os dois. Uma avaliação em duas camadas evitaria isso. Não mudaria a escolha da regressão linear, que não tem ajuste, mas deixaria a comparação ainda mais justa.

**Explicação vídeo a vídeo.** Além do "e se" da Parte 3, mostraria quanto cada atributo contribuiu para a nota daquele vídeo específico ("este vídeo perde 15 pontos por excesso de texto").

**Modelos para outras métricas**, como cliques ou retenção, para clientes que querem otimizar uma métrica específica, e não a nota.

## Melhorias no motor de recomendações

**Recomendar combinações.** Hoje cada mudança é calculada sozinha. O motor poderia mostrar o efeito de várias juntas. No exemplo do LinkedIn da Parte 3, acrescentar o gancho e reduzir o texto levaria a nota de 49 para cerca de 82.

**Pesar o esforço.** Colocar legenda é barato; regravar o vídeo com uma pessoa é caro. Ordenar por ganho dividido pelo esforço (que o próprio time de marketing informaria) deixaria as recomendações mais práticas.

**Mostrar a margem de cada recomendação.** O gancho, por exemplo, vale entre 17,4 e 18,4 pontos nas 15 provas da Parte 2, um número firme. A música no TikTok varia de 8 a 15 pontos, um número mais incerto. O usuário deveria ver essa diferença.

**Respeitar as regras de cada marca.** Não sugerir rosto para uma marca que só usa animação, nem voz para um canal que não usa narração.

**Recomendar a partir do próprio vídeo**, com as medidas da pergunta 4.1: "a marca só aparece no segundo 12; antecipe para antes do segundo 5".

**Mostrar exemplos**: três vídeos parecidos que foram bem, usando a "impressão digital" de vídeo da pergunta 4.1.

## Em que ordem eu faria

Primeiro, o teste A/B do gancho, porque ele prova (ou derruba) a recomendação mais importante de todo o trabalho. Segundo, os dados reais e o monitoramento, para saber quanto o modelo piora fora dos dados simulados. Terceiro, a margem de erro em cada previsão. Por último, as medidas tiradas do vídeo.

A lógica é que, antes de sofisticar o modelo, é preciso saber duas coisas: se as recomendações realmente causam a melhora e quão bom o modelo é com dados reais. Sofisticar antes disso seria aperfeiçoar algo que ainda não foi validado.
