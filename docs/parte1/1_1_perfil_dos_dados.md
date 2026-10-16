# Pergunta 1.1: qual o perfil geral dos dados?

Notebook: [`notebooks/parte1/1_1_perfil_dos_dados.ipynb`](../../notebooks/parte1/1_1_perfil_dos_dados.ipynb).

## Pergunta

Qual o perfil geral dos dados? Distribuições, valores faltantes, outliers. Como você trataria cada caso?

## Resposta curta

A base tem 500 vídeos de anúncio ("criativos") de 2024, veiculados no Meta, no TikTok e no LinkedIn. Antes de olhar qualquer coisa, separei 400 para estudar e guardei 100 para a prova final do modelo, na Parte 2.

Os números de volume, como impressões, gasto e receita, são muito desiguais: a maioria das campanhas é pequena, e algumas são enormes. Por isso uso a **mediana** (o valor do meio) em vez da média, que é puxada pelas gigantes. A nota que a Klike dá a cada vídeo, o `klike_score`, não tem esse problema.

Achei 10 linhas com contas que não batiam (um número digitado errado) e corrigi cada uma com aritmética. Os valores vazios são poucos (de 5% a 9% em 7 colunas) e não seguem nenhum padrão. O que dava para calcular, calculei; o resto preenchi com a mediana da rede social do vídeo. Os valores extremos que não eram erro são campanhas grandes de verdade, e ficaram.

Também organizei as métricas por etapa: ver, interagir, clicar, comprar. Isso mostrou que cada tipo de campanha tem a sua métrica de sucesso.

## O que fiz, passo a passo

**1. Separei os dados antes de olhar.** Guardei 20% dos vídeos como uma "prova na gaveta". Se eu olhasse esses vídeos agora, minhas decisões seriam influenciadas por eles, e o teste final do modelo deixaria de ser honesto. O sorteio é sempre o mesmo, para qualquer pessoa conseguir repetir. Ele também mantém a mesma proporção de cada rede social nas duas partes. Daqui em diante, tudo usa só os 400 vídeos de estudo.

**2. Olhei a estrutura da base.** Contei quantos vídeos há em cada rede, categoria e objetivo, e procurei linhas repetidas (não há nenhuma). A descoberta mais importante foi sobre o formato: o TikTok não tem nenhum vídeo horizontal, e o LinkedIn tem só 9 verticais. Isso limita algumas comparações depois. Vi também que o objetivo da campanha e a categoria do produto quase se definem um ao outro (as campanhas de marca, por exemplo, só têm dois objetivos). Na prática, as duas colunas repetem informação.

**3. Olhei como os números se distribuem.** Para cada coluna, comparei a média com a mediana e desenhei um histograma, um gráfico de barras que mostra quantos vídeos caem em cada faixa de valor. Nas colunas de volume, a média de impressões chega a ser 7,7 vezes a mediana: poucas campanhas gigantes puxam a média para cima. Para os gráficos ficarem legíveis, usei uma escala que "aperta" os números enormes (a escala logarítmica).

**4. Conferi se as contas batiam.** Várias colunas são contas de outras. A taxa de cliques (CTR) é cliques ÷ impressões, o custo por clique (CPC) é gasto ÷ cliques, e o retorno sobre o gasto (ROAS) é receita ÷ gasto. Então dá para conferir cada linha, como uma auditoria. Achei 10 erros:

- em 4 linhas, as impressões estavam erradas: cliques e CTR concordavam entre si, e as impressões ficavam de 150 a 1.100 vezes acima do que deveriam. Corrigi com impressões = cliques ÷ CTR;
- em 6 linhas, o custo por clique não batia. Para saber se o erro estava no custo por clique ou no gasto, usei uma terceira conta (receita ÷ ROAS) como desempate, uma espécie de voto da maioria. Assim corrigi 3 custos por clique e 3 gastos;
- num desses casos, a terceira conta não ajudava (a receita era zero). Decidi pelo bom senso: com o gasto original, o custo para aparecer mil vezes ficaria 4 vezes acima do maior valor de todo o Meta. Então o erro estava no gasto.

**5. Tratei os valores vazios.** Primeiro contei quantos faltam e onde. Depois perguntei se os buracos têm padrão. Por exemplo, os vídeos sem duração informada são piores ou melhores que os outros? Para saber o que é uma diferença grande, comparei com 1.000 grupos sorteados ao acaso, do mesmo tamanho: se a diferença cabe no que o acaso produz, não há padrão. Em seguida, escolhi como preencher. Testei quatro jeitos de adivinhar a duração, dos mais simples aos mais sofisticados. Escondi de propósito 10% das durações conhecidas e medi qual jeito errava menos. Por fim, antes de preencher, guardei uma marcação de quais valores eram vazios, para não perder essa informação.

**6. Procurei valores extremos** com duas regras automáticas comuns, e conferi se elas encontravam os 10 erros do passo 4.

**7. Criei colunas novas** que tornam as campanhas comparáveis:

- a **retenção**, a fração do vídeo que a pessoa assistiu;
- a **taxa de conversão**, quantos dos cliques viraram venda ou cadastro;
- o **custo para aparecer mil vezes** (CPM);
- o **custo por conversão** (CPA), quanto custa cada venda ou cadastro;
- o **número de boas práticas** do vídeo (gancho, rosto, chamada para ação e legenda, de 0 a 4).

**8. Passei a limpeza para um arquivo reaproveitável** (`src/limpeza.py`). Conferi que ele dá exatamente o mesmo resultado do passo a passo e salvei os dados limpos.

## Por que fiz assim

**Mediana, e não média.** Se um bilionário entra numa sala, a renda média dispara, mas a mediana quase não muda. Com campanhas gigantes misturadas às pequenas, a mediana descreve melhor o vídeo típico.

**Corrigir, e não apagar.** Em cada linha com erro, só um número estava errado; o resto do vídeo estava certo. Apagar a linha jogaria fora informação boa.

**Preencher com a mediana da rede social.** Foi o jeito que menos errou no teste do passo 5 (9,1 segundos de erro médio, contra 9,7 a 10,0 dos métodos mais sofisticados), e é o mais fácil de explicar. Um dos métodos sofisticados só ficaria melhor usando o tempo assistido, que só existe depois de o vídeo ir ao ar. Usar isso para adivinhar a duração seria trapacear na Parte 2, cujo modelo precisa funcionar antes de postar.

**Legenda vazia vira "desconhecido".** "Não sei se tem legenda" é diferente de "não tem legenda". Inventar um sim ou um não seria afirmar algo que eu não sei.

**Guardar quais valores eram vazios.** Quando preencho, todos os vazios ficam iguais à mediana. Isso esconderia diferenças nas análises seguintes. A marcação permite voltar a usar só os valores reais quando for preciso.

**Não corrigir o limite do CTR.** O valor verdadeiro dos vídeos que bateram no limite se perdeu, e não há conta que o recupere. O honesto é avisar, não inventar.

## O que descobri

Os 10 erros eram poucos, mas pesavam muito: corrigi-los muda a **média** de impressões em 72%, e a mediana em só 0,2%. É a prova de que os erros existiam e de que a mediana é o número certo para estes dados.

O CTR parece ter sido cortado num limite: 42 vídeos têm CTR exatamente igual a 0,15, e nenhum passa disso. O mesmo acontece com o engajamento, em 0,10. É como uma balança que só vai até 150 kg: quem pesa mais aparece como 150. Esse corte pega mais os vídeos com gancho (15% deles, contra 5,7% dos sem gancho). Por isso, nas próximas perguntas, o efeito do gancho no CTR aparece menor do que realmente é.

As campanhas de marca ("Branding") quase nunca têm receita: 47 de 49 têm receita zero, embora tenham conversões. Elas não são feitas para vender, então deixei a marca de fora de toda análise de retorno sobre o gasto.

Os vazios não têm padrão: em 19 de 21 comparações, a diferença coube no que o acaso produz. A exceção é o custo por clique vazio, que eu recalculo pela conta exata, então não atrapalha.

As regras automáticas de valores extremos marcaram 50 vídeos: os 10 erros e mais 40 campanhas sem erro nenhum, só grandes. A regra automática aponta candidatos; quem decide se é erro são as contas.

Cada objetivo de campanha tem a sua métrica de sucesso. A taxa de cliques quase não muda entre objetivos (de 5,4% a 6,7%), mas o resto muda muito. As campanhas feitas para serem vistas (awareness) quase não vendem: cada conversão custa R$67, e o retorno é zero. Para elas, o que importa é a retenção, que é a maior de todas (57%). As de instalação de aplicativo têm o menor custo por conversão (R$10,9). As de conversão têm o maior retorno (2,4 reais por real investido). Julgar todas pelo CTR ou pelo retorno seria injusto. Por isso, a pergunta 1.2 olha também a métrica principal de cada objetivo.

A época do ano não importa: o mês explica cerca de 3% da variação, o mesmo que o acaso.

## Limites

Os dados são simulados, então alguns padrões podem ser simplificações de quem os gerou. O LinkedIn tem só 66 vídeos no treino, e tudo o que digo sobre ele tem mais incerteza. O valor real dos vídeos que bateram no limite do CTR se perdeu. E o caso empatado do passo 4 foi resolvido por bom senso, não por uma conta exata; o risco é pequeno, porque é uma campanha de marca, que fica fora das análises de retorno.
