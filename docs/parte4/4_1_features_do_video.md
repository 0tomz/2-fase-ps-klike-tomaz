# Pergunta 4.1: que features eu extrairia do vídeo original?

## Pergunta

Se você tivesse acesso ao vídeo original (não só metadados), que features adicionais você extrairia para melhorar o modelo e as recomendações?

## Resposta curta

Hoje o modelo sabe **se** o vídeo tem gancho, rosto ou texto, mas não sabe **se eles são bons**. Um gancho fraco e um gancho excelente contam igual. É aí que provavelmente está o terço da nota que o modelo não consegue explicar.

A Parte 2 também mostrou que mais vídeos do mesmo tipo ajudariam pouco: o erro para de cair depois de uns 200 vídeos. O que falta são informações melhores sobre cada vídeo.

Com o vídeo em mãos, eu trocaria os "sim ou não" por medidas de **como** o vídeo foi feito:

- quanto tempo leva até a primeira mudança de cena;
- quanto tempo o rosto aparece;
- quanto da tela o texto ocupa;
- em que segundo a marca aparece;
- o que é falado.

Isso melhoraria o modelo e tornaria as recomendações muito mais precisas. Em vez de "adicione um gancho", o motor poderia dizer "o vídeo só muda de cena no segundo 4; antecipe para o segundo 1".

## As features que eu extrairia

Todas existem antes de o vídeo ir ao ar, então mantêm a promessa do Klike de avaliar antes de postar.

**Sobre o gancho**, o atributo mais forte de todo o trabalho, mediria o que acontece nos primeiros 3 segundos:

- quanto tempo até o primeiro corte de cena;
- quanto a imagem se mexe;
- se o primeiro quadro já mostra um rosto, um texto ou o produto;
- qual é a primeira frase falada. Uma pergunta, um número ou uma promessa ("3 erros que você comete...") são ganchos clássicos;
- se há som logo no começo.

Para ler o texto que aparece na imagem, existe uma técnica chamada **OCR**, que faz o que um scanner faz com um documento. Para saber o que é falado, existe a **transcrição automática**, que transforma a fala em texto.

**Sobre o rosto**, trocaria o "tem rosto" por quanto tempo o rosto aparece, se a pessoa olha para a câmera (o que dá a sensação de uma conversa) e a expressão dela.

**Sobre o texto na tela**, que tem um ponto ideal no meio, trocaria os três níveis (pouco, médio, muito) por números: quantas palavras, quanto da tela o texto ocupa e por quanto tempo cada texto fica visível. Mediria também se o texto cai na parte de baixo da tela, que no TikTok e no Reels fica escondida atrás dos botões do aplicativo. Com isso, o motor poderia dizer "o texto ocupa 40% da tela; reduza para 20%".

**Sobre o áudio**, trocaria o número único de música/voz por uma medida segundo a segundo, já que a Parte 2 mostrou que a voz importa no TikTok. Mediria também a velocidade da fala, se a chamada para ação é falada e em que momento, e se a legenda acompanha de fato o que é dito. Isso também resolveria um problema de hoje: em 9% dos vídeos, não se sabe se há legenda.

**Sobre a marca e o estilo**, mediria:

- em que segundo a marca ou o logotipo aparecem (cedo demais pode parecer propaganda; tarde demais, ninguém lembra);
- quanto tempo o produto aparece, o que deve importar para as campanhas de venda;
- o ritmo da edição;
- se o vídeo tem cara de "feito no celular" ou de produção profissional, porque no TikTok o estilo nativo costuma funcionar melhor;
- a duração e o formato reais, medidos no arquivo. Hoje, 7,5% das durações estão vazias.

**Sobre o vídeo como um todo**, usaria uma "impressão digital" do conteúdo: uma lista de números gerada por um modelo de imagem já treinado, em que vídeos parecidos recebem números parecidos. Ela permitiria responder "este vídeo se parece com os campeões da categoria?" e mostrar exemplos ("veja três vídeos parecidos que foram bem").

## Como isso melhora o modelo e o motor

O modelo deixaria de tratar todo gancho como igual. Com medidas contínuas, ele conseguiria separar um gancho bom de um ruim. Esse é o caminho para reduzir o erro de cerca de 7 pontos, principalmente nos vídeos muito bons e muito ruins, que é onde o modelo mais erra hoje.

O motor apontaria **onde** mexer no vídeo:

- "a marca só aparece no segundo 12; os vídeos com nota alta a mostram antes do segundo 5";
- "não há fala nos primeiros 4 segundos; no TikTok, colocar voz no começo deve subir a nota".

E, com a curva de retenção segundo a segundo, que as plataformas informam, daria finalmente para responder onde as pessoas abandonam o vídeo e recomendar a duração com base nos dados. Hoje isso não é possível, porque só temos o tempo médio assistido.

## Por que essas, e por onde eu começaria

Escolhi essas features porque atacam os limites que o próprio trabalho mostrou: o "tem gancho" que não diz se o gancho é bom, o texto em só três níveis, a música e a voz resumidas num número e a legenda desconhecida.

Começaria pelas mais baratas de extrair e mais ligadas ao que já funciona: o corte e o movimento nos 3 primeiros segundos, o tempo de rosto, a área do texto e a mistura de fala e música. A "impressão digital" do vídeo viria depois.

## Riscos e cuidados

**Muitas informações para poucos vídeos.** Com 400 vídeos, dezenas de colunas novas fariam o modelo decorar os exemplos em vez de aprender. Cada feature nova passaria pelo mesmo teste da Parte 2: entra só se reduzir o erro em vídeos que o modelo não viu.

**Custo.** Analisar vídeo exige computadores com placa de vídeo, e isso é caro. Por isso, extrairia só o necessário e guardaria o resultado, como explico na pergunta 4.2.

**Associação, não causa.** "Vídeos que cortam no 1º segundo têm nota maior" ainda precisaria de um teste A/B antes de virar regra.

**Privacidade.** Rostos e vozes são dados pessoais, protegidos pela LGPD. Guardaria só as medidas, não as imagens.
