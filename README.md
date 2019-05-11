## Inteligência Artificial - UFFS 2019.1

#### Descrição:
Desenvolvimento de algoritmo genético para resolução do problema de colaração de vértices.

Dados um número __n__ de vértices, uma probabilidade __p__ (de 0 à 100) para criação de arestas entre dois vértices e um número de gerações __g__, a aplicação gera um grafo aleatório com __n__ vértices e, utilizando um algoritmo genético, colore seus vértices de forma que dois vértices conectados por uma aresta não tenham a mesma cor.

#### Detalhes:
Trabalho desenvolvido utilizando linguagem [Python 3.5+](https://www.python.org/) e bibliotecas [pyeasyga](https://github.com/remiomosowon/pyeasyga) e [Networkx](https://networkx.github.io/).

### Instalação de dependências
```
pip install -r requirements.txt
```

### Execução
Depois de instaladas as dependências:
```
python main.py n p g
```
Sendo __n__ é o número de vértices, __p__ a probabilidade da criação de uma aresta e __g__ o número de gerações a serem executadas.
