# Klike.ai — Data Science Challenge

Este repositório traz as quatro partes do case. Cada uma tem um texto explicativo em `docs/`, com as decisões e o porquê de cada uma, e um notebook em `notebooks/`, com o código passo a passo. Abaixo estão os principais resultados, as figuras, como rodar o projeto e como ele está organizado.

## Principais resultados

**Exploração dos dados.** O atributo que mais pesa é o gancho nos 3 primeiros segundos: vídeos com gancho têm nota cerca de 17 pontos maior, mesmo comparando com vídeos parecidos em todo o resto. Depois vêm o rosto humano e a quantidade de texto na tela, que tem um ponto ideal no meio. As redes diferem muito em custo, mas o que funciona é quase igual nas três; a exceção é a voz, que importa no TikTok. E o vídeo decide se a pessoa para e clica, mas quase não decide se ela compra: a venda depende mais de quem vê o anúncio. Antes da análise, 10 linhas com números digitados errado foram encontradas e corrigidas. [Textos da Parte 1](docs/parte1/)

**Modelo.** A regressão linear, o mais simples dos três modelos testados, foi o que menos errou. Usando só o que existe antes de postar, ela erra em média 6,7 pontos nos 100 vídeos guardados para o teste, contra 11,7 de quem chutasse a nota média. Em 3 de cada 4 vídeos, a previsão fica a até 10 pontos da nota real. Um modelo que também vê os cliques e as vendas erra só 1 ponto a menos, ou seja, o vídeo sozinho já explica quase toda a nota. [Textos da Parte 2](docs/parte2/)

**Motor de recomendações.** Funciona como um simulador de "e se": muda uma coisa no vídeo, pergunta ao modelo qual seria a nova nota e entrega as três mudanças de maior ganho, considerando a rede e o objetivo da campanha. Por exemplo: "Adicionar um gancho nos 3 primeiros segundos pode aumentar a nota em ~18 pontos (de 49 para 67) e o CTR em ~133% no LinkedIn". Nas 100 campanhas de teste, as que ele aponta com mais espaço para melhorar são justamente as de nota real mais baixa. [Texto da Parte 3](docs/parte3/3_motor_de_recomendacoes.md)

**Visão de produto.** O próximo passo de maior valor é medir a qualidade do vídeo, e não só a presença de cada atributo: um gancho fraco e um excelente valem o mesmo para o modelo de hoje. Em produção, o motor aprenderia com os resultados reais das campanhas, e a primeira prioridade seria um teste A/B para provar que as recomendações causam a melhora. [Texto da Parte 4](docs/parte4/4_visao_de_produto.md)

Uma ressalva vale para tudo: os dados são simulados e observados, então os resultados mostram o que anda junto, não necessariamente o que causa.

## As figuras

As três primeiras são as figuras para o time de marketing (Parte 1). As duas últimas resumem o modelo (Parte 2).

![O gancho é o que mais sobe a nota, o CTR e o engajamento](reports/figures/fig1_o_que_mover_no_criativo.png)

![O básico funciona nas três redes; no TikTok, voz importa](reports/figures/fig2_o_que_funciona_em_cada_rede.png)

![O vídeo decide o clique; a venda depende de quem vê](reports/figures/fig3_o_video_decide_o_clique.png)

![Gancho, rosto e texto na medida certa são o que mais muda a nota](reports/figures/parte2_fig1_o_que_pesa_na_nota.png)

![O que está no vídeo pesa mais que a campanha em que ele roda](reports/figures/parte2_fig2_video_pesa_mais_que_campanha.png)

## Como rodar

É preciso ter o **Python 3.11 ou mais novo** (o projeto foi feito com o 3.11.9). Todos os comandos rodam na pasta principal do repositório. Primeiro, crie o ambiente e instale as bibliotecas:

```bash
python -m venv venv
venv\Scriptsctivate          # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

Depois, rode todos os notebooks de uma vez:

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/parte1/*.ipynb notebooks/parte2/*.ipynb notebooks/parte3/*.ipynb
```

A ordem importa, e o comando já a respeita:

- o notebook 1.3 salva a tabela de efeitos por rede social que o motor da Parte 3 usa;
- o 2.2 salva os modelos que o 2.3, o 2.4 e a Parte 3 usam.

Os notebooks já vêm executados no repositório, então dá para ler os resultados sem rodar nada.

Para receber as recomendações de uma campanha pela linha de comando, use o código dela:

```bash
python -m src.recomendacoes KLK-0123
```

Para conferir se o código está funcionando, cada arquivo de `src/` tem uma autoconferência:

```bash
python -m src.limpeza
```

O mesmo vale para `src.features`, `src.avaliacao` e `src.recomendacoes` (este último, sem o código de campanha).

## Como o repositório está organizado

- `docs/` guarda os textos explicativos, um por pergunta, em `parte1/` a `parte3/`. A Parte 4 é só texto e reúne as três respostas num arquivo único, em `parte4/`.
- `notebooks/` guarda os notebooks, um por pergunta, em `parte1/` a `parte3/`. A Parte 4 não tem notebook, porque não tem código.
- `src/` guarda o código reaproveitado pelos notebooks:
  - a limpeza (`limpeza.py`);
  - a preparação das informações para o modelo (`features.py`);
  - as métricas de avaliação (`avaliacao.py`);
  - o motor de recomendações (`recomendacoes.py`).
- `data/raw/` guarda o arquivo original do case, que nunca é alterado.
- `data/processed/` guarda a tabela de efeitos de cada atributo por rede social, gerada pelo notebook 1.3 e usada pelo motor da Parte 3. Os dados limpos não são salvos: cada notebook aplica `src/limpeza.py` ao arquivo original, para todos usarem sempre a mesma limpeza.
- `models/` guarda os dois modelos treinados: o pré-lançamento e o completo (notebook 2.2).
- `reports/figures/` guarda as cinco figuras: três da Parte 1 e duas da Parte 2.
