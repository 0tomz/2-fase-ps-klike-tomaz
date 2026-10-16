# Pergunta 2.2: qual modelo usar, e por quê?

Notebook: [`notebooks/parte2/2_2_modelo.ipynb`](../../notebooks/parte2/2_2_modelo.ipynb). Modelos salvos em `models/`.

## Pergunta

Treine pelo menos um modelo de regressão. Explique sua escolha.

Um **modelo de regressão** aprende, com exemplos, uma regra que transforma as informações de um vídeo num número: aqui, a nota de 0 a 100.

## Resposta curta

Treinei três modelos e escolhi o mais simples, a **regressão linear**, porque ela errou menos e é a única que explica cada resultado em pontos de nota.

Antes de postar, ela erra em média **6,9 pontos**. Quem chutasse sempre a nota média erraria 12,8, quase o dobro. Os dois modelos mais sofisticados erraram mais, mesmo depois de ajustados: a Random Forest errou 7,5 e a rede neural, 8,1. Com 400 vídeos e efeitos que parecem simplesmente somar, o modelo simples ganha.

Testei também se valeria a pena ter um modelo separado para cada rede social. Não vale: um modelo único, que sabe a rede de cada vídeo, erra menos, principalmente no LinkedIn, que tem poucos vídeos.

## O que fiz, passo a passo

**1. Criei uma régua mínima.** Antes de qualquer modelo, medi quanto erra quem não usa modelo nenhum: chutar a nota média para todo vídeo, ou a nota média da rede social do vídeo. Um modelo só vale a pena se ganhar dessa régua com folga.

**2. Escolhi três candidatos bem diferentes:**

- **Regressão linear.** Soma um peso para cada característica: nota = base + peso do gancho (se tiver gancho) + peso do rosto (se tiver rosto) + ... É como uma receita, em que cada ingrediente acrescenta um tanto ao sabor. Cada peso se lê "quantos pontos isso vale, mantendo todo o resto igual".
- **Random Forest.** Junta centenas de **árvores de decisão**, sequências de perguntas de sim ou não ("tem gancho?" → "é TikTok?" → ...). Cada árvore aprende com um sorteio diferente dos vídeos, e a previsão final é a média de todas. É como perguntar a 300 especialistas que viram casos diferentes e tirar a média das opiniões. A vantagem é que ela encontra sozinha curvas e combinações, como "o gancho só ajuda se tiver rosto".
- **Rede neural.** Camadas de contas que aprendem sozinhas a forma da relação. É muito flexível, mas precisa de muitos exemplos, e funciona como uma caixa-preta.

**3. Ajustei a Random Forest e a rede neural antes de comparar.** Esses dois modelos têm escolhas que precisam ser feitas antes do treino, como o tamanho das árvores ou o número de camadas da rede. Testei várias combinações, sempre com as mesmas 15 provas do notebook 2.1, e fiquei com a melhor de cada. A regressão linear não tem nada a ajustar.

**4. Comparei os três** no Modelo A (só o que se sabe antes de postar) e no Modelo B (com os resultados da campanha).

**5. Testei um modelo por rede social contra um modelo único.** Em cada uma das 15 provas, treinei um modelo com as três redes juntas e três modelos separados, e medi o erro de cada rede.

**6. Treinei os modelos finais com os 400 vídeos e salvei** num arquivo, para a Parte 3 usar. Salvei também o peso de cada característica em pontos de nota.

## Por que fiz assim

**A regressão linear era minha aposta antes de rodar,** por três motivos: são só 400 vídeos; na Parte 1, os efeitos pareciam simplesmente somar (gancho, rosto, texto); e a Parte 3 precisa dizer "ter gancho vale +18 pontos", algo que só a regressão linear dá direto.

**Testei a Random Forest e a rede neural para conferir essa aposta.** Se a relação tivesse curvas ou combinações importantes, elas ganhariam. Não ganharam, e isso confirma que, nestes dados, os efeitos somam de forma simples.

**Ajustei os dois concorrentes antes de comparar**, porque a comparação só é justa se cada modelo estiver no seu melhor.

**A escolha é segura.** Como a regressão linear não tem ajuste, não há risco de eu ter escolhido uma configuração que só funcionou por sorte nestas 15 provas. O teste final (notebook 2.3) confirmou o número: 6,7 pontos de erro em vídeos que o modelo nunca viu.

## O que descobri

Erro médio na avaliação, em pontos de nota (quanto menor, melhor):

| | Antes de postar (Modelo A) | Com os resultados (Modelo B) |
|---|---|---|
| chutar a nota média | 12,8 | 12,8 |
| **regressão linear** | **6,9** | **5,6** |
| Random Forest | 7,5 | 6,5 |
| rede neural | 8,1 | 7,2 |

A Random Forest errou 9% mais que a regressão linear antes de postar e 15% mais com os resultados. A rede neural errou 18% e 29% mais. O melhor tamanho de rede foi uma camada de 64 "neurônios"; com duas camadas, ela piorou. Mais flexibilidade não ajuda com poucos exemplos.

O modelo único ganhou dos modelos por rede no TikTok (6,9 contra 7,2) e principalmente no LinkedIn (7,9 contra 8,8), e empatou no Meta. O LinkedIn tem só cerca de 53 vídeos em cada rodada de treino, pouco para um modelo próprio. O modelo único "empresta" a ele o que aprendeu nas outras redes. Isso confirma a Parte 1: o que funciona é quase igual nas três redes.

Os maiores pesos da regressão, em pontos de nota:

- gancho: +17,9;
- muito texto, em vez de médio: −15,1;
- rosto: +11,5;
- só música, sem voz, no TikTok: −11,5;
- legenda: +8,1;
- chamada para ação: +7,5.

## Limites

Duas colunas andam juntas: "é TikTok" e "música no TikTok". Quando isso acontece, a regressão linear não sabe direito a qual das duas dar o crédito, e o peso da música no TikTok varia de uma prova para outra (de −8,3 a −14,9 pontos, como mostra o notebook 2.4). Os outros pesos são estáveis.

Com cerca de 53 vídeos do LinkedIn por rodada, não dá para afirmar diferenças finas dessa rede. A Random Forest e a rede neural poderiam ganhar com muito mais dados, ou com informações que descrevessem combinações reais. Com 400 vídeos simulados, não ganham.
