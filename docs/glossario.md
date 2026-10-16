# Glossário da Parte 1

Cada termo usado nos notebooks da Parte 1, na ordem em que aparece, com uma frase simples e uma analogia.

## Notebook 1.1: perfil dos dados

| Termo | O que é | Analogia |
|---|---|---|
| **Criativo** | Cada vídeo de anúncio da base; é uma linha da tabela. | A "peça" de uma campanha, como um cartaz numa parede. |
| **Treino e teste** | Treino: a parte dos dados que eu estudo. Teste: a parte guardada para medir o modelo no fim. | O teste é a prova guardada na gaveta: se eu olhar antes, a nota não vale. |
| **`random_state=42` (semente)** | Número que fixa o sorteio, para ele sair sempre igual. | Embaralhar o baralho sempre do mesmo jeito. |
| **`stratify`** | Faz o sorteio manter a proporção de cada grupo (aqui, de cada plataforma). | Montar dois times com a mesma quantidade de goleiros em cada um. |
| **`crosstab`** | Tabela que conta quantas linhas há em cada combinação de duas colunas. | Uma tabela de "quantos alunos de cada turma são de cada bairro". |
| **V de Cramér** | Número de 0 a 1 que diz o quanto uma coluna de texto define a outra (0 = nada, 1 = totalmente). | Saber a cidade quase define o estado (perto de 1); saber o signo não diz nada do time (perto de 0). |
| **Média** | Soma de tudo dividida pela quantidade. | Dividir a conta do restaurante igualmente. |
| **Mediana** | O valor do meio quando tudo é colocado em ordem. | Se entra um bilionário na sala, a média de renda dispara e a mediana quase não muda. |
| **Cauda longa** | Quando a maioria dos valores é pequena e poucos são enormes. | A maioria das músicas tem poucas visualizações e algumas têm bilhões. |
| **Skew (assimetria)** | Número que mede o quanto a distribuição é torta; 0 = simétrica. | Uma gangorra: 0 é equilibrada; quanto maior, mais pende para um lado. |
| **Histograma** | Gráfico de barras que mostra quantos valores caem em cada faixa. | Contar quantos alunos tiraram nota entre 0–1, 1–2, ..., 9–10. |
| **log1p** | `log(1 + x)`: encolhe os números grandes muito mais que os pequenos. | Uma lupa ao contrário: 10 vira 2,4, e 10 mil vira 9,2. |
| **CTR** | Cliques ÷ impressões: a fração de quem viu e clicou. | De 100 pessoas que passaram pela vitrine, quantas entraram na loja. |
| **CPC** | Gasto ÷ cliques: quanto custa cada clique. | Quanto se paga por cada pessoa que entrou na loja. |
| **ROAS** | Receita ÷ gasto: quantos reais voltam para cada real investido. | Coloquei R$1 na máquina e saíram R$3: ROAS 3. |
| **Teto (valor cortado)** | Quando o dado foi limitado num máximo e quem passava dele ficou registrado no máximo. | Uma balança que só vai até 150 kg: quem pesa 180 aparece como 150. |
| **Faltante (vazio)** | Uma célula da tabela sem valor. | Uma pergunta deixada em branco no questionário. |
| **Heatmap** | Tabela em que a cor de cada célula mostra o tamanho do número. | Um mapa de calor do tempo: mais escuro = mais quente. |
| **Régua do acaso** | Sortear muitos grupos aleatórios do mesmo tamanho para ver quanto um número muda só por sorte. | Antes de dizer que uma moeda é viciada, ver quantas caras sai jogando uma moeda normal. |
| **MAE (erro absoluto médio)** | A média do tamanho dos erros, sem sinal. | "Em média, eu erro 9 segundos." |
| **KNNImputer** | Preenche um vazio com a média dos registros mais parecidos. | Adivinhar a altura de alguém pela altura dos 10 colegas mais parecidos com ele. |
| **IterativeImputer** | Preenche um vazio com uma regressão que usa as outras colunas. | Estimar o peso de alguém a partir da altura e da idade. |
| **Padronizar (`StandardScaler`)** | Colocar as colunas na mesma escala (média 0, desvio 1). | Converter preços em reais, dólares e euros para a mesma moeda antes de comparar. |
| **Indicador de faltante** | Coluna 0/1 que vale 1 quando o valor original estava vazio e foi preenchido (o `add_indicator` do Projeto_carros). | Um adesivo "valor estimado" no item do inventário. |
| **Quartil** | Os valores que dividem os dados ordenados em quatro partes iguais. | As marcas de 25%, 50% e 75% numa fila de pessoas por altura. |
| **IQR (intervalo interquartil)** | A largura dos 50% do meio (3º quartil − 1º quartil). Na regra do IQR, é extremo quem fica mais de 1,5 IQR fora da caixa. | Medir quão espalhada está a "turma do meio" e marcar quem se afasta muito dela. |
| **Boxplot** | Gráfico de caixa: a caixa vai do 1º ao 3º quartil, a linha é a mediana e os pontinhos são extremos. | Um resumo da fila de alturas em cinco números. |
| **Desvio padrão** | A distância típica dos valores em relação à média. | O quanto as notas de uma turma costumam se afastar da média da turma. |
| **z-score** | Quantos desvios padrão um valor está longe da média. Acima de 3 = extremo. | "Esta pessoa é 3 vezes mais alta que a variação normal da turma." |
| **Retenção** | Tempo assistido ÷ duração do vídeo: a fração do vídeo que a pessoa viu. | Ler 50 de 100 páginas de um livro: 50%. |
| **Taxa de conversão** | Conversões ÷ cliques: de quem clicou, quantos compraram ou se cadastraram. | De quem entrou na loja, quantos saíram com sacola. |
| **CPM** | Gasto ÷ impressões × 1000: quanto custa aparecer mil vezes. | O preço de mil panfletos entregues. |
| **CPA** | Gasto ÷ conversões: quanto custa cada venda, cadastro ou instalação. Fica vazio quando não houve conversão. | Quanto se gastou em panfletos para conseguir cada cliente novo. |
| **Métrica principal do objetivo** | A métrica que mede o que aquela campanha quer: retenção (awareness), engajamento (engagement), CTR (traffic), CPA (conversions e app install). | Não se julga um goleiro pelos gols que ele marca. |
| **eta²** | De 0 a 1, quanto da variação de uma métrica se explica só por saber o grupo. | Quanto da diferença de altura entre alunos se explica só por saber a série deles. |

## Notebook 1.2: atributos × performance

| Termo | O que é | Analogia |
|---|---|---|
| **Vazamento de dados** | Usar no modelo uma informação que não existiria na hora de prever. | Corrigir a prova olhando o gabarito. |
| **Correlação de Pearson** | De −1 a +1: o quanto duas colunas andam juntas em linha reta. | Altura e tamanho do sapato: quanto mais alto, maior o pé. |
| **Correlação de Spearman** | A mesma ideia, calculada sobre a ordem dos valores; pega relações curvas e não liga para valores gigantes. | Comparar a posição no ranking, e não a pontuação exata. |
| **Diferença das medianas (%)** | Mediana com o atributo ÷ mediana sem o atributo − 1. | "Lojas com vitrine iluminada vendem 30% mais que as sem." |
| **n** | Quantos criativos há num grupo. | Quantas pessoas responderam a pesquisa. |
| **Bootstrap** | Sortear os dados com reposição milhares de vezes e refazer a conta, para ver o quanto ela varia. | Refazer a mesma pesquisa várias vezes com sorteios diferentes da mesma população. |
| **Intervalo de 95%** | A faixa onde ficam 95% dos resultados do bootstrap. Se não cruza o zero, o efeito é confiável. | A margem de erro de uma pesquisa eleitoral. |
| **Confundimento** | Quando uma terceira coluna mexe nas duas que estou comparando e cria uma relação falsa. | Vendas de sorvete e afogamentos sobem juntos por causa do verão, não um por causa do outro. |
| **Retargeting** | Anúncio mostrado para quem já interagiu com a marca. | Mandar convite de novo para quem já foi à festa no ano passado. |
| **Regressão linear** | Fórmula que soma o efeito de cada coluna; o peso de cada uma se lê "mantendo todo o resto igual". | Uma receita: cada ingrediente soma um tanto ao sabor final. |
| **`get_dummies` (one-hot)** | Transforma cada categoria de texto numa coluna 0/1. | Trocar "cor = azul" por perguntas "é azul? sim/não", "é verde? sim/não". |
| **Categoria de referência** | A categoria que fica de fora no one-hot; as outras são comparadas com ela. | Medir a altura de todos em relação ao aluno mais baixo da turma. |
| **Peso no log (`e^peso − 1`)** | Quando a regressão usa o log da métrica, cada peso vira uma variação em %: `e^peso − 1`. | Em vez de "+R$ 2", dizer "+10% no preço". |
| **R²** | De 0 a 1: quanto da variação a regressão explica. | 0,74 = a fórmula explica 74% de por que uma nota é diferente da outra. |
| **Associação não é causa** | Duas coisas andarem juntas não prova que uma causa a outra. | Bombeiros aparecem em todos os incêndios, mas não causam incêndios. |
| **Teste A/B** | Experimento em que se sorteia quem vê a versão A e quem vê a B. | Dar o remédio a um grupo sorteado e placebo a outro. |
| **Funil** | O caminho do público: ver, clicar, converter. | Da vitrine (ver) à porta (clicar) e ao caixa (comprar). |

## Notebooks 1.3 e 1.4

| Termo | O que é | Analogia |
|---|---|---|
| **Comparação par a par** | Comparar as redes de duas em duas (Meta × TikTok, Meta × LinkedIn, TikTok × LinkedIn): efeito numa − efeito na outra, com intervalo de 95% pelo bootstrap. | Comparar os times de um campeonato em todos os confrontos, não só na final. |
| **Pontos percentuais (p.p.)** | A diferença entre duas porcentagens. De +30% para +50% são 20 p.p. | A inflação passou de 4% para 6%: subiu 2 pontos percentuais. |
| **Regra de bolso** | Regra simples, sem teste estatístico novo, para decidir se um efeito "funciona igual" nas redes: mesmo sinal nas três, confiável em pelo menos duas e nenhum par com diferença confiável. | Se três médicos diferentes dão o mesmo diagnóstico, dá para confiar. |
| **Manual por plataforma** | Lista dos atributos que mais sobem e mais derrubam a nota em cada rede. | Um guia de "faça e não faça" para cada rede social. |
| **`fig.savefig`** | Função do matplotlib que grava o gráfico num arquivo de imagem. | Tirar uma foto do gráfico para colar no slide. |
