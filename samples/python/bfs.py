from collections import deque

def bfs(graph: dict, start_node: str) -> list:
    """
    Breadth-First Search.
    Tests deque and set usage.
    """
    visited = set()
    queue = deque([start_node])
    visited.add(start_node)
    order = []
    
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order
