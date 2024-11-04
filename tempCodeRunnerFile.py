import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set up the figure
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 12)
ax.axis('off')

# Define colors and styles for the boxes and arrows
box_color = "#4CAF50"
text_color = "white"
arrow_color = "black"

# Helper function to add a box with text
def add_box(ax, text, x, y, width=2, height=0.8, color=box_color):
    box = patches.FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.2", edgecolor="none", facecolor=color)
    ax.add_patch(box)
    ax.text(x + width / 2, y + height / 2, text, ha="center", va="center", fontsize=10, color=text_color, weight="bold")
    return box

# Helper function to add arrows connecting box edges
def add_arrow(ax, box_from, box_to, color=arrow_color, curve=False, curve_dir='left'):
    # Calculate coordinates for arrow connection
    x1, y1 = box_from.get_x() + box_from.get_width() / 2, box_from.get_y()
    x2, y2 = box_to.get_x() + box_to.get_width() / 2, box_to.get_y() + box_to.get_height()
    if curve:
        style = 'arc3,rad=-0.3' if curve_dir == 'left' else 'arc3,rad=0.3'
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5, connectionstyle=style))
    else:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.5))

# Boxes and text
box_game_rules = add_box(ax, "Game Rules\nand Setup", 4.5, 10, width=2.5)
box_algorithms = add_box(ax, "Algorithm Selection\nand Integration", 4.5, 8, width=2.5)

# Algorithm boxes in a single row with reduced width and height
box_alpha_beta = add_box(ax, "Alpha-Beta Pruning", 0.5, 6, width=2)
box_genetic = add_box(ax, "Genetic Algorithm", 3.5, 6, width=2)
box_fuzzy = add_box(ax, "Fuzzy Logic", 6.5, 6, width=2)
box_astar = add_box(ax, "A* Algorithm", 9.5, 6, width=2)

# Additional boxes
box_ui = add_box(ax, "Tkinter UI\nImplementation", 4.5, 2, width=2.5)
box_eval = add_box(ax, "Evaluation\nand Testing", 4.5, 0, width=2.5)

# Arrows between boxes
add_arrow(ax, box_game_rules, box_algorithms)  # Arrow from Game Rules to Algorithm Selection
add_arrow(ax, box_algorithms, box_alpha_beta)  # Arrow to Alpha-Beta Pruning
add_arrow(ax, box_algorithms, box_genetic)  # Arrow to Genetic Algorithm
add_arrow(ax, box_algorithms, box_fuzzy)  # Arrow to Fuzzy Logic
add_arrow(ax, box_algorithms, box_astar)  # Arrow to A* Algorithm
add_arrow(ax, box_alpha_beta, box_ui, curve=True, curve_dir='right')  # Curved arrow from Alpha-Beta to UI
add_arrow(ax, box_genetic, box_ui)  # Arrow from Genetic Algorithm to UI
add_arrow(ax, box_fuzzy, box_ui, curve=True, curve_dir='left')  # Curved arrow from Fuzzy Logic to UI
add_arrow(ax, box_astar, box_ui, curve=True, curve_dir='left')  # Curved arrow from A* to UI
add_arrow(ax, box_ui, box_eval)  # Arrow from UI to Evaluation

# Show plot
plt.title("Methodology Flowchart for DoRa Block Battle", fontsize=14, weight="bold")
plt.show()
