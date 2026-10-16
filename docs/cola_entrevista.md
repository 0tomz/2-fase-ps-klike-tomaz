# Cola para a entrevista: Parte 1 (EDA)

Para cada pergunta: um roteiro de cerca de 2 minutos para falar em voz alta, e 3 ou 4 perguntas difíceis que a banca pode fazer, com resposta.

---

## 1.1 Perfil geral dos dados

**Roteiro (~2 min):**

> "Antes de olhar qualquer coisa, separei 20% dos dados para teste, com a mesma proporção de cada plataforma. É a prova guardada na gaveta: tudo o que eu decido vem só do treino, para a nota da Parte 2 ser honesta.
>
> Depois, a primeira coisa que fiz foi conferir se as contas batiam, porque várias métricas são contas de outras: CTR é cliques sobre impressões, CPC é gasto sobre cliques, ROAS é receita sobre gasto. Achei 10 linhas com erro. Em 4, as impressões estavam na casa dos milhões quando cliques e CTR davam algumas dezenas de milhares; corrigi com cliques sobre CTR. Em 6, o CPC não batia, e usei o ROAS para desempatar qual número estava errado. Corrigir essas 10 linhas mudou a média de impressões em 72% e a mediana quase nada. Por isso uso a mediana em toda a análise: as métricas têm cauda longa.
>
> Os vazios eram poucos, de 5 a 9%, e não tinham padrão: comparei com grupos sorteados ao acaso e quase tudo ficou dentro do acaso. O que dava para calcular, calculei. O resto preenchi com a mediana da plataforma, que foi o método que menos errou num teste em que eu escondi valores conhecidos. Guardei um indicador de quais valores eram inventados.
>
> Dois cuidados para o resto da análise: o CTR parece cortado em 0,15, então o efeito do gancho fica subestimado; e ROAS não se aplica a Branding, que não é feito para vender, então tirei Branding dessas análises."

**Perguntas difíceis:**

1. **"Por que não apagou as linhas com erro?"**
   O resto do criativo estava certo, e o erro era um número só, recuperável pela conta. Apagar jogaria fora informação boa. São só 10 linhas, mas elas mudavam a média de impressões em 72%.
2. **"Por que não usou KNN ou IterativeImputer, que são mais sofisticados?"**
   Eu testei. Escondi 10% das durações conhecidas e medi o erro: a mediana da plataforma errou menos (9,1 s contra 9,7 a 10,0 s). Além disso, o IterativeImputer só ficaria melhor usando o tempo assistido, que só existe depois de postar. Isso seria vazamento de dados na Parte 2.
3. **"Como você sabe que os vazios não escondem nada?"**
   Comparei a mediana da nota, do CTR e do gasto de quem tem vazio com a de todos, e usei como régua 1.000 grupos sorteados do mesmo tamanho. Em 19 de 21 comparações, a diferença coube no acaso. A exceção foi o CPC vazio, que eu recalculo pela conta exata, então não atrapalha. Não dá para provar que não há padrão, mas não há sinal de que haja.

---

## 1.2 Atributos × performance

**Roteiro (~2 min):**

> "Primeiro separei o que se sabe antes de postar (os atributos do vídeo e o contexto) do que só se sabe depois (CTR, engajamento, nota). A Klike promete prever antes de postar, então o modelo não pode usar o CTR para prever a nota: seria olhar o gabarito.
>
> Depois comparei a mediana de cada métrica com e sem cada atributo, e usei bootstrap para ver se a diferença era confiável. O gancho nos 3 primeiros segundos foi o mais forte: 66% a mais de CTR, 56% a mais de engajamento e uns 17 pontos a mais de nota. O rosto humano vem em segundo. Quantidade de texto tem um ponto ótimo no meio: muito texto tira uns 15 pontos.
>
> O cuidado principal foi o confundimento. Quem já conhece a marca clica mais, e se os vídeos com gancho fossem mostrados mais para esse público, o gancho levaria um crédito que não é dele. Conferi de três jeitos: a proporção de retargeting é parecida com e sem gancho; o gancho funciona dentro de cada plataforma e de cada público; e uma regressão linear, mantendo o resto igual, dá os mesmos 17 pontos.
>
> Não olhei só o CTR: analisei nove métricas, do clique à venda, incluindo o CPA, que eu criei. Repeti a regressão para cada uma. O criativo age no começo do funil: o gancho sobe CTR, engajamento e retenção, mas não muda conversão, CPA nem ROAS. Quem move a venda é o público: em retargeting, o CPA é 44% menor. As exceções são o muito texto, que atrapalha até a venda, e o formato horizontal, que sai mais caro por conversão. E julguei cada objetivo pela sua métrica: retenção em awareness, CTR em traffic, CPA em conversions.
>
> Uma surpresa: não existe duração ideal nestes dados."

**Perguntas difíceis:**

1. **"Isso prova que o gancho causa o aumento?"**
   Não. São dados observados, então é associação. Controlei o que dava (plataforma, público, categoria, outros atributos) e o efeito se manteve. Mas a prova seria um teste A/B, sorteando quem vê o vídeo com e sem gancho.
2. **"Você fez 40 comparações. Algumas não seriam significativas por acaso?"**
   Sim, cerca de 2 em 40. Por isso eu só destaco o que se repete. O gancho aparece em CTR, engajamento, retenção e nota, nas três redes e na regressão. Um efeito que aparecesse uma vez só eu trataria como indício.
3. **"Por que tanto CTR? Ele é o alvo?"**
   Não. O alvo é a nota `klike_score`, e o CTR é uma métrica de resultado: nem pode entrar no modelo da Parte 2, porque só existe depois de postar. Ele aparece muito porque é o primeiro exemplo do enunciado, é a métrica que o criativo mais mexe e é comparável entre redes (a plataforma explica 0,2% dele). Mas a resposta abre pela nota e cobre nove métricas.
4. **"A densidade de texto tem correlação quase zero com a nota. Como você diz que ela importa?"**
   A correlação mede relação em linha reta, e aqui a relação tem forma de morro: o texto médio é o melhor, e os dois extremos perdem. As medianas por nível mostram isso (67 pontos no médio, 48 no muito texto, 59 no pouco). Correlação perto de zero não quer dizer que não há relação.

---

## 1.3 Padrões por plataforma

**Roteiro (~2 min):**

> "Li o 'TikTok × LinkedIn' do enunciado como um exemplo, então comparei as três redes e os três pares.
>
> O contexto muda muito: o CPC do LinkedIn é cerca de cinco vezes o do TikTok, o TikTok engaja quase o dobro, e o ROAS vai de 0,6 no LinkedIn a 2,9 no TikTok. Mas o CTR e a nota mediana são parecidos.
>
> Para saber se o que funciona muda, calculei o efeito de cada atributo em cada rede e, para cada par, a diferença entre os efeitos, com intervalo por bootstrap. De 72 comparações, só 1 deu diferença confiável, menos do que o acaso daria. Gancho, rosto e evitar muito texto funcionam nas três.
>
> Na regressão dentro de cada rede apareceram dois indícios: tirar a voz custa uns 12 pontos a mais no TikTok do que no Meta, e o gancho pesa um pouco mais no LinkedIn. Na comparação simples, a voz não aparecia, porque vinha misturada com outros atributos.
>
> Então a resposta é: as redes diferem no contexto, não no que funciona. O motor da Parte 3 pode partir de regras comuns e somar poucos ajustes por rede. Fechei com um manual por plataforma."

**Perguntas difíceis:**

1. **"Por que a comparação simples e a regressão discordam sobre a música no TikTok?"**
   A comparação simples junta tudo: vídeos com mais música também podem ter menos gancho ou mais texto, e esses efeitos se misturam. A regressão compara vídeos iguais em todo o resto e isola a música. Quando as duas discordam, confio mais na que controla os outros atributos, mas trato como indício a ser testado.
2. **"Dá para confiar em conclusões sobre o LinkedIn com 66 criativos?"**
   Só na direção. Os intervalos do LinkedIn são bem mais largos, e várias células têm menos de 15 criativos e ficam em branco. Por exemplo, "vertical vai mal no LinkedIn" eu não pude testar: só há 9 verticais.
3. **"O rosto é confiável no TikTok e não no LinkedIn. Então ele funciona diferente?"**
   Não necessariamente. O LinkedIn tem menos criativos, então o intervalo dele é mais largo. Para dizer que um efeito muda entre duas redes, calculei a diferença entre os efeitos, sorteio a sorteio do bootstrap, e olhei se o intervalo dessa diferença cruza o zero. No CTR do rosto, TikTok × LinkedIn dá +2 pontos percentuais: praticamente igual.
4. **"Não achar diferença prova que é igual?"**
   Não. Os intervalos das diferenças são largos (cerca de 90 pontos percentuais no par Meta × TikTok). Digo que não há sinal de diferença, e que só diferenças grandes seriam detectadas com esse tamanho de base.

---

## 1.4 Visualizações para marketing

**Roteiro (~2 min):**

> "O enunciado pede pelo menos três figuras, e eu escolhi três, cada uma respondendo a uma pergunta do marketing. O título de cada uma é a conclusão, não a descrição: 'o gancho é o que mais sobe a nota', e não 'klike_score por has_hook'. Cada plataforma tem sempre a mesma cor, o que importa vem em azul e o resto em cinza, e os valores estão escritos nas barras.
>
> A primeira responde 'o que eu mudo no próximo vídeo?': o gancho lidera na nota, no CTR e no engajamento, e muito texto derruba. A segunda responde 'isso vale em todas as redes?': o básico funciona nas três, com a exceção da voz no TikTok. A terceira responde 'o criativo vende?': o vídeo decide o clique, e a venda depende de quem vê. O gancho não muda o custo por conversão, mas o público de retargeting converte 89% mais.
>
> Em todas, o rodapé diz quantos criativos e de onde vem o dado, e grupos com menos de 15 criativos ficam de fora."

**Perguntas difíceis:**

1. **"Por que só três figuras?"**
   Foi o que o enunciado pediu, e três bastam para contar a história: o que mudar, onde vale e até onde o vídeo pesa. Eu tinha feito outras (duração, checklist, texto por rede), mas elas repetiam algo destas três ou mostravam um resultado negativo que cabe numa frase ("não há duração ideal").
2. **"Por que tirou as barras de erro?"**
   Para quem não é técnico, barra de erro confunde mais do que ajuda. A incerteza vai no rodapé ou na cor: na figura 3, as células em cinza claro são as que podem ser acaso. Nos notebooks de análise, os intervalos estão todos lá.
3. **"Na figura 3, o gancho não muda a venda. Então o gancho não serve?"**
   Serve, para o que ele faz: atenção e clique (CTR +66%, retenção +42%) e cerca de 17 pontos de nota. O que a figura mostra é que cobrar venda do criativo é injusto: quem move conversão e custo por conversão é o público e a oferta.
