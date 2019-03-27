INF = 1000

def sum_diagonals(t_board, cur_i, cur_j):

    total_s = 0
    #Top left
    new_i, new_j = cur_i-1, cur_j-1
    while new_i >= 0 and new_j >= 0:
        total_s += t_board[new_i][new_j]
        new_i -= 1
        new_j -= 1

    #Bottom right
    new_i, new_j = cur_i+1, cur_j+1
    while new_i < len(t_board) and new_j < len(t_board):
        total_s += t_board[new_i][new_j]
        new_i += 1
        new_j += 1

    #Top right
    new_i, new_j = cur_i-1, cur_j+1
    while new_i >= 0 and new_j < len(t_board):
        total_s += t_board[new_i][new_j]
        new_i -= 1
        new_j += 1

    #Bottom left
    new_i, new_j = cur_i+1, cur_j-1
    while new_i < len(t_board) and new_j >= 0:
        total_s += t_board[new_i][new_j]
        new_i += 1
        new_j -= 1

    return total_s

def calculate(t_board):

    line_sum = 0
    for i in t_board:
        i_sum = sum(i)
        if i_sum <= 1:
            line_sum += 0
        elif i_sum == 2:
            line_sum += 1
        else:
            line_sum += i_sum
    # print(f"line_sum is {line_sum}")

    diagonal_sum = 0

    for i in range(len(t_board)):
        for j in range(len(t_board)):

            if t_board[j][i] == 1:
                diagonal_sum += sum_diagonals(t_board, j, i)
    diagonal_sum /= 2
    # print(f"diag_sum is {diagonal_sum}")

    return line_sum + diagonal_sum


def calculate_heuristic(board):

    h_board = []
    for i in range(len(board)):
        h_board.append([0]*4)

    for i in range(len(board)):
        new_board = [row[:] for row in board]

        for j in range(len(new_board[i])):
            new_board[j][i] = 0

        # print(f"\n{i}\n")
        # for line in new_board:
        #     print(line)

        for j in range(len(new_board[i])):
            new_board[j][i] = 1

            # print(f"\n{i} and {j}\n")
            # for line in new_board:
            #     print(line)

            h_board[j][i] = calculate(new_board) / 2
            # print(f"\nfor {i} and {j} = {h_board[j][i]}")
            # for line in h_board:
            #     print(line)
            # input()

            new_board[j][i] = 0

    return h_board

def find_better(c_board):

    min_cost = INF
    for i in range(len(c_board)):
        for j in range(len(c_board[i])):
            if c_board[i][j] <= min_cost:
                min_cost = c_board[i][j]

    min_coords = []
    for i in range(len(c_board)):
        for j in range(len(c_board[i])):
            if c_board[i][j] == min_cost:
                min_coords.append((i,j))

    return min_coords


def main():
    board = [[1,0,1,0],
             [0,1,0,1],
             [0,0,0,0],
             [0,0,0,0]]

    print("\nInitial:\n")
    for line in board:
        print(line)
    prevs = []

    while True:

        c_board = calculate_heuristic(board)

        print("\nHeuristic:\n")
        for line in c_board:
            print(line)

        moves = find_better(c_board)
        print(f"\nAll moves = {moves}")
        for mv in moves:
            if mv not in prevs:
                prevs.append(mv)
                move = mv
                break

        print(f"Best move = {move}")
        for i in range(len(board)):
            if i == move[0]:
                board[i][move[1]] = 1
            else:
                board[i][move[1]] = 0
        if (c_board[move[0]][move[1]]*2) == 0:
            print("\nSolution found:\n")
            for line in board:
                print(line)
            break

        print(f"\nNew board:\n")
        for line in board:
            print(line)
        input("\nPress Enter\n")

if __name__ == "__main__":
    main()
