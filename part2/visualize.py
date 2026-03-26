"""
Visualize TSP solutions.

Usage:
    python visualize.py [--cities N] [--seed S] [--compact]
"""

import argparse
import random

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np


# Style matching the TikZ slides
NODE_COLOR = '#4444CC'
NODE_SIZE = 220
NODE_FONT = {'color': 'white', 'fontweight': 'bold', 'fontsize': 7}
EDGE_BG_COLOR = '#CCCCCC'
EDGE_BG_ALPHA = 0.3
EDGE_BG_WIDTH = 0.5
TOUR_COLOR = '#8B0000'
TOUR_WIDTH = 2.5
SUBTOUR_COLORS = ['#CC7700', '#7700AA', '#007744', '#CC0044', '#0066CC']


def _draw_nodes(ax, coords, node_size=None, show_labels=None):
    """Draw blue filled circles with white number labels."""
    n = len(coords)
    if node_size is None:
        node_size = NODE_SIZE if n <= 30 else max(10, 300 // n)
    if show_labels is None:
        show_labels = n <= 30
    for i, (x, y) in enumerate(coords):
        ax.scatter(x, y, s=node_size, c=NODE_COLOR, zorder=5, edgecolors='#3333AA',
                   linewidths=0.5 if n > 30 else 1)
        if show_labels:
            ax.text(x, y, str(i), ha='center', va='center', zorder=6, **NODE_FONT)


def _draw_complete_graph(ax, coords):
    """Draw faded complete graph edges in background."""
    n = len(coords)
    for i in range(n):
        for j in range(i + 1, n):
            ax.plot([coords[i][0], coords[j][0]], [coords[i][1], coords[j][1]],
                    color=EDGE_BG_COLOR, alpha=EDGE_BG_ALPHA, linewidth=EDGE_BG_WIDTH, zorder=1)


def _draw_edges(ax, coords, edges, color=TOUR_COLOR, linewidth=TOUR_WIDTH):
    """Draw a set of edges."""
    for (i, j) in edges:
        ax.plot([coords[i][0], coords[j][0]], [coords[i][1], coords[j][1]],
                color=color, linewidth=linewidth, zorder=3, solid_capstyle='round')


def _draw_subtour_box(ax, coords, component, color, label):
    """Draw a dashed rounded rectangle around a subtour component."""
    all_pts = np.array(coords)
    span = max(all_pts.max(axis=0) - all_pts.min(axis=0))
    pad = span * 0.06

    points = np.array([coords[i] for i in component])
    x_min, y_min = points.min(axis=0) - pad
    x_max, y_max = points.max(axis=0) + pad

    rect = FancyBboxPatch(
        (x_min, y_min), x_max - x_min, y_max - y_min,
        boxstyle=f"round,pad={pad * 0.3:.2f}", linewidth=1.5,
        edgecolor=color, facecolor='none', linestyle='--', zorder=2,
    )
    ax.add_patch(rect)
    ax.text((x_min + x_max) / 2, y_max + pad * 0.5, label,
            ha='center', fontsize=9, color=color)


def plot_tour(coords, edges, title="TSP Tour", ax=None, show_complete=True):
    """Plot a valid tour."""
    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=(7, 7))

    n = len(coords)
    lw = TOUR_WIDTH if n <= 30 else max(0.8, 60 / n)

    if show_complete and n <= 30:
        _draw_complete_graph(ax, coords)

    _draw_edges(ax, coords, edges, color=TOUR_COLOR, linewidth=lw)
    _draw_nodes(ax, coords)

    ax.set_title(title, fontsize=13, color='#006600', fontweight='bold')
    ax.set_aspect('equal')
    ax.margins(0.08)
    ax.axis('off')
    return ax


def plot_subtours(coords, edges, components, title="Subtours", ax=None, show_complete=True):
    """Plot a solution with subtours, each component in a different color with a bounding box."""
    if ax is None:
        _, ax = plt.subplots(1, 1, figsize=(7, 7))

    if show_complete and len(coords) <= 30:
        _draw_complete_graph(ax, coords)

    for k, S in enumerate(components):
        color = SUBTOUR_COLORS[k % len(SUBTOUR_COLORS)]
        comp_edges = [(i, j) for (i, j) in edges if i in S and j in S]
        _draw_edges(ax, coords, comp_edges, color=color, linewidth=TOUR_WIDTH)
        items = ', '.join(str(i) for i in sorted(S))
        _draw_subtour_box(ax, coords, S, color, f'$S_{{{k+1}}}$ = {{{items}}}')

    _draw_nodes(ax, coords)

    ax.set_title(title, fontsize=13, color='#CC0000', fontweight='bold')
    ax.set_aspect('equal')
    ax.margins(0.08)
    ax.axis('off')
    return ax


def get_coords(n_cities, seed=None, grid_size=100):
    """Regenerate the same coordinates used by random_euclidean_tsp."""
    if seed is not None:
        random.seed(seed)
    return [(random.uniform(0, grid_size), random.uniform(0, grid_size))
            for _ in range(n_cities)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cities', type=int, default=20)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--compact', action='store_true', help='Use MTZ formulation')
    args = parser.parse_args()

    coords = get_coords(args.cities, args.seed)

    from generator import random_euclidean_tsp
    distances = random_euclidean_tsp(args.cities, seed=args.seed)

    if args.compact:
        from compact_mtz import tsp_mtz
        model, x = tsp_mtz(distances)
        label = "MTZ"
    else:
        from tsp import tsp_rowgen
        model, x = tsp_rowgen(distances)
        label = "Row Generation"

    print(f"Solving {args.cities}-city TSP with {label}...", end=" ", flush=True)
    model.optimize()
    print(f"done ({model.getSolvingTime():.1f}s)")

    # Extract selected edges
    if args.compact:
        selected = [(i, j) for (i, j) in x if model.getVal(x[i, j]) > 0.5]
    else:
        selected = [(i, j) for (i, j) in x if model.getVal(x[i, j]) > 0.5]

    # Check for subtours
    from subtour import find_subtours
    n = args.cities
    subtours = find_subtours(selected, n)

    obj = model.getObjVal()
    show_cg = n <= 30

    if subtours:
        plot_subtours(coords, selected, subtours,
                      title=f"Subtours ({len(subtours)} components)",
                      show_complete=show_cg)
    else:
        plot_tour(coords, selected,
                  title=f"{label} — {n} cities, cost={obj:.0f}",
                  show_complete=show_cg)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
