# Klike.ai — Data Science Challenge

Este repositório traz as quatro partes do case. Cada uma tem um texto explicativo em `docs/`, com as decisões e o porquê de cada uma, e um notebook em `notebooks/`, com o código passo a passo.

## O que fazer no próximo vídeo

Comparando vídeos parecidos em todo o resto, na nota Klike (de 0 a 100):

1. **Gancho nos 3 primeiros segundos:** vídeos com gancho têm cerca de **18 pontos** a mais, e cerca de 50% mais cliques.
2. **Texto na tela na medida certa:** vídeos com muito texto têm cerca de **15 pontos** a menos, e os com pouco texto, cerca de 8 a menos.
3. **Rosto humano:** vídeos com rosto têm cerca de **12 pontos** a mais.
4. **Legenda e chamada para ação no fim:** cerca de **8 pontos** a mais cada.
5. **No TikTok, voz:** lá, vídeos só com música e sem voz têm cerca de **11 pontos** a menos (o número exato é incerto: de 8 a 15). Nas outras redes, a música não faz diferença.

## Como ler os números

- **Pontos de nota:** diferenças na nota Klike, que vai de 0 a 100. "+18 pontos" é a distância entre, por exemplo, 49 e 67.
- **"Comparando vídeos parecidos":** o número vem de uma regressão linear, uma conta que compara vídeos iguais em todo o resto (rede, público, objetivo, outros atributos) e isola o efeito de uma característica. Quando um número vem de uma **comparação simples** (a mediana de quem tem contra a de quem não tem, sem controlar mais nada), o texto diz isso.
- **"Confiável":** o resultado se repete quando a amostra varia. Para saber, refiz cada conta milhares de vezes com sorteios dos mesmos vídeos e olhei se o efeito ficava sempre do mesmo lado do zero.

## Quão confiável é isto

O modelo que prevê a nota antes de postar erra, em média, cerca de 7 pontos numa escala de 0 a 100. Os números acima mostram o que **anda junto** com uma nota maior, e não o que **causa** uma nota maior: provar causa exigiria um teste A/B, com o mesmo anúncio em duas versões para públicos sorteados. Os dados são simulados, e a nota parece ter sido gerada somando o efeito de cada atributo; com dados reais, os efeitos devem ser menores e menos limpos. Quando um número foi medido em poucos vídeos, os textos dizem isso e mostram a faixa em vez de um valor exato.

## Principais resultados

**Exploração dos dados.** O gancho é o atributo que mais anda junto com nota alta, seguido do rosto e do texto na medida. As redes diferem muito em custo (um clique no LinkedIn custa cerca de cinco vezes o do TikTok), mas o que funciona é quase igual nas três; a exceção é a voz no TikTok. Vídeos com gancho têm mais cliques, mas não convertem mais; as campanhas de retargeting é que convertem mais e mais barato. Antes da análise, 10 linhas com números digitados errado foram encontradas e corrigidas. [Textos da Parte 1](docs/parte1/)

**Modelo.** A regressão linear, o mais simples dos três modelos testados, foi o que menos errou. Usando só o que existe antes de postar, ela erra 6,7 pontos nos 100 vídeos guardados para o teste, contra 11,7 de quem chutasse a nota média. Em 3 de cada 4 vídeos, a previsão fica a até 10 pontos da nota real. Um modelo que também vê os cliques e as vendas erra só 1 ponto a menos: o vídeo sozinho já explica quase toda a nota. [Textos da Parte 2](docs/parte2/)

**Motor de recomendações.** Funciona como um simulador de "e se": muda uma coisa no vídeo, pergunta ao modelo qual seria a nota e entrega as três mudanças de maior ganho. Mostra também a faixa do efeito na métrica da campanha, quando ela é confiável, e sugere o retargeting à parte, porque é uma decisão de público. O ganho na nota é quase o mesmo em todas as redes; o contexto entra pela voz no TikTok, pela métrica mostrada e pelos formatos que cada rede usa. [Texto da Parte 3](docs/parte3/3_motor_de_recomendacoes.md)

**Visão de produto.** O próximo passo de maior valor é medir a qualidade do vídeo, e não só a presença de cada atributo: para o modelo de hoje, um gancho fraco e um excelente valem o mesmo. A primeira prioridade em produção seria um teste A/B para saber se seguir as recomendações realmente melhora as campanhas. [Texto da Parte 4](docs/parte4/4_visao_de_produto.md)

## As figuras

**Vídeos com gancho têm a maior vantagem.** Na nota, nos cliques e no engajamento, o gancho fica à frente de todos os outros atributos, e o excesso de texto é o que mais pesa contra (comparação simples).

![Vídeos com gancho têm a maior vantagem na nota, no CTR e no engajamento](reports/figures/fig1_o_que_mover_no_criativo.png)

**O básico vale nas três redes.** Cada célula é quantos pontos de nota o atributo soma naquela rede, comparando vídeos parecidos; em cinza, o que pode ser acaso. Só a voz muda: ela só pesa no TikTok.

![Gancho, rosto e texto na medida valem nas três redes; a voz só pesa no TikTok](reports/figures/fig2_o_que_funciona_em_cada_rede.png)

**Mais cliques não é mais vendas.** Vídeos com gancho têm mais cliques e mais retenção, mas não convertem mais; as campanhas de retargeting convertem mais e mais barato (comparação simples; em cinza, o que pode ser acaso).

![Vídeos com gancho têm mais cliques, mas não mais vendas; o retargeting vende mais barato](reports/figures/fig3_o_video_decide_o_clique.png)

**O que mais pesa na nota, em pontos.** Os efeitos do modelo final, comparando vídeos parecidos.

![Gancho, rosto e texto na medida certa são o que mais muda a nota](reports/figures/parte2_fig1_o_que_pesa_na_nota.png)

**O vídeo pesa mais que a campanha.** Quanto o erro do modelo aumenta quando cada informação é embaralhada: as do vídeo (em azul) vêm todas antes das da campanha.

![O que está no vídeo pesa mais que a campanha em que ele roda](reports/figures/parte2_fig2_video_pesa_mais_que_campanha.png)

## Como rodar

É preciso ter o **Python 3.11 ou mais novo** (o projeto foi feito com o 3.11.9). Todos os comandos rodam na pasta principal do repositório. Primeiro, crie o ambiente e instale as bibliotecas:

```bash
python -m venv venv
venv\Scripts\activate          # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

Depois, rode todos os notebooks de uma vez. Leva cerca de 20 minutos:

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/parte1/*.ipynb notebooks/parte2/*.ipynb notebooks/parte3/*.ipynb
```

A ordem importa, e o comando já a respeita: o notebook 1.3 salva a tabela de efeitos por rede social que o motor da Parte 3 usa, e o 2.2 salva os modelos que o 2.3, o 2.4 e a Parte 3 usam. Os notebooks já vêm executados no repositório, então dá para ler os resultados sem rodar nada.

Para receber as recomendações de uma campanha pela linha de comando, use o código dela:

```bash
python -m src.recomendacoes KLK-0479
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
