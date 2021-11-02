import numpy as np
from app.AG import AG
from matplotlib import pyplot as plt

tamanho_populacao = 10
passos = 10
inicio = 3
fim = 6
n_selecionados = 4

ag = AG(tamanho_populacao, 0.5, 0, 1, 0, 100, [4.2, 4.9], [inicio, fim], passos, n_selecionados)
ag.set_geracao_espira_quadrada(0.001, 8.85418*(10**-12), 1.2566*(10**-6))

# N gerações
n = 10
for j in range(n):
    ag.nova_geracao()

# Mostrar melhor
menor = 0
for i in range(tamanho_populacao-1):
    if ag.fitness_espira_quadrada(ag.geracao[i])[0] < ag.fitness_espira_quadrada(ag.geracao[menor])[0]:
        menor = i

plt.plot(np.arange(inicio, fim, (fim-inicio)/passos), ag.fitness_espira_quadrada(ag.geracao[menor])[1])
plt.xlabel("Frequency (GHz)")
plt.ylabel("S11 (dB)")
plt.title("S11")
plt.show()

plt.plot(np.arange(inicio, fim, (fim-inicio)/passos), ag.curva_referencia_r)
plt.xlabel("Perfect (GHz)")
plt.ylabel("S11 (dB)")
plt.title("S11")
plt.show()

# Mostrar Fitness
diferenca = ag.fitness_espira_quadrada(ag.geracao[menor])[1] - ag.curva_referencia_r
f = np.sum(np.square(diferenca))
print(f)