import math

# Напрямки: 0: UP, 1: RIGHT, 2: DOWN, 3: LEFT
MOVE_MAP = {0: "UP", 1: "RIGHT", 2: "DOWN", 3: "LEFT"}

# Швидка вагова матриця з aj-r 2048-AI (тягне в лівий нижній кут)
WEIGHTS = [
    [2,   4,   8,   16],
    [32,  16,  8,   4],
    [64,  128, 256, 512],
    [8192,4096,2048,1024]
]

def get_best_move(matrix, depth=4):
    best_score = -float('inf')
    best_move = None
    
    for move in [0, 1, 2, 3]:
        moved_matrix, moved, _ = execute_move(matrix, move)
        if not moved:
            continue
            
        score = expectimax(moved_matrix, depth - 1, False)
        if score > best_score:
            best_score = score
            best_move = MOVE_MAP[move]
            
    if best_move is None:
        for move in [0, 1, 2, 3]:
            _, moved, _ = execute_move(matrix, move)
            if moved: return MOVE_MAP[move]
        return "DOWN"
        
    return best_move

def expectimax(matrix, depth, is_player_turn):
    if depth == 0 or is_game_over(matrix):
        return evaluate_board(matrix)
        
    if is_player_turn:
        best_score = -float('inf')
        for move in [0, 1, 2, 3]:
            moved_matrix, moved, _ = execute_move(matrix, move)
            if moved:
                score = expectimax(moved_matrix, depth, False)
                best_score = max(best_score, score)
        return best_score
    else:
        score_sum = 0
        empty_cells = []
        for r in range(4):
            for c in range(4):
                if matrix[r][c] == 0:
                    empty_cells.append((r, c))
                    
        if not empty_cells:
            return evaluate_board(matrix)
            
        # Рахуємо середній результат без створення зайвих копій через deepcopy
        for r, c in empty_cells:
            # Тимчасово підставляємо 2
            matrix[r][c] = 2
            score_sum += 0.9 * expectimax(matrix, depth - 1, True)
            
            # Тимчасово підставляємо 4
            matrix[r][c] = 4
            score_sum += 0.1 * expectimax(matrix, depth - 1, True)
            
            # Повертаємо як було
            matrix[r][c] = 0
            
        return score_sum / len(empty_cells)

def evaluate_board(matrix):
    score = 0
    empty_tiles = 0
    for r in range(4):
        for c in range(4):
            val = matrix[r][c]
            if val == 0:
                empty_tiles += 1
                continue
            score += WEIGHTS[r][c] * math.log2(val)
    return score + (empty_tiles * 25)

def is_game_over(matrix):
    for r in range(4):
        for c in range(4):
            if matrix[r][c] == 0: return False
            if r < 3 and matrix[r][c] == matrix[r+1][c]: return False
            if c < 3 and matrix[r][c] == matrix[r][c+1]: return False
    return True

def slide_and_merge(row):
    # Оптимізований зсув рядка без зайвих pop()
    non_zeros = [x for x in row if x != 0]
    new_row = []
    skip = False
    for i in range(len(non_zeros)):
        if skip:
            skip = False
            continue
        if i + 1 < len(non_zeros) and non_zeros[i] == non_zeros[i+1]:
            new_row.append(non_zeros[i] * 2)
            skip = True
        else:
            new_row.append(non_zeros[i])
    while len(new_row) < 4:
        new_row.append(0)
    return new_row

def execute_move(matrix, move):
    # Швидке створення копії списку замість копіювання всього об'єкта
    m = [row[:] for row in matrix]
    
    if move == 3: # LEFT
        for i in range(4): m[i] = slide_and_merge(m[i])
    elif move == 1: # RIGHT
        for i in range(4): m[i] = slide_and_merge(m[i][::-1])[::-1]
    elif move == 0: # UP
        for c in range(4):
            col = [m[r][c] for r in range(4)]
            new_col = slide_and_merge(col)
            for r in range(4): m[r][c] = new_col[r]
    elif move == 2: # DOWN
        for c in range(4):
            col = [m[r][c] for r in range(4)][::-1]
            new_col = slide_and_merge(col)[::-1]
            for r in range(4): m[r][c] = new_col[r]
            
    return m, m != matrix, 0