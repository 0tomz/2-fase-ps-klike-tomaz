# Parte 4: visão de produto

As três perguntas desta parte são abertas. Respondo cada uma apoiado no que as Partes 1 a 3 mostraram, porque as melhores ideias para o futuro vêm justamente dos limites que o trabalho encontrou.

## 4.1 Se eu tivesse o vídeo original, que features eu extrairia?

> Se você tivesse acesso ao vídeo original (não só metadados), que features adicionais você extrairia para melhorar o modelo e as recomendações?

Hoje o modelo sabe **se** o vídeo tem gancho, rosto ou texto, mas não sabe **se eles são bons**. Para ele, um gancho fraco e um gancho excelente valem exatamente o mesmo. É aí que provavelmente está o terço da nota que o modelo ainda não consegue explicar. A Parte 2 reforçou essa leitura: a curva de aprendizado mostrou que o erro para de cair depois de uns 200 vídeos. Ou seja, o que falta não são mais vídeos do mesmo tipo, e sim informações melhores sobre cada vídeo.

Com o vídeo em mãos, eu trocaria os "sim ou não" por medidas de **como** o vídeo foi feito, em cinco frentes:

1. o que acontece nos 3 primeiros segundos (o gancho);
2. quanto o rosto aparece;
3. quanto espaço o texto ocupa na tela;
4. o que se ouve, fala ou música;
5. quando a marca aparece, e o estilo do vídeo.

**O gancho** foi o atributo mais forte de todo o trabalho, então é por ele que eu começaria. Mediria quanto tempo o vídeo leva para mudar de cena e quanto a imagem se mexe no começo, porque um começo parado tende a fazer a pessoa rolar o feed. Mediria também o que aparece no primeiro quadro (um rosto, um texto ou o produto), o que diz que tipo de gancho é aquele. E transcreveria a primeira frase falada. A **transcrição automática** transforma a fala em texto, e com ela dá para saber se o vídeo começa com uma pergunta, um número ou uma promessa ("3 erros que você comete..."), os ganchos clássicos.

**O rosto** hoje é só "tem ou não tem". Eu mediria por quanto tempo ele aparece, se a pessoa olha para a câmera, o que dá a sensação de uma conversa direta, e a expressão dela. Assim o modelo separaria um rosto que prende a atenção de um rosto que só passa pela tela.

**O texto na tela** tem um ponto ideal no meio (Partes 1 e 2), mas hoje está resumido em três níveis: pouco, médio e muito. Com o vídeo, eu usaria o **OCR**, uma técnica que lê o texto de uma imagem como um scanner lê um documento. Com ele, contaria as palavras, mediria quanto da tela o texto ocupa e por quanto tempo cada frase fica visível. Também veria se o texto cai na parte de baixo da tela, que no TikTok e no Reels fica escondida atrás dos botões do aplicativo. Com isso, o motor poderia dizer algo muito mais útil que "reduza o texto": "o texto ocupa 40% da tela; reduza para 20%".

**O áudio** hoje é um único número que mistura música e voz. A Parte 2 mostrou que a voz importa no TikTok, então eu mediria a fala e a música segundo a segundo. Mediria também a velocidade da narração, se a chamada para ação é dita em voz alta e em que momento, e se a legenda acompanha de fato o que é falado. Esta última medida ainda resolveria um problema de hoje: em 9% dos vídeos, não se sabe se há legenda.

**A marca e o estilo** fecham a lista. O segundo em que a marca aparece provavelmente importa: cedo demais parece propaganda, e tarde demais ninguém lembra. O tempo em que o produto aparece deve pesar nas campanhas de venda. O ritmo da edição e a "cara" do vídeo (feito no celular ou produzido em estúdio) também contam, principalmente no TikTok, onde o estilo nativo costuma funcionar melhor. A duração e o formato seriam medidos direto no arquivo, o que acabaria com as durações vazias (7,5% hoje). Por fim, usaria uma espécie de "impressão digital" do vídeo: uma lista de números gerada por um modelo de imagem já treinado, em que vídeos parecidos recebem números parecidos. Ela permitiria perguntar "este vídeo se parece com os campeões da categoria?" e mostrar exemplos parecidos que foram bem.

Todas essas medidas existem **antes** de o vídeo ir ao ar, então mantêm a promessa do Klike. Elas melhorariam o modelo, que passaria a distinguir um gancho bom de um ruim, justamente onde ele mais erra hoje: nos vídeos muito bons e muito ruins. E melhorariam o motor, que passaria a apontar **onde** mexer, com frases como estas:

- "a marca só aparece no segundo 12; os vídeos com nota alta a mostram antes do segundo 5";
- "não há fala nos primeiros 4 segundos; no TikTok, colocar voz no começo deve subir a nota".

Começaria pelas medidas mais baratas e mais ligadas ao que já funciona: o começo do vídeo, o tempo de rosto, a área do texto e a mistura de fala e música. Com dois cuidados. O primeiro é não encher um modelo de 400 vídeos com dezenas de colunas novas, o que o faria decorar em vez de aprender; cada medida passaria pelo mesmo teste da Parte 2 e só entraria se reduzisse o erro em vídeos que o modelo não viu. O segundo é a privacidade: rostos e vozes são dados pessoais, protegidos pela LGPD, então eu guardaria só as medidas, e não as imagens.

## 4.2 Como eu colocaria o motor em produção?

> Como você colocaria o seu Recommendations Engine em produção? Pense em arquitetura, escalabilidade e como ele se integraria a um produto real.

A experiência do usuário seria simples: ele sobe o vídeo no Klike **antes de publicar** e, em segundos, recebe a nota prevista e as três recomendações. Por trás disso, eu montaria o sistema em cinco peças:

1. um serviço de recomendações, que recebe os pedidos e devolve as respostas;
2. uma fila e computadores próprios para analisar os vídeos;
3. um banco que guarda as medidas de cada vídeo;
4. um retreino periódico com os resultados reais das campanhas;
5. um monitoramento que avisa quando o modelo começa a errar mais.

**O serviço de recomendações** é o balcão de atendimento. Ele recebe o vídeo e os dados da campanha, chama o modelo e devolve a nota e as recomendações. Na prática, é um programa que fica no ar recebendo pedidos pela internet (uma **API**) e usa o mesmo modelo salvo na Parte 2 e a mesma função de recomendação da Parte 3. Calcular a nota é leve: uma regressão linear responde em milésimos de segundo.

**A fila e os computadores de vídeo** existem porque a outra parte do trabalho, analisar o vídeo com as medidas da pergunta 4.1, é pesada. Os vídeos entram numa fila, como as senhas de um banco, e computadores com placa de vídeo os atendem um a um. Quando a fila cresce, ligam-se mais computadores, como abrir mais caixas num banco cheio. Assim nenhum vídeo se perde num pico de uso, e o custo acompanha a demanda.

**O banco de medidas** guarda o resultado da análise de cada vídeo. Se o mesmo vídeo for enviado de novo, ele não é analisado outra vez. Isso, junto com analisar primeiro só os 3 primeiros segundos e o áudio (onde está o gancho), é o que mantém o custo sob controle.

**O retreino periódico** é a peça que faz o produto aprender. Depois que a campanha roda, os resultados reais voltam das plataformas (Meta, TikTok, LinkedIn). Todo mês, o modelo é treinado de novo com esses dados, usando a mesma avaliação honesta da Parte 2. O modelo novo só substitui o antigo se errar menos em campanhas recentes que nenhum dos dois viu. Cada versão fica guardada, e toda recomendação registra qual versão a gerou; se algo der errado, volta-se para a anterior.

**O monitoramento** compara a nota prevista com o resultado real quando ele chega, e avisa se o erro subir ou se os vídeos mudarem de perfil (um formato novo, por exemplo).

No produto, o uso principal seria antes de publicar, com um botão de simulação para o usuário ligar e desligar mudanças e ver a nota mudar na hora. É o mesmo "e se" da Parte 3, na tela. Agências que testam muitas versões de um anúncio poderiam mandar 50 variações de uma vez e receber a lista ordenada da melhor para a pior. Essa é a maior força do modelo: na Parte 2, ele acertou 3 de cada 4 dos melhores vídeos. Para não deixar ninguém esperando, eu ofereceria duas velocidades: uma resposta rápida, só com os dados da campanha, em segundos; e uma completa, com a análise do vídeo, em alguns minutos. Se a análise do vídeo falhar, o cliente ainda recebe a resposta rápida.

Eu não construiria tudo de uma vez. Primeiro, colocaria no ar o motor que já existe, registrando cada recomendação dada. Depois, ligaria a coleta dos resultados reais e o retreino, para o modelo aprender com dados de verdade em vez dos simulados. Só então acrescentaria a análise de vídeo, quando já desse para medir se ela realmente diminui o erro.

Os riscos que eu vigiaria são quatro:

- **o mundo muda:** as plataformas mudam seus algoritmos, e o modelo de hoje não vale para sempre;
- **dados reais são mais bagunçados que os simulados,** então o erro de cerca de 7 pontos provavelmente vai piorar, e a primeira tarefa em produção é medir quanto;
- **o sistema pode se enganar sozinho:** se todos os clientes seguirem as recomendações, todos os vídeos passam a ter gancho, e o modelo fica sem vídeos sem gancho para comparar. Manter uma pequena parte dos vídeos sem recomendação, e fazer testes A/B, mantém o modelo honesto;
- **os dados são dos clientes:** os vídeos e os resultados de cada um precisam ficar separados, com regras claras de uso, como exige a LGPD.

## 4.3 O que eu faria com mais tempo?

> O que mais você faria se tivesse mais tempo? Que análises, experimentos ou melhorias no engine ficaram de fora?

Em ordem de prioridade, eu faria:

1. testes A/B para provar que as recomendações causam a melhora;
2. a mesma análise com dados reais, acompanhando o erro do modelo;
3. uma margem de erro em cada previsão e em cada recomendação;
4. recomendações combinadas e pesadas pelo esforço de cada mudança;
5. as medidas tiradas do próprio vídeo (pergunta 4.1).

**Os testes A/B vêm primeiro** porque a mesma ressalva apareceu em todas as partes: os dados mostram o que anda junto, não o que causa. "Vídeos com gancho têm nota maior" ainda não é o mesmo que "colocar um gancho aumenta a nota". Num teste A/B, o mesmo anúncio é feito em duas versões, idênticas exceto pelo gancho, e cada versão é mostrada a um público sorteado. Como o sorteio garante públicos parecidos, qualquer diferença vem do gancho. Faria o mesmo com o rosto, o texto e a voz no TikTok, e depois testaria o próprio motor: metade dos clientes recebe recomendações e a outra metade não. Esse último teste responde à pergunta que mais importa para o produto: seguir as recomendações melhora a campanha?

**Os dados reais vêm em segundo** porque este conjunto é simulado. A nota parece ter sido gerada somando os efeitos de cada atributo, o que explica por que um modelo tão simples foi tão bem. Antes de sofisticar qualquer coisa, eu precisaria saber quão bom o modelo é no mundo real.

**A margem de erro** mudaria a forma de apresentar os resultados. Hoje o modelo diz "nota 68". O ideal seria "68, provavelmente entre 60 e 76". O mesmo vale para as recomendações: o gancho vale entre 17,4 e 18,4 pontos nas 15 provas da Parte 2, um número firme, enquanto a música no TikTok varia de 8 a 15, um número mais incerto. O usuário deveria ver essa diferença.

**As recomendações combinadas** tornariam o motor mais prático. Hoje cada mudança é calculada sozinha. O motor poderia mostrar o efeito de várias juntas: no exemplo do LinkedIn da Parte 3, acrescentar o gancho e reduzir o texto levaria a nota de 49 para cerca de 82. E poderia pesar o esforço: colocar legenda é barato, regravar o vídeo com uma pessoa é caro. Ordenar pelo ganho dividido pelo esforço, que o próprio time de marketing informaria, deixaria as sugestões mais realistas.

**As medidas do vídeo** vêm por último não por serem menos importantes, mas porque só fazem sentido depois das anteriores. Sofisticar o modelo antes de saber se as recomendações causam a melhora, e quão bom ele é com dados reais, seria aperfeiçoar algo que ainda não foi validado.

Algumas análises menores também ficaram de fora e entrariam no caminho:

- tratar o limite de 15% no CTR, que faz o efeito do gancho nos cliques parecer menor;
- usar a retenção segundo a segundo para, aí sim, recomendar a duração ideal de cada rede;
- procurar combinações (gancho por rede, rosto por idade) quando houver mais vídeos, principalmente do LinkedIn;
- criar um meio-termo entre um modelo único e um modelo por rede, que deixe cada rede ter seus próprios efeitos, puxados para o efeito geral quando ela tem poucos dados.
