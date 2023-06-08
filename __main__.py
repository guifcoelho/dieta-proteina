import pyscipopt as scip
import math
import pandas as pd

class TipoProteina:
    nome: str
    minimo: float
    maximo: float
    def __init__(self, nome, minimo = 0, maximo = None):
        self.nome = nome
        self.minimo = minimo
        self.maximo = maximo

class Produto:
    nome: str
    tipos_proteina: list[TipoProteina]
    peso_unit: float
    preco: float
    minimo_qtd: int
    maximo_qtd: int
    def __init__(self, nome, tipos_proteina, peso_unit, preco, minimo_qtd = 0, maximo_qtd = None):
        self.nome = nome
        self.tipos_proteina = tipos_proteina
        self.peso_unit = peso_unit
        self.preco = preco
        self.minimo_qtd = minimo_qtd
        self.maximo_qtd = maximo_qtd

def resolver(dieta_semanal: float, tipos_proteina: dict[str, TipoProteina], produtos: list[Produto]):
    m = scip.Model("Otimizador-WMS")

    v_produto = {
        produto.nome: m.addVar(
            name=f"v_produto({produto.nome})",
            vtype="INTEGER",
            lb=produto.minimo_qtd,
            ub=produto.maximo_qtd if produto.maximo_qtd else math.inf
        )  
        for produto in produtos
    }
    v_produto_parc = {
        produto.nome: m.addVar(
            name=f"v_produto_parc({produto.nome})",
            vtype="CONTINUOUS",
            lb=produto.minimo_qtd,
            ub=produto.maximo_qtd if produto.maximo_qtd else math.inf
        )  
        for produto in produtos
    }

    m.setObjective(
        scip.quicksum(v_produto[produto.nome]*produto.preco for produto in produtos),
        'minimize'
    )

    m.addConss(
        v_produto[produto.nome] >= v_produto_parc[produto.nome]
        for produto in produtos
    )

    m.addCons(
        scip.quicksum(
            v_produto_parc[produto.nome]*produto.peso_unit
            for produto in produtos
        )
        == dieta_semanal
    )

    m.addConss(
        scip.quicksum(
            v_produto_parc[produto.nome]*produto.peso_unit
            for produto in produtos
            if tipo_proteina in produto.tipos_proteina
        )
        <= tipo_proteina.maximo
        for tipo_proteina in tipos_proteina.values()
        if tipo_proteina.maximo is not None
    )
    m.addConss(
        scip.quicksum(
            v_produto_parc[produto.nome]*produto.peso_unit
            for produto in produtos
            if tipo_proteina in produto.tipos_proteina
        )
        >= tipo_proteina.minimo
        for tipo_proteina in tipos_proteina.values()
    )

    m.setParams({
        'limits/gap': 1e-4,
        'limits/time': 60*5
    })

    m.optimize()

    resultado_dados = []
    for produto in produtos:
        qtd_produto_compra = int(round(m.getVal(v_produto[produto.nome])))
        qtd_produto_consumo = m.getVal(v_produto_parc[produto.nome])
        if qtd_produto_compra >= 1:
            resultado_dados += [(
                produto.nome,
                qtd_produto_compra,
                produto.peso_unit,
                produto.peso_unit*qtd_produto_consumo,
                produto.peso_unit*qtd_produto_compra,
                produto.peso_unit*qtd_produto_consumo / (produto.peso_unit*qtd_produto_compra),
                produto.preco * qtd_produto_compra
            )]

    resultado = \
        pd.DataFrame(
            resultado_dados,
            columns=['produto', 'quantidade_compra', 'peso_unit', 'peso_consumo', 'peso_compra', '% consumido', 'custo']
        )\
        .sort_values(['peso_consumo', 'custo', 'produto'], ascending=[False, False, True])\
        .reset_index(drop=True)

    return resultado

def main():

    dieta_semanal = 7*((40+160+40*2+160)+(40+140+40+140))
    maximo_carne_vermelha = 160*3+140*3
    tipos_proteina = {
        'ovo': TipoProteina('ovo', (40 + 40*2)*7 + (40 + 40)*7),
        'carne_vermelha': TipoProteina('carne_vermelha', maximo=maximo_carne_vermelha),
        'carne_vermelha-': TipoProteina('carne_vermelha-', maximo=maximo_carne_vermelha),
        'carne_vermelha+': TipoProteina('carne_vermelha+', 160+140, maximo_carne_vermelha),
        'peixe': TipoProteina('peixe', 2*(160+140)),
        'frango': TipoProteina('frango', 0),
        'frango+': TipoProteina('frango+', 2*(160+140)),
    }
    produtos = [
        Produto('cartela_ovo', [tipos_proteina['ovo']], 20*40, 17.49, maximo_qtd=2),#R$17,49/cartela
        Produto('file_peito_frango', [tipos_proteina['frango']], 700, 17), #R$17/cartela
        Produto('figado', [tipos_proteina['carne_vermelha-'], tipos_proteina['carne_vermelha']], 500, 26*0.5),#R$26/kg
        Produto('coxao_mole', [tipos_proteina['carne_vermelha+'], tipos_proteina['carne_vermelha']], 600, 40*0.6),
        Produto('sobre_coxa_sem_pele', [tipos_proteina['frango+']], 700*.7, 15), #R$17/cartela
        Produto('tilapia', [tipos_proteina['peixe']], 600, 60*0.6), 
    ]

    resultado = resolver(dieta_semanal, tipos_proteina, produtos)
    
    print()
    print(resultado)
    print("Dieta semanal mínima:", f"{dieta_semanal} g")
    print("Dieta atingida:", f"{resultado['peso_consumo'].sum()} g")
    print("Custo:", f"R$ {resultado['custo'].sum()}")
        

if __name__ == '__main__':
    main()