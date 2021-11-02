import numpy as np


class Individuo:
    fitness = None

    # Intervalo de Frequência que será gerado a curva
    intervalo_curva = [0, 20]
    # Passos na geração da curva
    passos_curva = 100
    # Curva de Absorção
    curva_a = None
    # Curva de Transmissão
    curva_t = None
    # Curva de Reflexão
    curva_r = None

    # Primeira Espira Quadrada
    d_1 = None
    p_1 = None
    w_1 = None
    r_1 = None

    # Dielétrico
    d = None
    e = None
    u = None

    # Segunda Espira Quadrada
    d_2 = None
    p_2 = None
    w_2 = None
    r_2 = None

    def __repr__(self) -> str:
        """Funçao usada para representar o individuo ao fazer print"""
        txt = f"Fitness = {self.fitness}, Intervalo da Curva = {self.intervalo_curva}"
        return f"Individuo ({txt})"

    # set_arranjo(Tamanho Quadrado Maior, Espessura, Periodicidade, Resistência,
    # Largura Dieletrico, Permissividade, Permeabilidade,
    # Tamanho Quadrado Maior, Espessura, Periodicidade, Resistência)
    def set_arranjo(self, d_1, w_1, p_1, r_1, d, e, u, d_2, w_2, p_2, r_2):
        self.d_1 = d_1
        self.w_1 = w_1
        self.p_1 = p_1
        self.r_1 = r_1

        self.d = d
        self.e = e
        self.u = u

        self.d_2 = d_2
        self.w_2 = w_2
        self.p_2 = p_2
        self.r_2 = r_2

    # set_espira_quadrada(Tamanho Quadrado Maior, Espessura, Periodicidade, Resistência)
    def set_espira_quadrada(self, d, w, p, r):
        self.d_1 = d
        self.w_1 = w
        self.p_1 = p
        self.r_1 = r

    def mutacao(self, taxa_mutacao):
        while True:
            mutar = np.random.normal(0, taxa_mutacao)
            self.p_1 *= mutar
            if self.p_1 >= 0: break
        while True:
            mutar = np.random.normal(0, taxa_mutacao)
            self.d_1 *= mutar
            if self.d_1 >= 0 and self.d_1 < self.p_1: break
        while True:
            mutar = np.random.normal(0, taxa_mutacao)
            self.w_1 *= mutar
            if self.w_1 >= 0 and self.w_1 < self.d_1: break
        while True:
            mutar = np.random.normal(0, taxa_mutacao)
            self.r_1 *= mutar
            if self.r_1 >= 0: break
