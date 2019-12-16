"""Projeto de construção de um analisador sintático preditivo.

Descendentes, derivação da raiz para folhas
Expansao da cabeça da produção
Necessaria remoção de recursão a esquerda
Geração de arvore sintática (derivação)
Decida recurisva sem retrocesso

Autor: Arthur Borges - 11711BCC014
"""
import sys
from lexico import analyze_code

RULES = {
    "S": [["programa", "Bloco"]],
    "Bloco": [["inicio", "Declaracao", "Comandos", "fim"]],
    "Declaracao": [["Tipo", "id", ";", "Declaracao"], []],
    "Tipo": [["int"], ["char"], ["real"]],
    "Comandos": [
        ["se", "(", "Condicao", ")", "Bloco", "Comandos"],
        ["enquanto", "(", "Condicao", ")", "Bloco", "Comandos"],
        ["id", "=", "Expressao", ";", "Comandos"],
        [],
    ],
    "Expressao": [
        ["id", "Expr'"],
        ["numeral", "Expr'"],
        ["'", "caracter", "'", "Expr'"],
        ["(", "Expressao", ")", "Expr'"],
    ],
    "Expr'": [["OpArit", "Expressao", "Expr'"], []],
    "OpArit": [["operador"]],
    "Condicao": [["Expressao", "OpRel", "Expressao"]],
    "OpRel": [["relop"]],
}

GENERATOR = None


def is_terminal(token):
    """Checa se um token é ou não terminal."""
    return token not in RULES.keys()


def print_tree(tree, tab=0):
    """Imprime uma arvore na tela."""
    print("\t" * tab, tree.symbol)
    for prod in tree.productions:
        print_tree(prod, tab + 1)


class SyntaxTree:
    """Implementa uma árvore de sintáxe."""

    def __init__(self, symbol, father):
        """Inicializa com símbolo e produções vazias."""
        self.symbol = symbol
        self.productions = []
        self.father = father

    def deriveprods(self, token):
        """Deriva a melhor produção levando em consideração o token informado."""
        sequence = []
        print(f"Deriving for {self.symbol}, {token['name']}")
        # Apenas um conjunto de regras pode ser derivado
        if len(RULES[self.symbol]) == 1:
            sequence = RULES[self.symbol][0]
        # Caso especial para Expr'
        elif self.symbol == "Expr'":
            sequence = (
                RULES[self.symbol][0] if token["name"] == "operador" else RULES[self.symbol][1]
            )
        # Caso especial para Declaracao
        elif self.symbol == "Declaracao":
            sequence = (
                RULES[self.symbol][0]
                if token["name"] in ["int", "char", "real"]
                else RULES[self.symbol][1]
            )
        # Caso especial para Comandos
        elif self.symbol == "Comandos" and token["name"] == "fim":
            return []

        # Derivação com base na cabeça da regra ser igual ao token especificado
        else:
            sequence = [
                seq for seq in RULES[self.symbol] if len(seq) > 0 and seq[0] == token["name"]
            ][0]

        # Faz atribuição das produções
        self.productions = [SyntaxTree(symbol, self) for symbol in sequence]


def recursive_build(current, inittoken):
    """Faz a decida recursiva sem retrocesso."""
    # Para cada símbolo na produção
    token = inittoken
    print(f"\nRecursive call for {current.symbol} and {token['name']}")
    for simb in current.productions:
        print(f"Analising symbol {simb.symbol} and token {token['name']}")
        # Se o símbolo é não terminal -> Recursão
        if not is_terminal(simb.symbol):
            print("\tIs not terminal -> Deriving")
            simb.deriveprods(token)
            token = recursive_build(simb, token)
        # Se o símbolo é terminal e casa com o token -> Sucesso
        elif is_terminal(simb.symbol) and simb.symbol == token["name"]:
            try:
                token = next(GENERATOR)
                while token["name"] == "separador":
                    token = next(GENERATOR)
                print(f"\tIs terminal and found -> Next token {token['name']}")
            except StopIteration:
                print(f"\tFim da análise")
        # Erro
        else:
            lin, col = token["pos"]
            print(f"Erro: Comando inválido: Linha {lin}, Coluna {col}")
            quit()
    # Retorna o token para a análise em ramos superiores
    return token


def analyze_syntax(filename):
    """Analisa a sintáxe e constrói a árvore de derivação."""
    # Inicialização do nó raiz e do gerador léxico
    root = SyntaxTree("S", None)

    global GENERATOR
    GENERATOR = analyze_code(filename)

    token = next(GENERATOR)
    root.deriveprods(token)
    recursive_build(root, token)
    return root


def main():
    """Main."""
    try:
        filename = sys.argv[1]
        syntaxtree = analyze_syntax(filename)
        print_tree(syntaxtree)
    except IndexError as e:
        print(f"Arquivo não especificado!", e.message)


if __name__ == "__main__":
    main()
