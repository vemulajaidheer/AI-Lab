"""
8-Puzzle using A* Search
f(n) = g(n) + h(n)
  g(n) = Depth of the node
  h(n) = Number of Misplaced Tiles
"""

import heapq

GOAL = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)      


def h_misplaced(state):
    """Number of tiles (excluding blank) not in their goal position."""
    return sum(1 for i in range(9) if state[i] != 0 and state[i] != GOAL[i])


def get_neighbors(state):
    """Generate all states reachable by moving the blank one step."""
    neighbors = []
    b = state.index(0)
    r, c = divmod(b, 3)
    for dr, dc, move in [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            nb = nr * 3 + nc
            s = list(state)
            s[b], s[nb] = s[nb], s[b]
            neighbors.append((tuple(s), move))
    return neighbors


def is_solvable(state):
    tiles = [t for t in state if t != 0]
    inv = sum(1 for i in range(len(tiles)) for j in range(i + 1, len(tiles)) if tiles[i] > tiles[j])
    return inv % 2 == 0


def print_state(state):
    for i in range(0, 9, 3):
        print(" ".join("_" if t == 0 else str(t) for t in state[i:i + 3]))
    print()


def a_star(start):
    # Each entry in the open list: (f, g, state, path)
    open_list = [(h_misplaced(start), 0, start, [])]
    visited = set()
    nodes_expanded = 0

    while open_list:
        f, g, state, path = heapq.heappop(open_list)

        if state == GOAL:
            return path, nodes_expanded

        if state in visited:
            continue
        visited.add(state)
        nodes_expanded += 1

        for nxt, move in get_neighbors(state):
            if nxt not in visited:
                g_new = g + 1                  # depth of child node
                h_new = h_misplaced(nxt)       # misplaced tiles
                f_new = g_new + h_new
                heapq.heappush(open_list, (f_new, g_new, nxt, path + [(move, nxt)]))
    return None, nodes_expanded


if __name__ == "__main__":
    print("Enter the start state (9 numbers, use 0 for blank)")
    print("Example: 1 2 3 0 4 6 7 5 8")
    user_input = input("Start state: ").strip()
    start = tuple(map(int, user_input.split())) if user_input else (1, 2, 3, 0, 4, 6, 7, 5, 8)

    print("\nInitial State:")
    print_state(start)

    if not is_solvable(start):
        print("This puzzle is not solvable.")
    else:
        path, expanded = a_star(start)
        g = 0
        print(f"Start  ->  g={g}, h={h_misplaced(start)}, f={g + h_misplaced(start)}")
        print_state(start)
        for move, state in path:
            g += 1
            h = h_misplaced(state)
            print(f"Move blank {move}  ->  g={g}, h={h}, f={g + h}")
            print_state(state)
        print("Goal reached!")
        print("Number of moves :", len(path))
        print("Nodes expanded  :", expanded)
