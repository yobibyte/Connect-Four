def check_streaks(state, streak, color=None):
    streak_list = []
    # for each piece in the board...
    for i in range(6):
        for j in range(7):
            # ...that is of the color we're looking for...
            if (color is None and state[i][j] != 0) or (color is not None and state[i][j] == color):
                streak_list.extend(streaks(i, j, state, streak))
    return [el for el in streak_list if len(el) > 0]


def streaks(row, col, state, streak):
    streak_list = [[],[],[],[]]
    for i in range(row, 6):
        if state[i][col] == state[row][col]:
            streak_list[0].append((i, col))
        else:
            break
    for j in range(col, 7):
        if state[row][j] == state[row][col]:
            streak_list[1].append((row, j))
        else:
            break

    j = col
    for i in range(row, 6):
        if j > 6:
            break
        elif state[i][j] == state[row][col]:
            streak_list[2].append((i,j))
        else:
            break
        j += 1 # increment column when row is incremented

    # check for diagonals with negative slope
    j = col
    for i in range(row, -1, -1):
        if j > 6:
            break
        elif state[i][j] == state[row][col]:
            streak_list[3].append((i,j))
        else:
            break
        j += 1
    return [el for el in streak_list if len(el) >= streak]
