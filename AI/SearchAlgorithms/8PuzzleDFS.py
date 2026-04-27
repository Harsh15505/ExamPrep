import copy

class PuzzleState:
    def __init__(self, board, parent=None, move=None, depth=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth+1                
        self.blank_pos = self.find_blank()

    def find_blank(self):
        """Find position of blank tile (0)"""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def get_board_tuple(self):
        """Convert board to tuple for hashing"""
        return tuple(tuple(row) for row in self.board)

    def is_goal(self, goal_state):
        """Check if current state matches goal state"""
        return self.board == goal_state

    def get_neighbors(self):
        """Generate all valid neighboring states"""
        neighbors = []
        row, col = self.blank_pos

        moves = [
            (-1, 0, "UP"),
            (1, 0, "DOWN"),
            (0, -1, "LEFT"),
            (0, 1, "RIGHT")
        ]

        for dr, dc, move_name in moves:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_board = copy.deepcopy(self.board)
                new_board[row][col], new_board[new_row][new_col] = \
                    new_board[new_row][new_col], new_board[row][col]

                neighbors.append(PuzzleState(new_board, self, move_name, self.depth + 1))

        return neighbors

    def get_path(self):
        """Get path from initial state to current state"""
        path = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return path[::-1]

    def display(self):
        """Display the puzzle board"""
        for row in self.board:
            print("  " + " ".join(str(x) if x != 0 else "_" for x in row))


class PuzzleSolver:
    def __init__(self, initial_state, goal_state):
        self.initial = PuzzleState(initial_state)
        self.goal = goal_state

    def solve_dfs(self, max_depth=50):
        """Solve using Depth First Search with depth limit"""
        visited = set()
        nodes_explored = [0]

        def dfs_recursive(state, depth):
            if depth > max_depth:
                return None

            board_tuple = state.get_board_tuple()
            if board_tuple in visited:
                return None

            visited.add(board_tuple)
            nodes_explored[0] += 1

            if state.is_goal(self.goal):
                return state.get_path()

            for neighbor in state.get_neighbors():
                result = dfs_recursive(neighbor, depth + 1)
                if result:
                    return result

            return None

        result = dfs_recursive(self.initial, 0)
        print(f"\nNodes explored: {nodes_explored[0]}")
        return result


def get_board_input(prompt):
    """Get 3x3 board input from user"""
    print(prompt)
    print("Enter 9 numbers (0-8) separated by spaces (0 represents blank):")

    while True:
        try:
            numbers = list(map(int, input().split()))

            if len(numbers) != 9:
                print("Error: Please enter exactly 9 numbers!")
                continue

            if set(numbers) != set(range(9)):
                print("Error: Please enter numbers 0-8 with no repetition!")
                continue

            board = [numbers[i:i+3] for i in range(0, 9, 3)]
            return board

        except ValueError:
            print("Error: Please enter valid integers!")


def display_solution(path, method):
    """Display the solution path"""
    if not path:
        print(f"\nNo solution found using {method}!")
        return

    print(f"\n{'=' * 60}")
    print(f"Solution found using {method}!")
    print(f"{'=' * 60}")
    print(f"Number of moves: {len(path) - 1}\n")

    for i, state in enumerate(path):
        if i == 0:
            print("Initial State:")
        else:
            print(f"\nStep {i}: Move {state.move}")
        state.display()

    print(f"\n{'=' * 60}")


def main():
    print("=" * 60)
    print("8-PUZZLE PROBLEM SOLVER (Using DFS)")
    print("=" * 60)

    initial_state = get_board_input("\nEnter Initial State:")
    goal_state = get_board_input("\nEnter Goal State:")

    solver = PuzzleSolver(initial_state, goal_state)

    print("\nSolving using DFS...")
    path = solver.solve_dfs()

    display_solution(path, "DFS")


main()