"""
Análisador léxico.

Retorna para cada token do arquivo informado:
    - Nome/Tipo do token
    - Valor do atributo (Opcional)
    - "pos"ição do lexema (Linha e Coluna)

Autor: Arthur Borges - 11711BCC014
"""

SYMBOL_TABLE = []

# TODO: DOCSTRINGS

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
    "BY": {"name": "=", "value": None, "pos": None},
}

# Lista de separadores
SEPARATORS = ["\t", "\n", " "]


def add_to_symboltable(lexeme):
    if lexeme not in SYMBOL_TABLE:
        SYMBOL_TABLE.append(lexeme)
    return SYMBOL_TABLE.index(lexeme)


def word_middle_aux(char, wtdchar, wtdstate):
    """a."""
    state = None
    stepback = False
    if char in SEPARATORS:
        state = "L"
        stepback = True
    if char == wtdchar:
        state = wtdstate
    elif char.isalpha() or char.isdigit():
        state = "K"
    return state, stepback


def word_final_aux(char, wtdstate):
    """a."""
    state = None
    stepback = False
    if char in SEPARATORS:
        state = wtdstate
        stepback = True
    elif char.isalpha() or char.isdigit():
        state = "K"
    return state, stepback


def word_auto(state, char):
    """a."""
    print(f"Word auto called: \t{state}, \t'{char}'")
    next_state = None
    stepback = False
    symbol_table = False

    if state == "A":
        if char == "s":
            next_state = "AC"
        elif char == "e":
            next_state = "BG"
        elif char == "f":
            next_state = "AF"
        elif char == "i":
            next_state = "AJ"
        elif char == "c":
            next_state = "AN"
        elif char == "r":
            next_state = "AS"
        elif char == "p":
            next_state = "BP"
        elif char.isalpha():
            next_state = "K"

    elif state == "AC":
        next_state, stepback = word_middle_aux(char, "e", "AD")
    elif state == "AD":
        next_state, stepback = word_final_aux(char, "AE")

    elif state == "AF":
        next_state, stepback = word_middle_aux(char, "i", "AG")
    elif state == "AG":
        next_state, stepback = word_middle_aux(char, "m", "AH")
    elif state == "AH":
        next_state, stepback = word_final_aux(char, "AI")

    elif state == "AJ":
        next_state, stepback = word_middle_aux(char, "n", "AK")
    elif state == "AK":
        next_state, stepback = word_middle_aux(char, "t", "AL")
        if char == "i":
            next_state = "BB"
    elif state == "AL":
        next_state, stepback = word_final_aux(char, "AM")

    elif state == "AN":
        next_state, stepback = word_middle_aux(char, "h", "AO")
    elif state == "AO":
        next_state, stepback = word_middle_aux(char, "a", "AP")
    elif state == "AP":
        next_state, stepback = word_middle_aux(char, "r", "AQ")
    elif state == "AQ":
        next_state, stepback = word_final_aux(char, "AR")

    elif state == "AS":
        next_state, stepback = word_middle_aux(char, "e", "AT")
    elif state == "AT":
        next_state, stepback = word_middle_aux(char, "a", "AU")
    elif state == "AU":
        next_state, stepback = word_middle_aux(char, "l", "AV")
    elif state == "AV":
        next_state, stepback = word_final_aux(char, "AX")

    elif state == "BB":
        next_state, stepback = word_middle_aux(char, "c", "BC")
    elif state == "BC":
        next_state, stepback = word_middle_aux(char, "i", "BD")
    elif state == "BD":
        next_state, stepback = word_middle_aux(char, "o", "BE")
    elif state == "BE":
        next_state, stepback = word_final_aux(char, "BF")

    elif state == "BG":
        next_state, stepback = word_middle_aux(char, "n", "BH")
    elif state == "BH":
        next_state, stepback = word_middle_aux(char, "q", "BI")
    elif state == "BI":
        next_state, stepback = word_middle_aux(char, "u", "BJ")
    elif state == "BJ":
        next_state, stepback = word_middle_aux(char, "a", "BK")
    elif state == "BK":
        next_state, stepback = word_middle_aux(char, "n", "BL")
    elif state == "BL":
        next_state, stepback = word_middle_aux(char, "t", "BM")
    elif state == "BM":
        next_state, stepback = word_middle_aux(char, "o", "BN")
    elif state == "BN":
        next_state, stepback = word_final_aux(char, "BO")

    elif state == "BP":
        next_state, stepback = word_middle_aux(char, "r", "BQ")
    elif state == "BQ":
        next_state, stepback = word_middle_aux(char, "o", "BR")
    elif state == "BR":
        next_state, stepback = word_middle_aux(char, "g", "BS")
    elif state == "BS":
        next_state, stepback = word_middle_aux(char, "r", "BT")
    elif state == "BT":
        next_state, stepback = word_middle_aux(char, "a", "BU")
    elif state == "BU":
        next_state, stepback = word_middle_aux(char, "m", "BV")
    elif state == "BV":
        next_state, stepback = word_middle_aux(char, "a", "BW")
    elif state == "BW":
        next_state, stepback = word_final_aux(char, "BX")

    elif state == "K":
        if char.isalpha() or char.isdigit():
            next_state = "K"
        elif char in SEPARATORS or char in ["+", "-", "/", "*", "<", ">", "=", ";", ")", "'"]:
            next_state = "L"
            stepback = True
            symbol_table = True

    if next_state is None:
        raise Exception(f"WORD: Caractér estranho para estado: '{char}', {state}.")

    print(f"Word auto return: {(next_state, next_state in FINALS.keys(), stepback)}")
    return (next_state, next_state in FINALS.keys(), stepback, symbol_table)


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
            next_state = "BY"
            stepback = True

    if next_state is None:
        raise Exception(f"RELOP: Caractér estranho para estado: '{char}', {state}.")

    # Retorna: O próximo estado, se é um estado final, se precisa voltar
    print(f"Relop auto return: {(next_state, next_state in FINALS.keys(), stepback)}")
    return (next_state, next_state in FINALS.keys(), stepback)


def separator_auto(state, char):
    """A separator automaton."""
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
    return (next_state, next_state in FINALS.keys(), stepback, True)


def analyse_line(line, num):
    """
    Faz a análise de uma linha do código.

    Retorna uma lista com todos os tokens encontrados
    """
    if line[-1] != "\n":
        line += "\n"  # Gambiarra pra testes e última linha do arquivo
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
        value = []

        try:
            # Existe um subautomato trabalhando, dê o caractér para o tal.
            if working_subauto is not None:
                print("Calling working subautomata...")
                current, finalized, stepback, *value = working_subauto(current, line[index])

            # Letra -> automato de reconhecimento de palavras reservadas e identificadores
            elif line[index].isalpha():
                current, finalized, stepback, *value = word_auto(current, line[index])
                working_subauto = word_auto

            # Número -> automato de reconhecimento de numerais
            elif line[index].isdigit():
                current, finalized, stepback, *value = number_auto(current, line[index])
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
        except Exception as ecp:
            raise Exception(
                f"Erro: Lexema: {lexeme}, Linha: {num}, Coluna: {index}, Detalhes: {ecp}"
            ) from ecp

        if finalized:
            print(f"Done processing the token -> lexeme: {lexeme}, stepback: {stepback}")
            working_subauto = None

            token = FINALS[current].copy()
            token["pos"] = (num, startpos + 1)

            # print(f"Value of token {lexeme} is {value}")
            if value != [] and value[0]:
                token["value"] = add_to_symboltable(lexeme)
            tokens.append(token)

            lexeme = ""
            current = "A"
            startpos = index + 1

        if stepback:
            index -= 1
            startpos -= 1
        elif not finalized:
            lexeme += line[index]
        index += 1

    if lexeme != "":  # Gambiarra - Separador não processado no final da linha
        if lexeme.replace("\t", "").replace("\n", "").replace(" ", "") == "":
            tokens.append({"name": "separador", "value": None, "pos": (num, startpos + 1)})
        else:
            raise Exception(
                f"Cacatér '{line[index-1]}' não reconhecido linha: {num}, coluna: {startpos}."
            )

    return tokens


def main(filename):
    """
    Main.

    Abre o arquivo e coleta as listas de tokens
    """
    with open(filename, "r") as code:

        tokens = []
        print("\nInício da análise léxica")

        for num, line in enumerate(code):
            tokens.append(analyse_line(line, num + 1))
        else:
            print("Fim da análise...\n  ")

        print("Tokens encontrados pelo analisador lexico")
        tokens = [token for sublist in tokens for token in sublist]
        for token in tokens:
            print(token)

    return tokens


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


def test_words():
    """a."""
    strs = ["id idteste programa enquanto int inicio fim real char se arthur programs"]

    for line in strs:
        tokens = analyse_line(line, 1)
        print(f"Tokens found in line '{line}':\n")
        for token in tokens:
            print(token)


def test():
    """a."""
    # test_relop()
    # test_arit()
    # test_symbol()
    # test_number()
    # test_words()

    main("ptest0.txt")

    print(SYMBOL_TABLE)
    # main("ptest1.txt")


def analyze_code(filename):

    for token in main(filename):
        yield token


if __name__ == "__main__":
    test()
