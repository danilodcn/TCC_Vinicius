import math
from app.FSS import FSS


class Substrato:
    # Espessura
    d = None
    # Permissividade Elétrica
    e = None
    # Permebalidade Magnética
    u = None

    def __init__(self, espessura, permissividade, permeabilidade):
        self.d = espessura
        self.e = permissividade
        self.u = permeabilidade

    def km(self, frequencia):
        vluz = math.sqrt(1 / (self.e * self.u))
        km = 2 * math.pi / (vluz / frequencia)
        return km

    def beta(self, frequencia, angulo_incidencia):
        km = self.km(frequencia)
        k0 = 2 * math.pi / (FSS.vluz / frequencia)
        kt = k0 * math.sin(angulo_incidencia)
        beta = math.sqrt(km ** 2 - kt ** 2)
        return beta

    # modo = 1 para TE e 2 para TM
    def zm(self, modo, frequencia, angulo_incidencia):
        beta = self.beta(frequencia, angulo_incidencia)
        zs = beta / (2 * math.pi * frequencia * self.e) if (modo == 1) else 2 * math.pi * frequencia * self.u / beta
        return zs

    # modo = 1 para TE e 2 para TM
    def get_impedancia(self, modo, frequencia, angulo_incidencia):
        beta = self.beta(frequencia, angulo_incidencia)
        zs = self.zm(modo, frequencia, angulo_incidencia)
        return zs*math.tan(beta*self.d)
