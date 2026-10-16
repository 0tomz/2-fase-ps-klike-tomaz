# Klike.ai — Data Science Challenge

O projeto tem quatro partes, cada uma numa pasta dentro de `notebooks/`: `notebooks/parte1/` (EDA), `notebooks/parte2/`, `notebooks/parte3/` e `notebooks/parte4/`. A limpeza reaproveitável fica em `src/limpeza.py`, os dados em `data/` e as explicações em `docs/`.

## Parte 1 — EDA

Quatro notebooks em [`notebooks/parte1/`](notebooks/parte1/), um por pergunta do case, já executados. Cada notebook roda sozinho e mostra o raciocínio passo a passo. Todos usam a mesma divisão treino/teste e a mesma limpeza, então os números batem entre eles.

| Pergunta | Notebook | Explicação |
|---|---|---|
| 1.1 Perfil geral dos dados | [`1_1_perfil_dos_dados.ipynb`](notebooks/parte1/1_1_perfil_dos_dados.ipynb) | [`docs/parte1/1_1_perfil_dos_dados.md`](docs/parte1/1_1_perfil_dos_dados.md) |
| 1.2 Atributos × performance | [`1_2_atributos_x_performance.ipynb`](notebooks/parte1/1_2_atributos_x_performance.ipynb) | [`docs/parte1/1_2_atributos_x_performance.md`](docs/parte1/1_2_atributos_x_performance.md) |
| 1.3 Padrões por plataforma | [`1_3_padroes_por_plataforma.ipynb`](notebooks/parte1/1_3_padroes_por_plataforma.ipynb) | [`docs/parte1/1_3_padroes_por_plataforma.md`](docs/parte1/1_3_padroes_por_plataforma.md) |
| 1.4 Visualizações para marketing | [`1_4_visualizacoes_marketing.ipynb`](notebooks/parte1/1_4_visualizacoes_marketing.ipynb) | [`docs/parte1/1_4_visualizacoes_marketing.md`](docs/parte1/1_4_visualizacoes_marketing.md) |

Apoio: [`docs/glossario.md`](docs/glossario.md) (cada termo, com uma analogia), [`docs/cola_entrevista.md`](docs/cola_entrevista.md) (roteiro e perguntas difíceis) e [`docs/tecnicas_conhecidas.md`](docs/tecnicas_conhecidas.md) (as técnicas usadas e de onde vêm).

### Como rodar

```bash
python -m venv venv
venv\Scripts\activate          # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace notebooks/parte1/1_1_perfil_dos_dados.ipynb notebooks/parte1/1_2_atributos_x_performance.ipynb notebooks/parte1/1_3_padroes_por_plataforma.ipynb notebooks/parte1/1_4_visualizacoes_marketing.ipynb
```

A limpeza também roda sozinha e se confere: `python -m src.limpeza`.

### O que cada notebook gera

| Arquivo | Quem gera | O que é |
|---|---|---|
| `data/processed/klike_treino_limpo.csv` | 1.1 | treino limpo (400 criativos) |
| `data/processed/klike_teste_limpo.csv` | 1.1 | teste limpo com as medianas do treino (100 criativos, não analisado) |
| `data/processed/efeitos_por_plataforma.csv` | 1.3 | diferença das medianas de cada atributo em cada rede (base da Parte 3) |
| `reports/figures/*.png` | 1.4 | as 3 figuras de apresentação |

`data/raw/klike_challenge_dataset.csv` é o arquivo original e nunca é alterado.

### Problema → evidência → tratamento

| Problema | Evidência | Tratamento |
|---|---|---|
| Olhar o teste contaminaria a nota final | O teste é a "prova guardada na gaveta" | Separar 80/20 antes de explorar, com a mesma proporção de cada rede (`stratify`) |
| Impressões erradas (4 linhas) | Cliques e CTR concordam entre si; as impressões ficam de 150 a 1.100 vezes acima | `impressões = cliques ÷ CTR` |
| CPC ou gasto errado (6 linhas) | `cpc ≠ gasto ÷ cliques`; a receita ÷ ROAS diz qual dos dois está certo | 3 CPC recalculados, 3 gastos recalculados (`cpc × cliques`) |
| Empate (KLK-0224, Branding, receita = 0) | Com o gasto original, o CPM ficaria 4 vezes acima do maior do Meta | Tratado como erro no gasto |
| CPC e receita vazios | São contas de outras colunas | Calculados: `gasto ÷ cliques` e `ROAS × gasto` |
| Duração, música/voz e engajamento vazios (~7%) | Sem padrão (régua do acaso); no teste de preenchimento, a mediana da plataforma errou menos que KNN e Iterative | Mediana da plataforma + indicador de faltante (`_faltava`) |
| Tempo assistido vazio | Não pode passar da duração do vídeo | Duração × fração mediana assistida na plataforma + indicador |
| Legenda vazia | "Não sei se tem" é diferente de "não tem" | Categoria "desconhecido" |
| "Boa performance" muda com o objetivo | Awareness quase não converte (CPA de R$67, ROAS 0); app install tem o menor CPA (R$10,9) | Criado o CPA (gasto ÷ conversões; vazio sem conversão); cada objetivo julgado pela sua métrica principal |
| CTR em 0,15 e engajamento em 0,10 | Muitos criativos exatamente nesse valor (teto) | Não corrigido; aviso nas conclusões (o efeito do gancho no CTR fica subestimado) |
| Receita = 0 em 96% de Branding | Branding tem conversões, mas não é feito para vender | Branding fora das análises de ROAS (filtro na hora) |
| Valores extremos | O z-score marca os 10 erros e mais 40 campanhas sem erro; no log, quase nada é extremo | Erros corrigidos; campanhas grandes de verdade ficam; uso de mediana e log |

### Principais descobertas (treino, 400 criativos)

1. **Gancho nos 3 primeiros segundos é a principal alavanca:** cerca de +17 pontos de nota, +66% de CTR e +56% de engajamento, mesmo comparando vídeos parecidos (regressão linear). Vale nas três redes.
2. **Rosto humano é a segunda** (+51% de engajamento, cerca de +11 pontos). **O texto tem um ponto ótimo no meio:** muito texto tira cerca de 15 pontos, pouco texto cerca de 8.
3. **As três redes diferem no contexto** (CPC do LinkedIn cerca de 5 vezes o do TikTok, TikTok engaja quase o dobro, ROAS de 0,6 no LinkedIn a 2,9 no TikTok), **mas o que funciona é quase o mesmo:** comparando os efeitos em cada par de redes, só 1 de 72 diferenças é confiável. Os indícios de diferença: **tirar a voz custa cerca de 12 pontos a mais no TikTok que no Meta**, e o gancho pesa um pouco mais no LinkedIn.
4. **O vídeo decide o clique; a venda depende de quem vê.** Analisando nove métricas, o criativo age no começo do funil (9 efeitos confiáveis em 30), quase nada no fim (8 em 50): o gancho não muda conversão, CPA nem ROAS. Quem move a venda é o público (retargeting: CPA 44% menor, ROAS 66% maior). Exceções: muito texto atrapalha do clique à venda, e o formato horizontal sai mais caro por conversão. Não há duração ideal.
5. **Retargeting sobe muito o CTR** (+70%), mas é efeito do público: compare criativos dentro do mesmo público.
6. **Para a Parte 2:** só com o que se sabe antes de postar, uma regressão explica 74% da variação da nota no treino (otimista; o teste dirá o valor real). CTR, retenção e engajamento não podem entrar no modelo "antes de postar".

São associações em dados observados e simulados, não causa. A prova seria um teste A/B.

### Figuras

| | |
|---|---|
| ![O que mover no criativo](reports/figures/fig1_o_que_mover_no_criativo.png) | ![O que funciona em cada rede](reports/figures/fig2_o_que_funciona_em_cada_rede.png) |
| ![O vídeo decide o clique](reports/figures/fig3_o_video_decide_o_clique.png) | |
