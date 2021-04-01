import tkinter as tk
import tktools
from algs.astar import astar
from algs.dijkstra import dijkstra
import numpy as np
import threading
from tkinter import filedialog
import random
from grid import Grid



class Frame(tk.Frame):
    def __init__(self, *args):
        tk.Frame.__init__(self, *args)
        
    def get_root(self):
        return self.master.get_root()

class Mainframe(tk.Frame):
    def __init__(self, *args):
        tk.Frame.__init__(self, *args)
        self.get_root().mainframe = self
        
        self.images = {}
        self.images['start.png'] = tk.PhotoImage(file="images/start.png")
        self.images['finish.png'] = tk.PhotoImage(file="images/finish.png")
        self.images['wall.png'] = tk.PhotoImage(file="images/wall.png")
        self.images['remove.png'] = tk.PhotoImage(file="images/remove.png")
        
        
        gridframe = Frame(self)
        gridframe.pack(side=tk.RIGHT, anchor='n', expand=True, fill='y')
        menuframe = Frame(self)
        menuframe.pack(side=tk.LEFT, anchor='w', expand=True, fill='y')
        
        self.grid = Grid(gridframe)
        self.grid.pack(anchor='e')
        
        
        
        
        text = tk.Label(menuframe, text="\n   Search Algorithm   \nVisualizer", font='System, 13')
        text.pack(side=tk.TOP)
        hyperlink = tktools.Hyperlink(menuframe, url="https://github.com/jakedolan443/search-algorithm-visualizer", text="https://github.com/jakedolan443/\nsearch-algorithm-visualizer")
        hyperlink.pack()
        separation = tk.Label(menuframe, text="\n")
        separation.pack(fill='x')
        
        optionList = ('Dijkstra', 'Astar', 'Bellman-Ford')
        self.v = tk.StringVar()
        self.v.set(optionList[0])
        self.v.trace("w", self.set_alg)
        algmenu = tk.OptionMenu(menuframe, self.v, *optionList)
        algmenu.config(width=13, font='System, 8')
        algmenu.pack()
        
        status_label = tk.Label(menuframe, textvariable=self.get_root().status_var, font='System, 8')
        status_label.pack()
        
        separation = tk.Label(menuframe, text="\n")
        separation.pack(fill='x')
        
        action_menu = tk.LabelFrame(menuframe, text="Actions")
        simulate_button = tk.Button(action_menu, text="Simulate", font='System, 10', width=13, command=self.simulate)
        simulate_button.pack()
        reset_button = tk.Button(action_menu, text="Reset", font='System, 10', width=13, command=self.grid.reset)
        reset_button.pack()
        action_menu.pack()
        separation = tk.Label(menuframe, text="\n")
        separation.pack(fill='x')
        
        togglemenu = tktools.ToggleMenu(menuframe, text="Tools", command=self.set_tool)
        self.tool_menu = togglemenu
        togglemenu.pack()
        togglemenu.add_toggle("Start", self.images['start.png'], "start")
        togglemenu.add_toggle("Finish", self.images['finish.png'], "finish")
        togglemenu.add_toggle("Wall", self.images['wall.png'], "wall")
        togglemenu.add_toggle("Remove", self.images['remove.png'], "remove")
        menuframe.bind("<Button-1>", lambda e: togglemenu.raise_all())
        separation = tk.Label(menuframe, text="\n")
        separation.pack(fill='x')
        
        wall_menu = tk.LabelFrame(menuframe, text="Grid")
        clear_button = tk.Button(wall_menu, text="Clear", font='System, 10', width=13, command=self.grid.draw)
        clear_button.pack()
        random_button = tk.Button(wall_menu, text="Random", font='System, 10', width=13, command=self.grid.random_draw)
        random_button.pack()
        load_blueprint = tk.Button(wall_menu, text="Load Blueprint", font='System, 10', width=13, command=self.import_grid)
        load_blueprint.pack()
        save_blueprint = tk.Button(wall_menu, text="Save Blueprint", font='System, 10', width=13, command=self.export_grid)
        save_blueprint.pack()
        wall_menu.pack()
        
    def get_root(self):
        return self.master.get_root()
    
    def import_grid(self):
        filename = filedialog.askopenfilename(defaultextension="*.visgrid", initialdir="templates/", filetypes=[('Search Algorithm Grid File','*.visgrid')])
        f = open("{}".format(filename), "rb")
        data = f.read().decode()
        f.close()
        
        
        metadata = data.split("///\n")[0]
        self.get_root().options['grid_size'][0], self.get_root().options['grid_size'][1] = int(metadata.split("x")[0]), int(metadata.split("x")[1]) 
        
        grid = data.split("///\n")[1]
        grid = grid.split("\n")
        for i in range(len(grid)):
            grid[i] = grid[i].split(",")
            for j in range(len(grid[i])):
                grid[i][j] = int(grid[i][j])
        
        self.grid.draw(data=grid)
    
    def export_grid(self):
        metadata = "{}x{}".format(self.get_root().options['grid_size'][0], self.get_root().options['grid_size'][1])
        grid = self.grid.export_walls()
        grid = "{}///\n{}".format(metadata, grid)

        f = filedialog.asksaveasfile(mode='wb', defaultextension="*.visgrid", initialdir="templates/", filetypes=[('Search Algorithm Grid File','*.visgrid')])
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        f.write(grid.encode())
        f.close() 
    
    def deselect_all(self):
        self.tool_menu.raise_all()
    
    def set_tool(self, tool):
        self.get_root().mode = tool
        
    def set_alg(self, *args):
        self.get_root().algorithm = self.v.get()
        
    def simulate(self):
        if not self.grid.in_search:
            self.tool_menu.raise_all()
            self.grid.reset()
            grid = self.grid.get()
            grid = np.asarray(grid)
            thread = threading.Thread(target = self.get_root().algorithms[self.get_root().algorithm], args = (self.grid, grid, self.get_root().coord_data['start'], self.get_root().coord_data['finish'], ))
            thread.start()
            


class Menu(tk.Menu):
    def __init__(self, *args):
        tk.Menu.__init__(self, *args)
        self.get_root().menu = self

        submenu = tk.Menu(self, tearoff=0)
        
        self.grid_size_var = tk.StringVar()
        submenu.add_radiobutton(label="8x8", command=self._size_update, variable=self.grid_size_var)
        submenu.add_radiobutton(label="16x16", command=self._size_update, variable=self.grid_size_var)
        submenu.add_radiobutton(label="32x32", command=self._size_update, variable=self.grid_size_var)
        submenu.add_radiobutton(label="64x64", command=self._size_update, variable=self.grid_size_var)
        submenu.add_radiobutton(label="128x128", command=self._size_update, variable=self.grid_size_var)
        self.add_cascade(label="Grid", menu=submenu)
        
        submenu = tk.Menu(self, tearoff=0)
        
        self.search_speed_var = tk.StringVar(); self.search_speed_var.set("1ms")
        submenu.add_radiobutton(label="Max", command=self._speed_update, variable=self.search_speed_var)
        submenu.add_radiobutton(label="1ms", command=self._speed_update, variable=self.search_speed_var)
        submenu.add_radiobutton(label="10ms", command=self._speed_update, variable=self.search_speed_var)
        submenu.add_radiobutton(label="100ms", command=self._speed_update, variable=self.search_speed_var)

        self.add_cascade(label="Speed", menu=submenu)
        
    def get_root(self):
        return self.master.get_root()

    def _speed_update(self):
        if self.search_speed_var.get() == "Max":
            self.search_speed_var.set("0")
        self.get_root().options['speed'] = float(self.search_speed_var.get().split("ms")[0])

    def _size_update(self):
        self.get_root().options['grid_size'] = (list(map(int, self.grid_size_var.get().split("x"))))
        self.get_root().grid.draw()




class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("980x860")
        self.title("Search Algorithm Visualizer")
        self.tk_setPalette(background='#DDDDDD')
        self.resizable(False, False)
        
        self.status_var = tk.StringVar(); self.status_var.set("\n\n")
        self.algorithm = "Dijkstra"
        self.algorithms = {"Dijkstra":dijkstra, "Astar":astar}
        self.options = {'grid_size':[64, 64], 'speed':0.1}
        
        menu = Menu(self)
        self.config(menu=menu)
        
        self.mode = None
        mainframe = Mainframe(self)
        mainframe.pack(fill='both', expand=True)
        
        
        
        self.mainloop()
        
    def get_root(self):
        return self
        













