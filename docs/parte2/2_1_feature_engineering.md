# Pergunta 2.1: quais features usar, e por quê?

Notebook: [`notebooks/parte2/2_1_feature_engineering.ipynb`](../../notebooks/parte2/2_1_feature_engineering.ipynb). Funções reaproveitadas: [`src/features.py`](../../src/features.py).

## Pergunta

Feature engineering: quais features você escolheu e por quê? Criou alguma feature nova?

Uma **feature** é cada informação que o modelo recebe para fazer a previsão, a "pista" que ele usa para adivinhar a nota.

## Resposta curta

A Klike promete dar a nota **antes** de o vídeo ir ao ar. Isso decidiu tudo. O modelo principal, que chamei de **Modelo A (pré-lançamento)**, só pode usar o que existe nesse momento:

- as oito características do vídeo: gancho, rosto, chamada para ação, legenda, formato, quantidade de texto na tela, duração e mistura de música e voz;
- quatro informações da campanha: a rede social, o objetivo, a idade do público e se ela mira quem já conhece a marca.

Fiz também um **Modelo B (completo)**, que recebe ainda os resultados que só aparecem depois de o anúncio rodar (cliques, engajamento, retenção, conversões). Ele não serve para o produto, mas funciona como régua: mostra quanto da nota o vídeo sozinho já explica.

Criei uma feature nova que ficou no modelo: a **música no TikTok**, porque a Parte 1 mostrou que lá vídeo sem voz perde pontos. Testei outras ideias, e nenhuma melhorou a previsão. Também tirei uma coluna que repetia outra (a categoria do produto, que quase define o objetivo da campanha).

Na avaliação, o Modelo A erra em média 6,9 pontos de nota, e o Modelo B, 5,6.

## O que fiz, passo a passo

**1. Usei a mesma divisão e a mesma limpeza da Parte 1**, com uma mudança. Os valores vazios que a Parte 1 preencheu voltaram a ficar vazios, e quem preenche agora é o próprio modelo, durante o treino (explico no passo 3).

**2. Decidi o que o modelo pode ver.** Usar uma informação que só existe depois de postar seria **vazamento de dados**: o modelo pareceria ótimo nos testes e não funcionaria no produto, como um aluno que tira 10 porque viu o gabarito. Por isso o Modelo A não recebe nenhum resultado da campanha, e o notebook confere isso automaticamente. Também ficaram de fora:

- o código da campanha, que não diz nada sobre o vídeo;
- a data, porque a Parte 1 não achou efeito da época do ano;
- os números de volume, como gasto e impressões, que dependem do orçamento e não do vídeo.

**3. Preparei cada tipo de informação**, porque o modelo só entende números:

- o que é sim/não vira 1 ou 0;
- o que é texto (o formato, por exemplo) vira várias perguntas de sim/não: "é vertical?", "é horizontal?". Um dos níveis fica de fora e serve de **referência**, e o modelo mede os outros em relação a ele. Para o formato, a referência é o quadrado, então o resultado se lê como "vertical em comparação com quadrado";
- os números vazios são preenchidos com a mediana, e uma marcação extra diz que o valor estava vazio;
- por fim, todos os números são colocados na mesma escala, como converter reais, dólares e euros para uma moeda só antes de comparar.

Tudo isso fica numa "linha de montagem" (o **Pipeline**) que aprende as medidas só com os dados de treino de cada rodada, e depois as aplica igual em qualquer vídeo novo.

**4. Testei cada ideia de feature nova com e sem ela.** O teste é a **validação cruzada**: os 400 vídeos de treino são divididos em 5 partes, o modelo aprende com 4 e é avaliado na 5ª, que ele não viu, e isso se repete até cada parte ter sido a prova uma vez. Repeti tudo 3 vezes com sorteios diferentes, o que dá 15 provas. É como estudar com 15 simulados diferentes em vez de um só. Todas as ideias fizeram as mesmas 15 provas, para a comparação ser justa.

**5. Defini uma regra para aceitar uma feature:** ela precisa reduzir o erro em pelo menos 1%. Se não muda nada, decide a interpretação: fica se ajuda a explicar o resultado, e sai se só complica.

**6. Conferi se as features finais repetem informação**, num mapa de calor da correlação entre elas.

## Por que fiz assim

**Dois modelos, e não um.** Se o Modelo B fosse muito melhor que o A, o produto teria um problema sério: a nota antes de postar seria pouco útil. Medir os dois responde a essa dúvida.

**Preencher os vazios durante o treino.** Na Parte 1, a mediana usada para preencher vinha de todos os 400 vídeos. Numa avaliação, isso deixaria os vídeos de prova influenciarem o preenchimento, um pequeno vazamento. Preenchendo dentro de cada rodada, a avaliação fica honesta. O custo é desprezível: o erro sobe de 6,92 para 6,95 pontos.

**Colocar tudo na mesma escala.** A rede neural, um dos modelos testados no notebook 2.2, aprende mal quando uma coluna está em segundos e outra entre 0 e 1. Na regressão linear, a escala não muda a previsão, mas deixa o peso das colunas comparável.

## O que descobri

**Nenhuma ideia nova reduziu o erro em 1% ou mais.** O Modelo A já capta quase tudo com as informações originais.

**O texto na tela precisa ser tratado como categoria.** Tratado como uma escala de 0 (pouco) a 2 (muito), o erro sobe 20%, e piora em todas as 15 provas. Faz sentido: a Parte 1 mostrou que o melhor é o meio, e uma escala força uma linha reta, como se "mais texto" fosse sempre melhor ou sempre pior.

**A categoria do produto saiu.** Tirá-la não perde nada (o erro até cai 0,5%), porque ela repete o objetivo da campanha. Fiquei com o objetivo porque é a escolha que o time faz em cada campanha.

**A música no TikTok ficou**, mesmo sem passar da régua de 1% (o erro cai 0,2%). Ela não atrapalha, confirma a Parte 1 e dá ao motor de recomendações da Parte 3 uma regra própria do TikTok: "coloque voz".

**A contagem de boas práticas** (gancho + rosto + chamada para ação + legenda) não muda nada na regressão linear, que já tem as quatro colunas separadas e as soma sozinha. Na Random Forest, um modelo feito de árvores de perguntas, ela reduz o erro em 4,5%, e por isso entrou só lá.

**As outras ideias saíram:** o gancho por rede social, curvas para duração e música, e faixas de duração. Nenhuma melhorou a previsão nem explicou algo novo.

**As features quase não repetem informação.** O único par muito parecido é "é TikTok" e "música no TikTok", o que é esperado, porque a segunda só existe no TikTok. Por isso os dois pesos devem ser lidos juntos.

## Limites

Como nenhuma ideia passou da régua de 1%, as decisões de manter ou tirar pesaram mais a interpretação do que o erro. A música no TikTok ficou por uma escolha que eu defendo pela Parte 1 e pela Parte 3, não pelo número. E os dados são simulados: a nota parece ter sido gerada somando os efeitos de cada atributo, o que explica por que curvas e combinações quase não ajudam.
