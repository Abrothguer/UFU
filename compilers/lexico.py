"""
Análisador léxico.

Retorna para cada token do arquivo informado:
    - Nome/Tipo do token
    - Valor do atributo (Opcional)
    - "pos"ição do lexema (Linha e Coluna)

Autor: Arthur Borges - 11711BCC014
"""

# Estados finais do autômato
FINALS = {
    "E": {"name": "relop", "value": "LE", "pos": None},
    "F": {"name": "relop", "value": "NE", "pos": None},
    "G": {"name": "relop", "value": "LT", "pos": None},
    "H": {"name": "relop", "value": "GE", "pos": None},
    "I": {"name": "relop", "value": "GT", "pos": None},
    "J": {"name": "relop", "value": "EQ", "pos": None},
    "L": {"name": "id", "value": None, "pos": None},
    "N": {"name": "numeral", "value": None, "pos": None},
    "T": {"name": "numeral", "value": None, "pos": None},
    "V": {"name": "numeral", "value": None, "pos": None},
    "W": {"name": "separador", "value": None, "pos": None},
    "Y": {"name": "operador", "value": "ADD", "pos": None},
    "Z": {"name": "operador", "value": "SUB", "pos": None},
    "AA": {"name": "operador", "value": "DIV", "pos": None},
    "AB": {"name": "operador", "value": "MUL", "pos": None},
    "AE": {"name": "se", "value": None, "pos": None},
    "AI": {"name": "fim", "value": None, "pos": None},
    "AM": {"name": "int", "value": None, "pos": None},
    "AR": {"name": "char", "value": None, "pos": None},
    "AX": {"name": "real", "value": None, "pos": None},
    "AW": {"name": "'", "value": None, "pos": None},
    "AY": {"name": ";", "value": None, "pos": None},
    "AZ": {"name": "(", "value": None, "pos": None},
    "BA": {"name": ")", "value": None, "pos": None},
    "BF": {"name": "inicio", "value": None, "pos": None},
    "BO": {"name": "enquanto", "value": None, "pos": None},
    "BX": {"name": "programa", "value": None, "pos": None},
    "BW": {"name": "=", "value": None, "pos": None},
}

SEPARATORS = ["\t", "\n", " "]


def word_auto(state, char):
    """a."""
    return "we must destroy him, for he is a creature of darkness."


def relop_auto(state, char):
    """a."""
    print(f"Relop auto called: \t{state}, \t'{char}'")
    next_state = None
    stepback = False

    if state == "A":
        if char == "<":
            next_state = "B"
        elif char == ">":
            next_state = "C"
        elif char == "=":
            next_state = "D"
    elif state == "B":
        if char == ">":
            next_state = "F"
        elif char == "=":
            next_state = "E"
        elif char.isalnum() or char in SEPARATORS:
            next_state = "G"
            stepback = True
    elif state == "C":
        if char == "=":
            next_state = "H"
        elif char.isalnum() or char in SEPARATORS:
            next_state = "I"
            stepback = True
    elif state == "D":
        if char == "=":
            next_state = "J"
        elif char.isalnum() or char in SEPARATORS:
            next_state = "BW"
            stepback = True

    if next_state is None:
        raise Exception(f"RELOP: Caractér estranho para estado: '{char}', {state}.")

    # Retorna: O próximo estado, se é um estado final, se precisa voltar
    print(f"Relop auto return: {(next_state, next_state in FINALS.keys(), stepback)}")
    return (next_state, next_state in FINALS.keys(), stepback)


def separator_auto(state, char):
    """a."""
    print(f"Separator auto called: \t\t{state}, \t'{char}'")
    if state == "A" and char in SEPARATORS:
        return ("X", False, False)
    elif state == "X":
        if char not in SEPARATORS:
            return ("W", True, True)
        return ("X", False, False)
    raise Exception(f"SEPARATOR: Caractér estranho: '{char}'.")


def arit_auto(state, char):
    """a."""
    print(f"Arithmetic auto called: \t{state}, \t'{char}'")
    if state == "A":
        if char == "+":
            return ("Y", True, False)
        if char == "-":
            return ("Z", True, False)
        if char == "/":
            return ("AA", True, False)
        if char == "*":
            return ("AB", True, False)

    raise Exception(f"ARIT: Caractér estranho para estado: '{char}', {state}.")


def symbol_auto(state, char):
    """a."""
    print(f"Symbol auto called: \t{state}, \t'{char}'")
    if state == "A":
        if char == "'":
            return ("AW", True, False)
        if char == ";":
            return ("AY", True, False)
        if char == "(":
            return ("AZ", True, False)
        if char == ")":
            return ("BA", True, False)

    raise Exception(f"SYMBOL: Caractér estranho para estado: '{char}', {state}.")


def number_auto(state, char):
    """a."""
    print(f"Number auto called: \t{state}, \t'{char}'")
    next_state = None
    stepback = False
    if state == "A":
        if char.isdigit():
            next_state = "M"

    elif state == "M":
        if char.isdigit():
            next_state = "M"
        elif char == ".":
            next_state = "O"
        elif char == "E":
            next_state = "P"
        elif char in SEPARATORS or char in ["+", "-", "/", "*", "<", ">", "=", ";", ")"]:
            next_state = "N"
            stepback = True

    elif state == "O":
        if char.isdigit():
            next_state = "Q"

    elif state == "P":
        if char.isdigit():
            next_state = "R"
        elif char == "+" or char == "-":
            next_state = "S"

    elif state == "Q":
        if char.isdigit():
            next_state = "Q"
        elif char == "E":
            next_state = "P"
        elif char in SEPARATORS or char in ["+", "-", "/", "*", "<", ">", "=", ";", ")"]:
            next_state = "T"
            stepback = True

    elif state == "R":
        if char.isdigit():
            next_state = "U"

    elif state == "S":
        if char.isdigit():
            next_state = "R"

    elif state == "U":
        if char in SEPARATORS or char in ["+", "-", "/", "*", "<", ">", "=", ";", ")"]:
            next_state = "V"
            stepback = True

    if next_state is None:
        raise Exception(f"NUMBER: Caractér estranho para estado: '{char}', {state}.")

    print(f"Number auto return: {(next_state, next_state in FINALS.keys(), stepback)}")
    return (next_state, next_state in FINALS.keys(), stepback)


def analyse_line(line, num):
    """
    Faz a análise de uma linha do código.

    Retorna uma lista com todos os tokens encontrados
    """
    size = len(line)
    index = 0
    current = "A"
    working_subauto = None

    lexeme = ""
    startpos = 0

    tokens = []

    while index < size:

        finalized = None
        stepback = False

        # Existe um subautomato trabalhando, dê o caractér para o tal.
        if working_subauto is not None:
            print("Calling working subautomata...")
            current, finalized, stepback = working_subauto(current, line[index])

        # Letra -> automato de reconhecimento de palavras reservadas e identificadores
        elif line[index].isalpha():
            pass

        # Número -> automato de reconhecimento de numerais
        elif line[index].isdigit():
            current, finalized, stepback = number_auto(current, line[index])
            working_subauto = number_auto

        # Relop -> automato de reconhecimento relop
        elif line[index] in ["<", ">", "="]:
            current, finalized, stepback = relop_auto(current, line[index])
            working_subauto = relop_auto

        # Operador -> automato de reconhecimento aritmetico
        elif line[index] in ["+", "-", "/", "*"]:
            current, finalized, stepback = arit_auto(current, line[index])
            working_subauto = arit_auto

        # Símbolos -> automato de reconhecimento de simbolos
        elif line[index] in ["'", ";", "(", ")"]:
            current, finalized, stepback = symbol_auto(current, line[index])
            working_subauto = symbol_auto

        # Separadores
        elif line[index] in SEPARATORS:
            current, finalized, stepback = separator_auto(current, line[index])
            working_subauto = separator_auto

        # Caracter estranho
        else:
            raise Exception(
                f"Cacatér '{line[index]}' não reconhecido linha: {num}, coluna: {index}."
            )

        if finalized:
            working_subauto = None

            token = FINALS[current].copy()
            token["pos"] = (num, startpos + 1)
            tokens.append(token)

            lexeme = ""
            current = "A"
            startpos = index + 1

        if stepback:
            index -= 1
            startpos -= 1
        else:
            lexeme += line[index]
        index += 1

    return tokens


def main(filename):
    """
    Main.

    Abre o arquivo e coleta as listas de tokens
    """
    with open(filename, "r") as code:

        print("Início da análise léxica")
        for num, line in code:
            analyse_line("line", num + 1)
        else:
            print("Fim da análise...")


def test_relop():
    """a."""
    strs = ["> < >= <= = == <>"]  # , "56==1", "67<>     0", "89 >= 0 "]

    for line in strs:
        tokens = analyse_line(line, 1)
        print(f"Tokens found in line {line}:\n")
        for token in tokens:
            print(token)


def test_arit():
    """a."""
    strs = ["+ - / * ++ --   */*+-+"]

    for line in strs:
        tokens = analyse_line(line, 1)
        print(f"Tokens found in line {line}:\n")
        for token in tokens:
            print(token)


def test_symbol():
    """a."""
    strs = ["(((';'))) ))(;;; ; ' ;' '"]

    for line in strs:
        tokens = analyse_line(line, 1)
        print(f"Tokens found in line {line}:\n")
        for token in tokens:
            print(token)


def test_number():
    """a."""
    strs = ["56 12353456 0  123.4 "]

    for line in strs:
        tokens = analyse_line(line, 1)
        print(f"Tokens found in line {line}:\n")
        for token in tokens:
            print(token)


def test():
    """a."""
    # test_relop()
    # test_arit()
    # test_symbol()
    test_number()


if __name__ == "__main__":
    test()
