# Pergunta 1.4: visualizações para o time de marketing

Notebook: [`notebooks/parte1/1_4_visualizacoes_marketing.ipynb`](../../notebooks/parte1/1_4_visualizacoes_marketing.ipynb). Figuras em `reports/figures/`.

## Pergunta

Crie pelo menos 3 visualizações que você usaria para apresentar insights a um time de marketing.

## Resposta curta

Três figuras, cada uma respondendo a uma pergunta diferente do time de marketing:

| Figura | A pergunta do marketing | A mensagem |
|---|---|---|
| 1. O que mover no criativo | O que eu mudo no próximo vídeo? | O gancho nos 3 primeiros segundos é o que mais sobe a nota (+17,6 pontos), o CTR (+66%) e o engajamento (+56%); muito texto derruba |
| 2. O que funciona em cada rede | Isso vale em todas as redes? | Gancho e rosto sobem a nota nas três redes; muito texto derruba nas três; no TikTok, voz importa |
| 3. O vídeo decide o clique | O criativo vende? | O gancho sobe CTR e retenção, mas não a venda; quem mexe na conversão, no CPA e no ROAS é o público (retargeting) |

## O que fiz

- **Os números das figuras são os mesmos das perguntas 1.2 e 1.3** (diferença das medianas com e sem cada atributo), refeitos dentro do notebook.
- **Gráficos simples:** barras horizontais e heatmaps, com matplotlib e seaborn.
- **Cada figura é salva com `fig.savefig`** em `reports/figures/`, para usar em slides.
- **Embaixo de cada figura**, escrevi como eu apresentaria aquilo ao time de marketing.

## Por que estas três

- **Juntas, elas contam uma história completa:** o que mudar (1), onde vale (2) e até onde o vídeo pesa no resultado (3).
- **Cada uma resume uma pergunta do case:** a 1 e a 3 vêm da pergunta 1.2, e a 2 vem da 1.3.
- **Ficaram de fora três figuras que eu tinha feito:**
  - **duração:** "não há duração ideal" é um resultado negativo, que cabe numa frase;
  - **checklist de boas práticas:** soma atributos que pesam diferente (o gancho vale bem mais que a legenda), e o peso de cada um já está na figura 1;
  - **texto na tela por rede:** muito texto já aparece nas figuras 1 e 2.

## Por que fiz assim

- **O título é a conclusão**, e não a descrição. O público lê o título e já sabe o que levar para casa.
- **Sem termos técnicos no título.** O rodapé diz quantos criativos e de onde vem o dado.
- **Cores:**
  - **a mesma cor para cada plataforma em todo o projeto** (Meta azul, TikTok laranja, LinkedIn verde);
  - o que importa vem em uma cor, e o resto em cinza: o olho vai direto para a mensagem.
- **Valores escritos nas barras e nas células:** ninguém precisa ler o eixo.
- **Fontes de 11 pt ou mais:** legíveis num slide.
- **Sem barras de erro:** para marketing, a incerteza vai no rodapé ou na cor (na figura 3, cinza claro = pode ser acaso).

## O que descobri ao montar as figuras

- **A figura 1 abre pela nota, não pelo CTR:** a nota é o alvo da Parte 2 e resume o funil inteiro. O CTR e o engajamento vêm ao lado, porque são as métricas que o marketing já acompanha.
- **A figura 2 mostra que o básico vale nas três redes:** gancho, rosto e evitar muito texto têm o mesmo sinal em todas. O rodapé traz a exceção da regressão: no TikTok, vídeo só com música e sem voz perde cerca de 13 pontos.
- **A figura 3 responde à pergunta "o criativo vende?":**
  - o gancho sobe o CTR em 66% e a retenção em 42%, mas não muda a taxa de conversão, o custo por conversão nem o ROAS;
  - o público de retargeting converte 89% mais, com conversão 44% mais barata e ROAS 66% maior;
  - só as células confiáveis são pintadas; as outras ficam em cinza claro.

## Limites

- **As figuras mostram comparações simples (medianas).** As exceções vêm da regressão e aparecem só no rodapé: o efeito da música no TikTok (figura 2) e os efeitos ajustados no funil (figura 3).
- **Associação não é causa:** para garantir que o gancho causa o aumento, o marketing poderia rodar um teste A/B.
