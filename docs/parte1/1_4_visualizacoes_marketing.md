# Pergunta 1.4: visualizações para o time de marketing

Notebook: [`notebooks/parte1/1_4_visualizacoes_marketing.ipynb`](../../notebooks/parte1/1_4_visualizacoes_marketing.ipynb). Figuras em `reports/figures/`.

## Pergunta

Crie pelo menos 3 visualizações que você usaria para apresentar insights a um time de marketing.

## Resposta curta

Fiz três figuras. Cada uma responde a uma pergunta que o time de marketing faria, e juntas elas contam uma história completa.

A **primeira** responde "o que eu mudo no próximo vídeo?". Ela mostra que o gancho nos 3 primeiros segundos é o que mais sobe a nota (+17,6 pontos), os cliques (+66%) e o engajamento (+56%). Mostra também que muito texto na tela vai na direção contrária.

A **segunda** responde "isso vale em todas as redes?". O gancho e o rosto sobem a nota no Meta, no TikTok e no LinkedIn, e o excesso de texto derruba nas três. O rodapé traz a única exceção: no TikTok, a voz importa.

A **terceira** responde "o criativo vende?". O gancho sobe os cliques e a retenção, mas não muda a taxa de conversão, o custo por venda nem o retorno. Quem mexe na venda é o público: para quem já conhece a marca, a conversão é 89% maior e cada venda sai 44% mais barata.

## O que fiz

Os números das figuras são os mesmos das perguntas 1.2 e 1.3: a diferença entre a mediana dos vídeos com e sem cada atributo, refeita dentro do notebook. Usei gráficos simples, de barras e de mapa de calor (uma tabela em que a cor mostra o tamanho do número). Cada figura é salva como imagem, pronta para um slide. Embaixo de cada uma, no notebook, escrevi como eu a apresentaria ao time.

## Por que estas três

Eu tinha feito outras três figuras e tirei, porque elas repetiam algo destas ou mostravam um resultado que cabe numa frase:

- a da duração mostrava que não existe duração ideal, um resultado negativo;
- a do checklist de boas práticas somava atributos que pesam diferente (o gancho vale bem mais que a legenda), e o peso de cada um já está na primeira figura;
- a do texto na tela por rede repetia o que as figuras 1 e 2 já mostram.

## Por que fiz assim

**O título de cada figura é a conclusão, e não a descrição.** "O gancho é o que mais sobe a nota" diz o que levar para casa; "nota por gancho" obriga a pessoa a descobrir sozinha.

**Não há termos técnicos nos títulos.** O rodapé diz quantos vídeos foram usados e de onde vêm os dados.

**As cores seguem uma regra.** Cada rede tem sempre a mesma cor (Meta azul, TikTok laranja, LinkedIn verde). O que importa aparece em destaque, e o resto em cinza, para o olho ir direto à mensagem.

**Os valores estão escritos nas barras,** com letras grandes o bastante para um slide, e ninguém precisa ler o eixo.

**Não há barras de erro.** Para quem não é técnico, elas confundem mais do que ajudam. A incerteza aparece em palavras no rodapé ou na cor: na terceira figura, o que pode ser acaso fica em cinza claro.

## O que descobri ao montar as figuras

**A primeira figura começa pela nota, não pelos cliques.** A nota é o que a Klike quer prever e resume o caminho inteiro do cliente. Os cliques e o engajamento vêm ao lado, porque são as métricas que o marketing já acompanha.

**A segunda mostra que não é preciso um manual diferente para cada rede.** O básico vale nas três.

**A terceira muda a conversa sobre o que cobrar do vídeo.** O criativo é a vitrine: ele decide se a pessoa para e entra na loja. Se ela compra depende da oferta e de quem ela é. A única coisa do vídeo que atrapalha até a venda é o excesso de texto.

## Limites

As figuras mostram comparações simples entre medianas. Os resultados da conta "mantendo o resto igual" aparecem só nos rodapés: o efeito da música no TikTok, na figura 2, e os efeitos ajustados no funil, na figura 3. E, como em toda a Parte 1, é o que anda junto, não necessariamente o que causa. Para ter certeza de que o gancho causa o aumento, o marketing poderia fazer um teste A/B.
