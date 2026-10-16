# Pergunta 1.3: existem padrões diferentes por plataforma?

Notebook: [`notebooks/parte1/1_3_padroes_por_plataforma.ipynb`](../../notebooks/parte1/1_3_padroes_por_plataforma.ipynb). Termos em [`docs/glossario.md`](../glossario.md).

## Pergunta

Existem padrões diferentes por plataforma? O que funciona no TikTok funciona no LinkedIn (por exemplo)?

O "TikTok × LinkedIn" é só um exemplo. A pergunta é geral, então comparo **as três plataformas da base (Meta, TikTok e LinkedIn) e os três pares** (Meta × TikTok, Meta × LinkedIn, TikTok × LinkedIn), sem privilegiar nenhum.

## Resposta curta

**Sim, existem padrões diferentes, mas eles estão em como cada rede é, e pouco no que funciona nela.**

- **O contexto muda muito de rede para rede:**
  - CPC de R$0,51 no TikTok, R$0,80 no Meta e R$2,49 no LinkedIn;
  - CPA (custo por conversão) de R$15,9 no TikTok, R$24,2 no Meta e R$70,2 no LinkedIn. A taxa de conversão é a mesma nas três (cerca de 3,3%): a conversão no LinkedIn custa mais porque o clique é mais caro, não porque converte menos;
  - o TikTok engaja quase o dobro;
  - ROAS (sem Branding) de 2,9 no TikTok, 1,9 no Meta e 0,6 no LinkedIn;
  - o TikTok é vertical e curto; o LinkedIn, horizontal ou quadrado e mais longo.
- **O que funciona é quase o mesmo nas três:** gancho (cerca de +17 pontos de nota), rosto (+9 a +12) e evitar muito texto (−12 a −16). Comparando os efeitos par a par, **só 1 de 72 diferenças entre redes é confiável**, menos do que o acaso daria.
- **As diferenças que apareceram (indícios):**

| Par | O que muda |
|---|---|
| Meta × TikTok | **voz:** tirar a voz custa cerca de 12 pontos a mais no TikTok; **rosto:** segura a retenção no Meta (+32%), não no TikTok (−6%) |
| Meta × LinkedIn | **gancho:** pesa um pouco mais no LinkedIn (+24,7 contra +17,1 pontos, no limite do confiável) |
| TikTok × LinkedIn | nenhuma diferença confiável no efeito dos atributos (o LinkedIn tem poucos criativos) |

- **Para o exemplo do case:** o que funciona no TikTok funciona no LinkedIn na **direção**. Não achei diferença confiável nesse par, mas é o par com menos criativos para detectar diferenças finas.

## O que fiz, passo a passo

1. **Perfil de cada rede:**
   - mediana de custo (CPM, CPC, CPA), CTR, engajamento, retenção, taxa de conversão, ROAS (sem Branding) e nota;
   - **eta²** (quanto da variação se explica só por saber a plataforma);
   - `crosstab` do que cada rede veicula.
2. **Efeito de cada atributo dentro de cada rede:**
   - a diferença das medianas com e sem o atributo, com intervalo de 95% por bootstrap (como na pergunta 1.2);
   - quatro métricas: CTR, engajamento, retenção e nota;
   - heatmap atributo × rede, com o n de cada célula; células com menos de 15 criativos ficam em branco;
   - dois atributos viraram sim/não: "muito texto" e "mais música que voz" (música/voz acima de 0,5).
3. **O efeito muda de uma rede para outra? (par a par)**
   - para cada atributo, métrica e par de redes: efeito na rede A − efeito na rede B;
   - o intervalo de 95% vem dos mesmos sorteios do bootstrap: em cada sorteio, subtraio um efeito do outro;
   - diferença confiável = o intervalo inteiro de um lado do zero.
4. **"Funciona igual?"** juntando os passos 2 e 3 numa regra de bolso:
   - **funciona igual nas 3:** mesmo sinal nas três, confiável em pelo menos duas, e nenhum par com diferença confiável;
   - **mesma direção, força diferente:** mesmo sinal nas três, mas algum par com diferença confiável;
   - **funciona diferente:** confiável numa rede e com sinal oposto em outra;
   - **não dá para afirmar:** o resto.
   
   Depois, a **regressão linear dentro de cada rede** (a mesma da pergunta 1.2, com menos colunas de contexto), e a comparação dos pesos par a par, do mesmo jeito do passo 3.
5. **Duração por rede:** mediana por faixa de duração.
6. **Formato por rede:** cada par de formatos dentro de cada rede (quando os dois têm 15 criativos ou mais).
7. **Texto por rede:** mediana por nível de texto.
8. **Manual por plataforma:** os 3 atributos que mais sobem a nota e os 2 que mais derrubam. Salvei a tabela completa em `data/processed/efeitos_por_plataforma.csv`.

## Por que fiz assim

- **Comparar todos os pares** responde à pergunta geral. Olhar só TikTok × LinkedIn deixaria de fora o Meta, a rede com mais criativos e, portanto, a mais bem medida.
- **Testar a diferença entre os efeitos, e não só cada efeito:** "o rosto é confiável no TikTok e não no LinkedIn" não quer dizer que o rosto funciona diferente nas duas. Pode ser só que o LinkedIn tem menos criativos. Para afirmar que um efeito muda, o intervalo da **diferença** precisa ficar de um lado do zero.
- **A regressão por rede** foi necessária porque a comparação simples mistura atributos. Exemplo: "mais música que voz" no TikTok dava só −3,8 pontos na comparação simples; na regressão, mantendo o resto igual, aparece −13,4.
- **O limite de 15 criativos** evita conclusões com grupos minúsculos, que mudam muito por acaso.

## O que descobri

- **Custo:** CPM mediano de R$131 no LinkedIn, R$49 no Meta e R$27 no TikTok. A plataforma explica 77% da variação do CPC.
- **CTR quase igual nas três** (6,0% a 6,6%). Engajamento do TikTok: 3,2%, contra 1,6% a 1,8% nas outras.
- **Taxa de conversão igual nas três** (3,2% a 3,3%; eta² 0,00). Já o CPA vai de R$15,9 (TikTok) a R$70,2 (LinkedIn), cerca de 4,4 vezes: a diferença vem do custo do clique.
- **Efeito de cada atributo, rede a rede:**
  - gancho: nota +17 a +18, retenção +32% a +42% e CTR +53% a +133%, nas três;
  - rosto: nota +9 a +12 nas três;
  - muito texto: nota −12 a −16 e retenção −9% a −33%, nas três;
  - CTA e legenda: sobem a nota nas três, mas só são confiáveis no Meta.
- **Par a par (medianas):** de 72 comparações, só o rosto na retenção (Meta × TikTok) muda de forma confiável. Os intervalos das diferenças são largos (cerca de 90 pontos percentuais no par Meta × TikTok e cerca de 130 nos pares com o LinkedIn): só diferenças grandes seriam detectadas.
- **Na regressão por rede:**
  - gancho +17 a +25 pontos, rosto +10 a +13, muito texto −13 a −20, nas três;
  - **voz:** só música, sem voz, dá −13,4 no TikTok, −1,2 no Meta e −1,8 no LinkedIn. A diferença Meta × TikTok (12,2 pontos, intervalo de 0,4 a 23,9) é confiável;
  - **gancho:** +24,7 no LinkedIn contra +17,1 no Meta (diferença de 7,6, intervalo de 0,5 a 16,4, no limite);
  - 2 de 21 comparações confiáveis; cerca de 1 sairia por acaso, então trato as duas como indícios.
- **Sem duração ideal por rede:** a "melhor faixa" muda de uma métrica para outra, e os grupos são pequenos.
- **Formato:** das 15 comparações possíveis, só 1 é confiável: no Meta, o vertical engaja 57% mais que o horizontal. Na nota e no CTR, nenhum formato ganha de outro em nenhuma rede. "Vertical × horizontal" não pode ser testado no TikTok (não há horizontal) nem no LinkedIn (só 9 verticais).
- **Texto:** muito texto derruba a nota nas três redes; no CTR, só a queda do Meta (−32%) é confiável.

**Manual por plataforma:**

| Rede | Fazer | Evitar |
|---|---|---|
| Meta | gancho (+18,3 pts), rosto (+12,2), CTA (+7,5) | muito texto (−14,2) |
| TikTok | gancho (+17,0), rosto (+8,8), legenda (+5,1) | muito texto (−16,5); só música, sem voz (−13,4 na regressão) |
| LinkedIn | gancho (+17,3), rosto (+11,8), legenda (+10,9) | muito texto (−11,8) |

Para a Parte 3: o motor de recomendações pode partir de regras comuns às três redes e somar poucos ajustes por rede (a voz no TikTok).

## Limites

- **Não achar diferença não prova que os efeitos são iguais:** com estes tamanhos, só diferenças grandes seriam detectadas.
- **LinkedIn com 66 criativos** (53 com dados completos na regressão): os pares com o LinkedIn quase não conseguem detectar diferenças; os números dele são direção, não estimativa precisa.
- **Muitas comparações:** com 72 (medianas) e 21 (regressão), algumas sairiam "confiáveis" por acaso. Por isso, as diferenças encontradas são indícios.
- **Células vazias ou pequenas** (TikTok sem horizontal, LinkedIn com 9 verticais) impedem algumas comparações.
- **Dados observados e simulados:** associação, não causa.
