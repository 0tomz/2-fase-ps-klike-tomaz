# 2.1 Quais features usar, e por quê?

> Pergunta do case: feature engineering: quais features você escolheu e por quê? Criou alguma feature nova?
>
> Notebook: [`2_1_feature_engineering.ipynb`](../../notebooks/parte2/2_1_feature_engineering.ipynb) · Código: [`src/features.py`](../../src/features.py)

## Resposta curta

Uma **feature** é cada informação que o modelo recebe para prever a nota, a "pista" que ele usa. Como o Klike promete avaliar o vídeo **antes** de ele ir ao ar, o modelo principal (o **Modelo A**) só recebe o que existe nesse momento. São 8 características do vídeo (gancho, rosto, chamada para ação, legenda, formato, texto na tela, duração e mistura de música e voz) e 4 da campanha (rede social, objetivo, idade do público e retargeting). Criei uma feature nova que ficou: a **música no TikTok**. Tirei uma que repetia outra: a categoria do produto, que quase define o objetivo da campanha. Com isso, o Modelo A erra em média 6,9 pontos de nota na avaliação.

## Por que isso importa

O modelo julga o vídeo pelo que o time decide antes de publicar, e não pelos resultados. É isso que permite usá-lo antes de gastar a verba. Para medir o quanto se perde com essa restrição, fiz também um **Modelo B**, que recebe ainda os resultados da campanha (cliques, engajamento, retenção, conversões). Ele erra 5,6 pontos, pouco mais de 1 ponto a menos. Ou seja, o vídeo sozinho já explica quase tudo o que a nota mede.

## Como cheguei lá

**Evitei o vazamento de dados.** Usar no modelo uma informação que só existe depois de postar faria ele parecer ótimo nos testes e não funcionar no produto, como um aluno que tira 10 porque viu o gabarito. Por isso, nenhum resultado da campanha entra no Modelo A, e o notebook confere isso automaticamente. Também ficaram de fora o código da campanha, a data (a pergunta 1.1 não achou efeito da época do ano) e os números de volume, como gasto e impressões, que dependem do orçamento e não do vídeo.

**Preparei cada informação dentro de uma "linha de montagem"** (o **Pipeline**), que aprende tudo só com os dados de treino e aplica igual a qualquer vídeo novo. Ela transforma sim/não em 1 ou 0, transforma categorias (o formato, por exemplo) em perguntas de sim/não ("é vertical?") e preenche os vazios com a mediana, guardando a marcação de que estavam vazios. Preencher dentro da linha de montagem, e não antes, deixa a avaliação mais honesta, e o custo foi desprezível: o erro passou de 6,92 para 6,95 pontos.

**Testei cada ideia com e sem, sempre na mesma prova.** A prova é a **validação cruzada**: os 400 vídeos de treino são divididos em 5 partes, o modelo aprende com 4 e é avaliado na 5ª, que ele não viu, até cada parte ter sido a prova uma vez. Repeti isso 3 vezes, com sorteios diferentes, o que dá 15 provas. É como estudar com 15 simulados em vez de um só. Uma feature nova só entra se reduzir o erro em pelo menos 1%; se não muda nada, decide a interpretação.

**O texto na tela ficou como categoria.** Tratado como uma escala de 0 (pouco) a 2 (muito), o erro sobe 20%. Faz sentido: o melhor é o meio, e uma escala força uma linha reta, como se mais texto fosse sempre melhor ou sempre pior.

**A música no TikTok ficou** mesmo sem passar da régua de 1%: ela não atrapalha, confirma a pergunta 1.3 (no TikTok, vídeos sem voz têm nota menor) e dá ao motor da Parte 3 uma regra própria do TikTok. **A contagem de boas práticas** (gancho + rosto + chamada para ação + legenda) ajudou só a Random Forest, um dos modelos testados no 2.2, e entrou só nela. As outras ideias (gancho por rede, curvas para a duração, faixas de duração) não melhoraram nada e saíram.

## Limites

Como nenhuma ideia passou da régua de 1%, as decisões de manter ou tirar pesaram mais a interpretação do que o erro. Os dados são simulados: a nota parece ter sido gerada somando o efeito de cada atributo, o que explica por que curvas e combinações quase não ajudam.
