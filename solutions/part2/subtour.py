"""Solution for Exercise 1: Subtour Detection."""

from collections import defaultdict


def find_subtours(selected_edges, n_nodes):
    adj = defaultdict(set)
    for i, j in selected_edges:
        adj[i].add(j)
        adj[j].add(i)

    visited = set()
    components = []

    for node in range(n_nodes):
        if node in visited:
            continue
        component = set()
        stack = [node]
        while stack:
            v = stack.pop()
            if v in visited:
                continue
            visited.add(v)
            component.add(v)
            for neighbor in adj[v]:
                if neighbor not in visited:
                    stack.append(neighbor)
        components.append(component)

    if len(components) == 1:
        return []
    return components
