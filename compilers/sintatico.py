"""
Projeto de construção de um analisador sintático preditivo

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
    "S": ["programa", "Bloco"],
}


class SyntaxTree:
    def __init__(symbol, father):
        self.symbol = symbol
        self.productions = []
        self.father = father


def analyze_syntax(filename):
    pass


def main():

    try:
        filename = sys.argv[1]
    except IndexError:
        print(f"Arquivo não especificado!")

    analyze_syntax(filename)


if __name__ == "__main__":
    main()
