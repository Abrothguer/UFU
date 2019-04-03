
# Busca local so olha onde está, fica presa no mínimo local.
# 1- Guardar estados anteriores
# 2- Embaralhar no começo

from random import randint

def calculate_heuristic(state):

    conflict = 0
    for queen_1 in range(len(state)):
        for queen_2 in range(queen_1+1, len(state)):

            # Same row
            if state[queen_1] == state[queen_2]:
                conflict += 1

            # Diagonal
            difference = queen_2-queen_1
            if state[queen_1] == state[queen_2] - difference or state[queen_1] == state[queen_2] + difference:
                conflict += 1
    return conflict


def hill_climbing(initial_state):

    cost = calculate_heuristic(initial_state)
    current_state = initial_state

    while cost != 0:

        h_board = [[0 for x in range(len(current_state))] for y in range(len(current_state))]
        print(f"Current state is {current_state}")

        for column in range(len(current_state)):
            for row in range(len(current_state)):

                if current_state[column] != row:
                    c_board = list(current_state)
                    c_board[column] = row
                    h_board[row][column] = calculate_heuristic(c_board)
                else:
                    h_board[row][column] = cost

        # print(f"\nHeuristics Board:\n")
        # for line in h_board:
        #     print(line)
        # input()

        minimum_cost = cost
        for column in range(len(h_board)):
            for row in range(len(h_board)):
                if h_board[column][row] < minimum_cost:
                    minimum_cost = h_board[column][row]

        # print(f"Minimum cost found is {minimum_cost}")

        best_moves = []
        for column in range(len(h_board)):
            for row in range(len(h_board)):
                if h_board[column][row] == minimum_cost:
                    best_moves.append( (column, row) )

        print(f"\nBest moves are {best_moves}\n")
        if len(best_moves) > 0:
            index = randint(0, len(best_moves)-1) #random move.
            # print(f"\nChoose the move of index {index}")
            column = best_moves[index][0]
            row = best_moves[index][1]
            current_state[row] = column
        else:
            print("No best moves found!")

        cost = calculate_heuristic(current_state)

    return current_state

def tabu_search(initial_state):

    cost = calculate_heuristic(initial_state)
    current_state = initial_state
    tabu_list = []

    while cost != 0:

        h_board = [[0 for x in range(len(current_state))] for y in range(len(current_state))]
        print(f"Current state is {current_state}")

        for column in range(len(current_state)):
            for row in range(len(current_state)):

                if current_state[column] != row:
                    c_board = list(current_state)
                    c_board[column] = row
                    h_board[row][column] = calculate_heuristic(c_board)
                else:
                    h_board[row][column] = cost

        minimum_cost = cost
        for column in range(len(h_board)):
            for row in range(len(h_board)):
                if h_board[column][row] < minimum_cost:
                    minimum_cost = h_board[column][row]

        # print(f"Minimum cost found is {minimum_cost}")

        best_moves = []
        for column in range(len(h_board)):
            for row in range(len(h_board)):
                if h_board[column][row] == minimum_cost:
                    best_moves.append( (column, row) )

        best_moves = [move for move in best_moves if move not in tabu_list]
        print(f"Best moves are {best_moves}\n")

        if len(best_moves) > 0:

            column = best_moves[0][0]
            row = best_moves[0][1]

            tabu_list.append(best_moves[0])
            if len(tabu_list) > 2:
                tabu_list.remove(tabu_list[0])
            current_state[row] = column
        else:
            print("No best moves found!")

        cost = calculate_heuristic(current_state)

    return current_state

def main():
    repr_board = [0,1,0,1] # (0,0), (1,1), (0,2), (1,3).

    print("\nDefault board:\n")

    board = [[0 for x in range(len(repr_board))] for y in range(len(repr_board))]
    for col, row in enumerate(repr_board):
        board[row][col] = 1
    for line in board:
        print(line)

    print("\n[0].Subida/Descida")
    print("\n[1].Subida/Descida com lista Tabu")

    choice = int(input())

    if choice == 0:
        final_state = hill_climbing(repr_board)
    else:
        final_state = tabu_search(repr_board)

    board = [[0 for x in range(len(final_state))] for y in range(len(final_state))]
    for col, row in enumerate(final_state):
        board[row][col] = 1
    for line in board:
        print(line)


if __name__ == "__main__":
    main()
