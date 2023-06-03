# dieta-proteina
Calcula a quantidade de produtos a ser comprada para atender a dieta de proteína, minimizando o custo.

## Variáveis
- $\alpha_i \leq x_i \leq \beta_i \in Z^+, \forall i \in I$

  Onde $\alpha_i$ representa a menor quantidade do produto $i$ e $\beta_i$ representa a maior quantidade do produto $i$.
  
## Restrições

- $\sum\limits_{i} x_i \cdot P_i \geq \bar{P}$

  A soma do peso $P_i$ de cada produto $i$ multiplicada pela quantidade precisa ser menor que a dieta mínima total $\bar{P}$.
  
- $T^{MIN}_j \leq \sum\limits_i x_i \cdot P_i \leq T^{MAX}_j, \forall j \in J$, com $i \in I (j \in T^P_i)$

  Restringe o peso mínimo $T^{MIN}_j$ e máximo $T^{MAX}_j$ por tipo de proteína $j$ em relação a soma dos pesos dos produtos $i$ que tem o tipo de proteína $j$.
  
## Função objetivo

- Minimizar: $\sum\limits_{i} x_i \cdot C_i$

  Minimiza a soma do custo $C_i$ dos produtos $i \in I$ escolhidos.

  
