import math
import random
import numpy as np

from app.EspiraQuadrada import EspiraQuadrada
from app.FSS import FSS
from app.Individuo import Individuo
from app.Substrato import Substrato


class AG:
    # Intervalo de Frequência que será gerado a curva
    intervalo_curva = None
    # Passos na geração da curva
    passos_curva = None
    # Passo que começa a banda da antena
    passo_comeco_banda = None
    # Passo que termina a banda da antena
    passo_fim_banda = None

    # Array contendo a curva com funcionamento ideal de absorção
    curva_referencia_a = []
    # Array contendo a curva com funcionamento ideal de transmissão
    curva_referencia_t = []
    # Array contendo a curva com funcionamento ideal de reflexão
    curva_referencia_r = []

    # Máximo de Gerações
    max_geracoes = None
    # Fitness Última Geração
    ultimo_fitness = None
    # Faixa de Operação da Antena
    faixa_antena = None
    # Modo (1-TE, 2-TM)
    modo = None
    # Angulo de Incidencia
    angulo_incidencia = None
    # Tamanho da Geracao
    tamanho_geracao = None
    # Taxa de Mutação
    taxa_mutacao = None
    # Taxa de Crossover
    taxa_crossover = None
    # Quantidade de Selecionados
    n_selecionados = None
    # Geração
    geracao = []
    # Rank Weighting
    rank_weighting = []
    # Quantidade de Filhos por Casal
    n_filhos = None

    def __init__(self, tamanho_geracao, taxa_mutacao, taxa_crossover, modo, angulo_incidencia, max_geracoes, faixa_antena, intervalo_curva, passos_curva, n_selecionados):
        self.tamanho_geracao = tamanho_geracao
        self.taxa_mutacao = taxa_mutacao
        self.taxa_crossover = taxa_crossover
        self.n_selecionados = n_selecionados
        self.modo = modo
        self.angulo_incidencia = angulo_incidencia
        self.max_geracoes = max_geracoes
        self.faixa_antena = faixa_antena
        self.intervalo_curva = intervalo_curva
        self.passos_curva = passos_curva
        self.passo_comeco_banda = int(passos_curva * ((faixa_antena[0]-intervalo_curva[0]) / (intervalo_curva[1]-intervalo_curva[0])))
        self.passo_fim_banda = int(passos_curva * ((faixa_antena[1]-intervalo_curva[0]) / (intervalo_curva[1]-intervalo_curva[0])))
        self.curva_a_t()
        self.curva_r_t_metalic_fss()
        soma = (1+n_selecionados)*n_selecionados/2
        acumulado = 0
        for i in range(1, self.n_selecionados + 1):
            acumulado += (n_selecionados - i + 1)/soma
            self.rank_weighting.append(acumulado)
        self.n_filhos = round(2*(tamanho_geracao-n_selecionados)/n_selecionados)

    # Setar a curva com funcionamento ideal de absorção e transmissão
    def curva_a_t(self):
        # Array contendo a curva com funcionamento ideal de absorção
        self.curva_referencia_a = []
        # Array contendo a curva com funcionamento ideal de transmissão
        self.curva_referencia_t = []
        for i in range(self.passo_comeco_banda):
            self.curva_referencia_a.append(1)
            self.curva_referencia_t.append(0)
        for j in range(self.passo_fim_banda - self.passo_comeco_banda):
            self.curva_referencia_a.append(0)
            self.curva_referencia_t.append(1)
        for k in range(self.passos_curva-self.passo_fim_banda):
            self.curva_referencia_a.append(1)
            self.curva_referencia_t.append(0)

    # Métodos para AG de uma camada da FSS
    #
    #
    #
    #
    # Setar a curva com funcionamento ideal de reflexão e transmissão
    def curva_r_t_metalic_fss(self):
        # Array contendo a curva com funcionamento ideal de transmissão
        self.curva_referencia_t = []
        # Array contendo a curva com funcionamento ideal de reflexão
        self.curva_referencia_r = []
        for i in range(self.passo_comeco_banda):
            self.curva_referencia_r.append(1)
            self.curva_referencia_t.append(0)
        for j in range(self.passo_fim_banda-self.passo_comeco_banda):
            self.curva_referencia_r.append(0)
            self.curva_referencia_t.append(1)
        for k in range(self.passos_curva-self.passo_fim_banda):
            self.curva_referencia_r.append(1)
            self.curva_referencia_t.append(0)

    # Criar geração inicial do arranjo
    def set_geracao_espira_quadrada(self, l, e, u):
        for j in range(self.tamanho_geracao - 1):
            self.geracao.append(self.gerar_individuo_espira_quadrada(l, e, u))

    def gerar_individuo_espira_quadrada(self, l, e, u):
        # Intervalo: 0.002(2mm)-0.02(20mm)
        p = 0.002+0.018*random.random()
        # Intervalo: 0.4p_1-0.9p_1
        d = (0.4+0.5*random.random())*p
        # Intervalo: 0.05p_1-0.1p_1
        w = (0.05+0.05*random.random())*p
        # Rop = Zm^2*tan(km*d)^2/Z0
        frequencia = (self.faixa_antena[0] + self.faixa_antena[1]) / 2
        dieletrico = Substrato(l, e, u)
        zm = dieletrico.zm(self.modo, frequencia, self.angulo_incidencia)
        r = (zm**2)*(math.tan(dieletrico.km(frequencia))**2)/FSS.z0

        # set_espira_quadrada(Tamanho Quadrado Maior, Espessura, Periodicidade, Resistência)
        individuo = Individuo()
        individuo.set_espira_quadrada(d, w, p, r)
        return individuo

    def fitness_espira_quadrada(self, individuo):
        curva_r = []

        d = individuo.d_1
        w = individuo.w_1
        p = individuo.p_1
        r = individuo.r_1

        # Grating Lobe
        if p * (1 + math.sin(self.angulo_incidencia)) > FSS.vluz / (self.intervalo_curva[1]*10**9):
            return [99999, None]
        espira_quadrada = EspiraQuadrada(d, w, p, r)
        for i in range(self.passos_curva):
            v = espira_quadrada.calculo_impedancia((10**9)*(self.intervalo_curva[0]+(i/self.passos_curva) * (self.intervalo_curva[1]-self.intervalo_curva[0])), self.angulo_incidencia)
            r2 = (-1/(2*(math.sqrt(v[0]**2+v[1]**2)/espira_quadrada.z0)+1))**2
            curva_r = np.append(curva_r, 10*math.log(1-r2, 10))

        normalizado = np.true_divide(curva_r, max(np.abs(curva_r)))+1

        diferenca = normalizado - self.curva_referencia_r
        f = np.sum(np.square(diferenca))

        return [f, normalizado]

    # Métodos para AG do arranjo de FSS + Dielétrico
    #
    #
    #
    #
    # Criar geração inicial do arranjo
    def set_geracao_arranjo(self):
        for j in range(self.tamanho_geracao-1):
            self.geracao.append(self.gerar_individuo_arranjo())

    # Individuo sendo o arranjo inteiro
    def gerar_individuo_arranjo(self):
        # Dieletrico
        # Intervalo: 0.002(2mm)-0.01(10mm)
        d = 0.002+0.008*random.random()
        # Intervalo: 0.8e0-1.2e0
        e = 8.85418*(10**-12)*(1.2-0.4*random.random())
        # Intervalo: 0.8u0-1.2u0
        u = 1.2566*(10**-6)*(1.2-0.4*random.random())

        # Primeira Espira Quadrada
        # Intervalo: 0.002(2mm)-0.02(20mm)
        p_1 = 0.002+0.018*random.random()
        # Intervalo: 0.4p_1-0.9p_1
        d_1 = (0.4+0.5*random.random())*p_1
        # Intervalo: 0.05p_1-0.1p_1
        w_1 = (0.05+0.05*random.random())*p_1
        # Rop = Zm^2*tan(km*d)^2/Z0
        frequencia = (self.faixa_antena[0] + self.faixa_antena[1]) / 2
        dieletrico = Substrato(d, e, u)
        zm = dieletrico.zm(self.modo, frequencia, self.angulo_incidencia)
        r_1 = (zm**2)*(math.tan(dieletrico.km(frequencia))**2)/FSS.z0

        # Segunda Espira Quadrada
        # Intervalo: 0.002(2mm)-0.02(20mm)
        p_2 = 0.001+0.009*random.random()
        # Intervalo: 0.4p_2-0.9p_2
        d_2 = (0.2+0.7*random.random())*p_2
        # Intervalo: 0.05p_2-0.15p_2
        w_2 = (0.03+0.12*random.random())*p_2
        # Intervalo: 0ohm-0ohm
        r_2 = 0

        # Individuo(Tamanho Quadrado Maior, Espessura, Periodicidade, Resistência,
        # Largura Dieletrico, Permissividade, Permeabilidade,
        # Tamanho Quadrado Maior, Espessura, Periodicidade, Resistência)
        individuo = Individuo()
        individuo.set_arranjo(d_1, w_1, p_1, r_1, d, e, u, d_2, w_2, p_2, r_2)
        return individuo

    def selecionar_mate(self, selecionados):
        p = random.random()
        mate = None
        for m in range(self.n_selecionados):
            if p < self.rank_weighting[m]:
                print("a---------")
                print(self.n_selecionados)
                print("b")
                print(m)
                print("c")
                print(selecionados)
                print("d")
                print(len(selecionados))
                mate = selecionados[m]
                break
        return mate

    # Com o multiplicador é possível haver uma combinação fora do intervalor entre n1 e n2
    def combinar_real(self, multiplicador, n1, n2):
        beta = multiplicador * random.random();
        return n1*(1-beta) + beta*n2

    def crossover_espira_quadrada(self, macho, femea):
        # 1.3 pois assim será possivel o filho ter um valor fora do intervalo dos pais
        n = 1.3
        d, w, p, r = 0, 0, 0, 0
        while (p <= 0):
            p = self.combinar_real(n, macho.p_1, femea.p_1)
        while (d <= 0 or d > p):
            d = self.combinar_real(n, macho.d_1, femea.d_1)
        while (w <= 0 or w > d):
            w = self.combinar_real(n, macho.w_1, femea.w_1)
        while (r <= 0):
            r = self.combinar_real(n, macho.r_1, femea.r_1)

        resultado = Individuo()
        resultado.set_espira_quadrada(d, w, p, r)

        return resultado

    def nova_geracao(self):
        # Selecionar melhores
        selecionados = []
        # Setar o início da lista de fitness dos selecionados com 9999
        fitness_selecionados = [9999]
        # Para cada indivíduo verificar se ele se encaixa na lista de selecionados (Quando esse for menor que algum
        # dos n indivíduos já selecionados, encaixar este indivíduo na posição do que ele é menor)
        for j in range(self.tamanho_geracao-1):
            fitness_j = self.fitness_espira_quadrada(self.geracao[j])[0]
            for k in range(self.n_selecionados - 1):
                if fitness_j < fitness_selecionados[k]:
                    selecionados.insert(k, self.geracao[j])
                    fitness_selecionados.insert(k, self.fitness_espira_quadrada(self.geracao[j])[0])
                    break # Se for maior que um da lista de selecionados já pode pausar

        print(len(selecionados))

        # Substituir geração
        self.geracao = selecionados

        # 1 Selecionar os casais usando Rank Weighting
        # Selecionar Npop - Nkeep Casais:
        n_casais = math.floor(self.n_selecionados/2)
        n_filhos_gerados = 0

        for l in range(n_casais):
            # Selecionar pelo rank weighting macho e fêmea
            macho = self.selecionar_mate(selecionados)
            femea = self.selecionar_mate(selecionados)
            # Já fazer o crossover e mutação para gerar filhos
            for m in range(self.n_filhos):
                if(self.n_selecionados + n_filhos_gerados < self.tamanho_geracao):
                    filho = self.crossover_espira_quadrada(macho, femea)
                    filho.mutacao(self.taxa_mutacao)
                    self.geracao.append(filho)
                else: break
