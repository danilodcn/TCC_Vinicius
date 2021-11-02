from app.FSS import FSS


class EspiraQuadrada(FSS):
    # Tamanho do Quadrado Maior
    d = None
    # Periodicidade
    p = None
    # Espessura
    w = None
    # Resistencia
    r = None

    def __init__(self, tamanho, espessura, periodicidade, resistencia):
        super().__init__()
        self.d = tamanho
        self.w = espessura
        self.p = periodicidade
        self.r = resistencia

    def calculo_impedancia(self, frequencia, angulo_incidencia):
        xl = self.z0*self.d/self.p*self.f(self.p, 2*self.w, self.vluz/frequencia, angulo_incidencia)
        bc = 4*self.d/self.p*self.f(self.p, self.p-self.d, self.vluz/frequencia, angulo_incidencia)/self.z0
        return [self.r, xl-1/bc]
