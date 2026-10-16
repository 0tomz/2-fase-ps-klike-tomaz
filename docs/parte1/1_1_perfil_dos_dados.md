# Pergunta 1.1: qual o perfil geral dos dados?

Notebook: [`notebooks/parte1/1_1_perfil_dos_dados.ipynb`](../../notebooks/parte1/1_1_perfil_dos_dados.ipynb). Os termos técnicos estão explicados em [`docs/glossario.md`](../glossario.md).

## Pergunta

Qual o perfil geral dos dados? Distribuições, valores faltantes, outliers. Como você trataria cada caso?

## Resposta curta

- **Tamanho:** 500 criativos (vídeos de anúncio) de 2024. Separei 400 para estudar (treino) e guardei 100 para a prova final (teste).
- **Distribuições:** as métricas de volume (impressões, gasto, receita) têm poucas campanhas gigantes, então uso a **mediana** em vez da média. A nota `klike_score` é bem distribuída, sem esse problema.
- **Erros:** 10 linhas tinham contas que não batiam (impressões, CPC ou gasto digitados errado). Corrigi com aritmética.
- **Faltantes:** de 5% a 9% em 7 colunas, sem padrão. Calculei o que dava para calcular e preenchi o resto com a mediana da plataforma.
- **Extremos:** quase todos são campanhas grandes de verdade e ficaram. Só os erros foram corrigidos.
- **Métricas:** a base mede o funil inteiro (ver, interagir, clicar, converter, vender). Criei retenção, taxa de conversão, CPM e **CPA** (custo por conversão). Cada objetivo de campanha tem a sua métrica principal; a nota `klike_score` resume tudo e é o alvo da Parte 2.

## O que fiz, passo a passo

1. **Separei treino e teste antes de olhar os dados.** O teste é a "prova guardada na gaveta": se eu olhasse, contaminaria a nota final da Parte 2. Usei `train_test_split` com:
   - `random_state=42`, para o sorteio sair sempre igual;
   - `stratify=platform`, para treino e teste terem a mesma proporção de cada rede.
2. **Olhei a estrutura:** tamanho, tipos, linhas repetidas (nenhuma) e quantos criativos há em cada categoria.
   - Com `crosstab` vi que **o TikTok não tem nenhum vídeo horizontal** e que o LinkedIn tem só 9 verticais.
   - O **V de Cramér** (de 0 a 1, quanto uma coluna de texto define a outra) mostrou que objetivo e categoria andam muito juntos (0,59).
3. **Olhei as distribuições:** `describe`, média × mediana, skew (o quanto a distribuição é torta) e histogramas com 30 barras. Nas métricas de volume usei **log1p** (`log(1 + x)`), que "aperta" os números gigantes para o gráfico ficar legível.
4. **Conferi se as contas batiam.** Várias métricas são contas de outras (`ctr = cliques ÷ impressões`, `cpc = gasto ÷ cliques`, `roas = receita ÷ gasto`), então dá para auditar linha por linha.
   - **4 impressões erradas:** cliques e CTR concordavam entre si, só as impressões estavam fora. Corrigi com `impressões = cliques ÷ CTR`.
   - **6 CPC que não batiam:** usei o "voto da maioria". O gasto aparece em duas contas; se a receita ÷ ROAS confirma o gasto, o errado é o CPC; se não confirma, o errado é o gasto.
   - **1 empate (receita = 0):** decidi pelo bom senso. Com o gasto original, o custo por mil impressões ficaria 4 vezes acima do maior do Meta.
   - Mostrei uma tabela antes/depois das 10 linhas.
5. **Tratei os vazios.**
   - **Onde estão:** contei os vazios e mostrei num heatmap onde estão e quais faltam juntos.
   - **"Os buracos têm padrão?":** comparei a mediana da nota, do CTR e do gasto dos criativos sem o valor com a de todos. Para saber o que é diferença grande, criei uma **régua do acaso**: sorteei 1.000 grupos do mesmo tamanho e vi quanto a mediana varia só por sorte.
   - **Qual preenchimento:** testei quatro jeitos de preencher a duração (mediana geral, mediana da plataforma, KNNImputer e IterativeImputer). Escondi 10% dos valores conhecidos e medi o erro (MAE).
   - **Indicador de faltante:** antes de preencher, criei para cada coluna uma coluna 0/1 que vale 1 quando o valor original estava vazio. É o `add_indicator` do Projeto_carros.
6. **Procurei valores extremos** com a regra do IQR e com o z-score, e conferi se elas achavam os 10 erros.
7. **Criei colunas novas:** retenção (fração do vídeo assistida), taxa de conversão, CPM (custo por mil impressões), **CPA** (gasto ÷ conversões; vazio quando não houve conversão), número de boas práticas (0 a 4) e faixa de duração.
   - **O que é "boa performance"?** Organizei as métricas por etapa do funil, se maior ou menor é melhor, e para qual objetivo cada uma é a principal:

| Etapa do funil | Métrica | Melhor quando | Principal para o objetivo |
|---|---|---|---|
| Ver | CPM, retenção | menor; maior | awareness |
| Interagir | engajamento | maior | engagement |
| Clicar | CTR, CPC | maior; menor | traffic |
| Converter | taxa de conversão, CPA | maior; menor | conversions, app_install |
| Vender | ROAS | maior | conversions (fora Branding) |
| Tudo | `klike_score` | maior | todos (alvo da Parte 2) |

   - Depois, a mediana de cada métrica em cada objetivo.
8. **Passei a limpeza para `src/limpeza.py`** (uma função curta por problema), conferi que ele dá exatamente o mesmo resultado do passo a passo e salvei os arquivos limpos.

## Por que fiz assim

- **Mediana, e não média:** se um bilionário entra numa sala, a média de renda dispara e a mediana quase não muda. Aqui, a média de impressões é 7,7 vezes a mediana.
- **Corrigir, e não apagar, as linhas com erro:** o resto do criativo estava certo. Apagar jogaria fora informação boa por causa de um número.
- **Mediana da plataforma, e não KNN ou Iterative:**
  - foi o método que menos errou (9,1 s, contra 9,9 a 10,0 s dos outros);
  - é o mais simples de explicar;
  - não usa o tempo assistido, que só existe depois de postar. Usá-lo para preencher a duração seria trapaça na Parte 2.
- **Legenda vazia vira "desconhecido":** "não sei se tem legenda" é diferente de "não tem legenda". Inventar "sim" ou "não" seria mentir.
- **Indicador de faltante:** preencher apaga quais valores eram inventados. O indicador guarda isso, e assim:
  - as perguntas 1.2 e 1.3 medem efeitos só com valores reais;
  - a Parte 2 pode usar o fato de faltar, se isso ajudar.
- **Não corrigi o teto do CTR:** o valor verdadeiro se perdeu. O certo é avisar, não inventar.

## O que descobri

- **10 erros** escondidos. Corrigi-los muda a **média** de impressões em −72% e a **mediana** em só −0,2%. Isso prova que os erros existiam e que a mediana é o número certo.
- **O CTR e o engajamento parecem cortados num teto:** 42 criativos com CTR exatamente 0,15 e 7 com engajamento exatamente 0,10. O corte pega mais os vídeos com gancho (15% deles, contra 5,7% dos sem gancho), então o efeito do gancho no CTR fica subestimado.
- **ROAS não se aplica a Branding:** 47 das 49 campanhas de marca têm receita zero, mas têm conversões. Campanha de marca não é feita para vender. Branding fica fora de qualquer análise de ROAS.
- **Os vazios não têm padrão:** 19 de 21 comparações ficaram dentro do acaso. A exceção é o CPC vazio, que é recalculado pela conta exata, então não atrapalha.
- **O z-score marca 50 criativos:** os 10 erros e mais 40 campanhas sem erro nenhum. A regra genérica aponta candidatos; quem decide são as contas.
- **Cada objetivo tem o seu "bom número":**
  - o CTR quase não muda entre objetivos (5,4% a 6,7%), mas o fim do funil muda muito;
  - awareness quase não converte (taxa de conversão de 0,7%, CPA de R$67, ROAS 0); a métrica dela é a retenção (57%, a maior);
  - app install tem o menor CPA (R$10,9 por instalação);
  - conversions tem o maior ROAS (2,4) e a maior nota (63,7).
  
  Por isso, julgar todas as campanhas pelo CTR ou pelo ROAS seria injusto. A pergunta 1.2 mede os atributos também na métrica principal de cada objetivo.
- **CPA:** mediana de R$23,9, com cauda longa (até R$1.010). 16 criativos não tiveram conversão e ficam com o CPA vazio (a divisão por zero daria infinito).
- **Não há sazonalidade:** o mês explica cerca de 3% da variação, o mesmo que o acaso daria.

## Limites

- **Dados simulados:** alguns padrões podem ser simplificações da simulação.
- **O LinkedIn tem só 66 criativos no treino:** tudo sobre ele tem mais incerteza.
- **Teto do CTR:** o valor real dos melhores vídeos se perdeu.
- **Caso empatado:** a escolha do caso empatado (KLK-0224) é uma decisão de bom senso, não uma conta exata. O risco é pequeno, porque é Branding.
