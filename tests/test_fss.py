import os, sys
# o pytest nao estava conseguindo fazer o import do app
# por isso é necessário adicionar essa linha
sys.path.append(os.getcwd())       

from app.FSS import FSS
    

class TestFSS:
    def teste_calculo_c(self):
        fss = FSS()
        result = fss.beta(29, 78)
        # o resultado foi de 0.5513770897216917
        # agora basta fazer o assertion
        assert result == 0.5513770897216917
        import ipdb; ipdb.set_trace()