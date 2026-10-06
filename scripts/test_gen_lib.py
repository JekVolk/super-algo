#!/usr/bin/env python3
"""
Test Generator Utility Library for Competitive Programming.
Generates arrays, permutations, trees (random, bamboo, star), graphs, and grids.
"""

import random
import string
from typing import List, Tuple

def gen_array(n: int, min_val: int = 1, max_val: int = 10**9, sorted_arr: bool = False, distinct: bool = False) -> List[int]:
    """Generates an array of n integers."""
    if distinct:
        if max_val - min_val + 1 < n:
            raise ValueError("Range is too small for distinct elements")
        arr = random.sample(range(min_val, max_val + 1), n)
    else:
        arr = [random.randint(min_val, max_val) for _ in range(n)]
    if sorted_arr:
        arr.sort()
    return arr

def gen_permutation(n: int, one_indexed: bool = True) -> List[int]:
    """Generates a random permutation of length n."""
    base = list(range(1 if one_indexed else 0, n + (1 if one_indexed else 0)))
    random.shuffle(base)
    return base

def gen_string(length: int, alphabet: str = string.ascii_lowercase) -> str:
    """Generates a random string of given length using alphabet."""
    return "".join(random.choice(alphabet) for _ in range(length))

def gen_tree(n: int, tree_type: str = "random", one_indexed: bool = True) -> List[Tuple[int, int]]:
    """
    Generates a tree with n vertices.
    Supported types:
    - 'random': Random tree with average depth O(sqrt(n)) or O(log n)
    - 'bamboo': Linear chain (depth n - 1), perfect for stack overflow tests
    - 'star': Node 1 connected to all other nodes (high degree test)
    - 'caterpillar': Central spine with random leaves attached
    """
    if n < 1:
        return []
    if n == 1:
        return []

    shift = 1 if one_indexed else 0
    edges: List[Tuple[int, int]] = []

    if tree_type == "bamboo":
        perm = list(range(n))
        random.shuffle(perm)
        for i in range(n - 1):
            edges.append((perm[i] + shift, perm[i + 1] + shift))

    elif tree_type == "star":
        center = random.randint(0, n - 1)
        for i in range(n):
            if i != center:
                edges.append((center + shift, i + shift))

    elif tree_type == "caterpillar":
        spine_len = max(2, n // 3)
        spine = list(range(spine_len))
        random.shuffle(spine)
        for i in range(spine_len - 1):
            edges.append((spine[i] + shift, spine[i + 1] + shift))
        for i in range(spine_len, n):
            attach_to = random.choice(spine)
            edges.append((attach_to + shift, i + shift))

    else:  # 'random' (Prufer or random attachment)
        for i in range(1, n):
            parent = random.randint(0, i - 1)
            edges.append((parent + shift, i + shift))
        # Randomize vertex labels
        perm = list(range(n))
        random.shuffle(perm)
        edges = [(perm[u - shift] + shift, perm[v - shift] + shift) for u, v in edges]

    # Shuffle edge order and directions
    random.shuffle(edges)
    edges = [(v, u) if random.random() < 0.5 else (u, v) for u, v in edges]
    return edges

def gen_graph(n: int, m: int, connected: bool = True, directed: bool = False, weighted: bool = False, min_w: int = 1, max_w: int = 100, one_indexed: bool = True) -> List[tuple]:
    """Generates a graph with n vertices and m edges."""
    shift = 1 if one_indexed else 0
    max_possible_edges = n * (n - 1) if directed else (n * (n - 1)) // 2
    m = min(m, max_possible_edges)

    edge_set = set()
    edges = []

    if connected and n > 1:
        tree_edges = gen_tree(n, "random", one_indexed)
        for u, v in tree_edges:
            edge_set.add((u, v) if directed else (min(u, v), max(u, v)))
            w = random.randint(min_w, max_w) if weighted else None
            edges.append((u, v, w) if weighted else (u, v))

    while len(edges) < m:
        u = random.randint(0, n - 1) + shift
        v = random.randint(0, n - 1) + shift
        if u == v:
            continue
        key = (u, v) if directed else (min(u, v), max(u, v))
        if key in edge_set:
            continue
        edge_set.add(key)
        w = random.randint(min_w, max_w) if weighted else None
        edges.append((u, v, w) if weighted else (u, v))

    random.shuffle(edges)
    return edges

def format_tree_input(n: int, edges: List[Tuple[int, int]]) -> str:
    """Formats tree into standard competitive input string."""
    lines = [str(n)]
    for u, v in edges:
        lines.append(f"{u} {v}")
    return "\n".join(lines)

if __name__ == "__main__":
    print("Приклад генерації бамбука (N=5):")
    print(format_tree_input(5, gen_tree(5, "bamboo")))
    print("\nПриклад генерації зв'язного зваженого графа (N=4, M=5):")
    g = gen_graph(4, 5, connected=True, weighted=True)
    for u, v, w in g:
        print(f"{u} -> {v} (вага: {w})")
