import tkinter as tk
from ui import GraphApp

# Initialise main application window
root = tk.Tk()
root.title("Graph Visualiser")
root.geometry("800x600")

app = GraphApp(root)
root.mainloop()