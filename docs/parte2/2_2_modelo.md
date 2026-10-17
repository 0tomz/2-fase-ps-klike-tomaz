# 2.2 Qual modelo usar, e por quê?

> Pergunta do case: treine pelo menos um modelo de regressão. Explique sua escolha.
>
> Notebook: [`2_2_modelo.ipynb`](../../notebooks/parte2/2_2_modelo.ipynb) · Modelos salvos em `models/`

## Resposta curta

Treinei três modelos e escolhi o mais simples, a **regressão linear**: ela errou menos e é a única que explica cada resultado em pontos de nota. Antes de postar, ela erra em média **6,9 pontos**, contra 12,8 de quem chutasse sempre a nota média. A Random Forest errou 7,5 e a rede neural, 8,1, mesmo depois de ajustadas. Com 400 vídeos e efeitos que parecem simplesmente somar, o modelo simples ganha. Também testei um modelo separado para cada rede social, e um modelo único erra menos.

## Por que isso importa

O modelo escolhido é transparente: dá para dizer "vídeos com gancho têm cerca de 18 pontos a mais, comparando vídeos parecidos", e é isso que permite ao motor da Parte 3 sugerir mudanças com número. Um modelo mais sofisticado poderia até prever um pouco melhor com muito mais dados, mas aqui ele erraria mais e não diria o porquê.

## Como cheguei lá

**Criei uma régua mínima.** Antes de qualquer modelo, medi quanto erra quem não usa modelo nenhum: chutar a nota média para todo vídeo (12,8 pontos de erro) ou a média da rede social (12,7). Um modelo só vale a pena se ganhar dessa régua com folga.

**Escolhi três modelos bem diferentes:**

- **Regressão linear:** soma um peso para cada característica, como uma receita em que cada ingrediente acrescenta um tanto ao sabor. Cada peso se lê "quantos pontos isso vale, comparando vídeos parecidos".
- **Random Forest:** junta centenas de árvores de perguntas de sim ou não ("tem gancho?" → "é TikTok?"), cada uma aprendendo com um sorteio diferente dos vídeos, e tira a média delas. É como perguntar a 300 especialistas. A vantagem é achar sozinha curvas e combinações.
- **Rede neural:** camadas de contas muito flexíveis, que precisam de muitos exemplos e funcionam como uma caixa-preta.

A regressão linear era a minha aposta, porque são só 400 vídeos e, na Parte 1, os efeitos pareciam simplesmente somar. Os outros dois servem para conferir a aposta: se a relação tivesse curvas ou combinações importantes, eles ganhariam.

**Ajustei os concorrentes antes de comparar.** A Random Forest e a rede neural têm escolhas que precisam ser feitas antes do treino, como o tamanho das árvores ou o número de camadas. Testei várias combinações e fiquei com a melhor de cada, sempre nas mesmas 15 provas da validação cruzada (o "estudar com 15 simulados" do 2.1). A comparação só é justa com cada modelo no seu melhor.

Erro médio na avaliação, em pontos de nota:

| | Antes de postar (Modelo A) | Com os resultados (Modelo B) |
|---|---|---|
| chutar a nota média | 12,8 | 12,8 |
| **regressão linear** | **6,9** | **5,6** |
| Random Forest | 7,5 | 6,5 |
| rede neural | 8,1 | 7,2 |

A melhor rede neural tinha uma camada só; com duas, ela piorou. Mais flexibilidade não ajuda com poucos exemplos. A regressão linear também não tem nenhum ajuste, então não há risco de eu ter escolhido uma configuração que só funcionou por sorte nestas provas.

**Um modelo único ganha de um por rede.** O modelo com as três redes juntas erra menos no TikTok (6,9 contra 7,2) e principalmente no LinkedIn (7,9 contra 8,8), e empata no Meta. O LinkedIn tem só cerca de 53 vídeos em cada rodada de treino, pouco para um modelo próprio; o modelo único "empresta" a ele o que aprendeu nas outras redes.

**Os maiores pesos**, em pontos de nota, comparando vídeos parecidos: gancho +18, muito texto −15, rosto +12, legenda +8, chamada para ação +8 e pouco texto −8. No TikTok, vídeos só com música têm cerca de 11 pontos a menos (de 8 a 15, como explico nos limites). Os modelos finais ficaram salvos para o 2.3, o 2.4 e a Parte 3 usarem sem treinar de novo.

## Limites

Duas informações andam juntas: "é TikTok" e "música no TikTok". Quando isso acontece, a regressão não sabe direito a qual das duas dar o crédito, e o peso da música no TikTok varia de uma prova para outra (de −8 a −15 pontos). Os outros pesos são estáveis. Com tão poucos vídeos do LinkedIn, não dá para afirmar diferenças finas dessa rede.
