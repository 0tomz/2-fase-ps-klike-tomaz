# 1.1 Qual o perfil geral dos dados?

> Pergunta do case: qual o perfil geral dos dados? Distribuições, valores faltantes, outliers. Como você trataria cada caso?
>
> Notebook: [`1_1_perfil_dos_dados.ipynb`](../../notebooks/parte1/1_1_perfil_dos_dados.ipynb)

## Resposta curta

A base tem 500 vídeos de anúncio de 2024, do Meta, do TikTok e do LinkedIn. Os números de volume (impressões, gasto, receita) são muito desiguais: a maioria das campanhas é pequena, e poucas são enormes. Por isso uso a mediana, e não a média. Havia 10 linhas com números digitados errado, que corrigi com aritmética. Os valores vazios são poucos (de 5% a 9% em 7 colunas) e não seguem nenhum padrão; preenchi com a mediana da rede social do vídeo. Os valores extremos que não eram erro são campanhas grandes de verdade, e ficaram.

## Por que isso importa

Dois cuidados valem para todo o resto do trabalho. O primeiro: a taxa de cliques (CTR) foi cortada num limite de 15%, como uma balança que só vai até 150 kg. Os melhores vídeos aparecem todos como 15%, então o efeito de um bom gancho nos cliques parece menor do que é. O segundo: as campanhas de marca (Branding) quase nunca têm receita, porque não são feitas para vender. Julgá-las pelo retorno sobre o gasto seria injusto, e por isso elas ficaram fora dessa conta.

Também vale lembrar que cada objetivo de campanha tem a sua métrica de sucesso. As campanhas feitas para serem vistas (awareness) quase não vendem (cada conversão custa R$67), mas têm a maior retenção (57% do vídeo assistido). As de instalação de app têm o menor custo por conversão (R$11). Por isso, ao longo do trabalho, cada objetivo é julgado pela sua própria métrica.

## Como cheguei lá

**Separei os dados antes de olhar.** Guardei 100 vídeos (20%) como uma "prova na gaveta", para testar o modelo da Parte 2 no fim. Se eu olhasse esses vídeos agora, minhas escolhas seriam influenciadas por eles, e a nota final deixaria de ser honesta. O sorteio é fixo e mantém a mesma proporção de cada rede nas duas partes. Daqui em diante, tudo usa só os 400 vídeos de estudo, o **treino**.

**Escolhi a mediana.** A mediana é o valor do meio quando tudo é colocado em ordem. Se um bilionário entra numa sala, a renda média dispara, mas a mediana quase não muda. Aqui, a média de impressões é 7,7 vezes a mediana. A mediana descreve melhor o vídeo típico.

**Conferi as contas.** Várias colunas são contas de outras: o CTR é cliques ÷ impressões, o custo por clique é gasto ÷ cliques, o retorno é receita ÷ gasto. Conferindo linha a linha, achei 10 erros: 4 em impressões, 3 em custo por clique e 3 em gasto. Para saber qual número estava errado quando dois não batiam, usei uma terceira conta como desempate. Corrigi em vez de apagar, porque em cada linha só um número estava errado. Corrigir só essas 10 linhas mudou a média de impressões em 72%, e a mediana em 0,2%. É a prova de que a mediana era a escolha certa.

**Tratei os vazios.** Primeiro perguntei se eles têm padrão: os vídeos sem duração informada, por exemplo, são piores que os outros? Para saber o que é uma diferença grande, comparei com 1.000 grupos sorteados ao acaso. Em 19 de 21 comparações, a diferença coube no acaso, ou seja, não há padrão. Depois testei quatro jeitos de preencher, escondendo de propósito valores conhecidos e medindo qual errava menos. A mediana da rede social errou menos (9,1 segundos de erro na duração, contra 9,7 a 10,0 dos métodos mais sofisticados) e é a mais fácil de explicar. Guardei uma marcação de quais valores eram vazios, e a legenda vazia virou "desconhecido": não saber se há legenda é diferente de não ter legenda.

**Olhei os extremos.** Duas regras automáticas marcaram 50 vídeos: os 10 erros e mais 40 campanhas sem erro nenhum, só grandes. A regra aponta candidatos; quem decide se é erro são as contas.

**Criei colunas que tornam as campanhas comparáveis:** a retenção (fração do vídeo assistida), a taxa de conversão, o custo para aparecer mil vezes (CPM) e o custo por conversão (CPA). Também organizei as métricas por etapa do caminho do cliente, o **funil**: ver, interagir, clicar, converter e vender.

A época do ano não importa: o mês explica cerca de 3% da variação da nota, o mesmo que o acaso. Toda a limpeza ficou num arquivo reaproveitável (`src/limpeza.py`), que os outros notebooks aplicam ao arquivo original.

## Limites

Os dados são simulados, então alguns padrões podem ser simplificações de quem os gerou. O LinkedIn tem só 66 vídeos no treino, e tudo sobre ele é mais incerto. O valor real dos vídeos que bateram no limite do CTR se perdeu. E um dos 10 erros foi resolvido por bom senso, e não por uma conta exata: com o gasto original, o custo para aparecer mil vezes ficaria 4 vezes acima do maior de todo o Meta.
