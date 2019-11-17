import time

from threading import Thread
from random import choice
from string import ascii_lowercase

N_THREADS = 30
SIGNALS = [0] * 30
PRINT_CICLES = 100000

STRING_SIZE = 80
STRING_TARGET = "".join(choice(ascii_lowercase) for _ in range(STRING_SIZE))

def pleb_thread(index):

    global STRING_TARGET, SIGNALS

    waiting_main = True
    thread_calls = 0
    current_cicle = 1
    print(f"Eu sou a thread {index} e acabo de ser inicializada!")

    while True:

        if current_cicle%PRINT_CICLES == 0:
            # print(f"Eu sou a thread {index} esperando pacientemente...")
            current_cicle = 1
        else:
            current_cicle += 1

        # Sua thread superior te chama
        if SIGNALS[index] == 1:

            print(f"Eu sou a thread {index} procurando letras minusculas...")

            # Procure a primeira minuscula que achar
            index_lower = -1
            for let_index, letter in enumerate(STRING_TARGET):
                if letter.islower():
                    index_lower = let_index
                    break

            # Não encontrei nada, logo sinalizo para quem me chamou que tivemos sucesso
            if index_lower == -1:
                print(f"Eu sou a thread {index} e não temos mais nada para capitalizar!")

                # Mude o seu sinal para -1 e caia no próximo if
                thread_calls += 1
                SIGNALS[ index ] = -1

            else:
                # Mude a letra para maiuscula
                STRING_TARGET = STRING_TARGET[0: index_lower] + STRING_TARGET[index_lower].upper() + STRING_TARGET[index_lower + 1: ]

                # Atualize o número de vezes que foi chamado
                thread_calls += 1

                # Não espere mais o início
                waiting_main = False

                # Você terminou o trabalho logo seu sinal volta pra 0
                SIGNALS[ index ] = 0

                # Chame a próxima por sinal
                SIGNALS[ index + 1 if index != N_THREADS - 1 else 0 ] = 1

        # Inicio da execução, ainda estou esperando que alguem me chame
        if waiting_main:
            continue

        # Sua thread inferior acaba de morrer
        if SIGNALS[index] == -1:

            print(f"Eu sou a thread {index} e quem eu chamei me disse que o trabalho foi concluido!")
            # Atualize o número de vezes que foi chamado
            thread_calls -= 1

            # Recebeu o sinal, logo volte pra 0
            SIGNALS [ index ] = 0

            # Sinalize a anterior
            SIGNALS[ index - 1 if index != 0 else N_THREADS - 1] = -1

        # O ciclo foi concluido, a thread morre
        if thread_calls == 0:

            print(f"Eu sou a thread {index} e meu proposito foi concluido, Adeus!")
            break


def main():
    """ Main thread """

    # Instancie todas as threads e as inicie
    plebs = [Thread(target = pleb_thread, args = [index]) for index in range(N_THREADS)]
    for pleb in plebs:
        pleb.start()

    # Esperando um segundo e chamando a primeira thread
    print(f"\nEu sou a thread principal e essa é a nossa string: {STRING_TARGET}")
    print(f"Numero de threads: {N_THREADS}\n")
    time.sleep(1)
    SIGNALS[0] = 1


if __name__ == "__main__":
    main()
