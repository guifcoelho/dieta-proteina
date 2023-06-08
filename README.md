# dieta-proteina
Calcula a quantidade de produtos a ser comprada para atender a dieta de proteína, minimizando o custo.

## Variáveis
- $\alpha_i \leq x_i \leq \beta_i \in R^+, \forall i \in I$

  Quantidade de produtos consumida.

- $\alpha_i \leq \bar{x}_i \leq \beta_i \in Z^+, \forall i \in I$

  Quantidade inteira de produtos comprada.

  Onde $\alpha_i$ representa a menor quantidade do produto $i$ e $\beta_i$ representa a maior quantidade do produto $i$.
  
## Restrições

- $\bar{x}_i \geq x_i, \forall i \in I$

  Define a quantidade inteira a ser comprada baseada em quanto é consumido.

- $\sum\limits_{i} x_i \cdot P_i = \bar{P}$

  A soma do peso $P_i$ de cada produto $i$ multiplicada pela quantidade (peso consumido) precisa ser igual a dieta mínima total $\bar{P}$.
  
- $T^{MIN}_j \leq \sum\limits_i x_i \cdot P_i \leq T^{MAX}_j, \forall j \in J$, com $i \in I (j \in T^P_i)$

  Restringe o peso mínimo $T^{MIN}_j$ e máximo $T^{MAX}_j$ por tipo de proteína $j$ em relação a soma dos pesos dos produtos $i$ que tem o tipo de proteína $j$.
  
## Função objetivo

- Minimizar: $\sum\limits_{i} \bar{x}_i \cdot C_i$

  Minimiza a soma do custo $C_i$ dos produtos $i \in I$ escolhidos.

  
