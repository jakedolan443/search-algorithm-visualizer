import tkinter as tk
from random import choice


class Grid(tk.Canvas):
    def __init__(self, *args):
        tk.Canvas.__init__(self, *args, bg='white', width=800, height=800, relief='groove')
        self.get_root().grid = self
        
        self.get_root().coord_data = {}
        self.get_root().coord_data['start'] = None
        self.get_root().coord_data['finish'] = None
        
        self.highlight_cache = []
        self.in_search = False
        self.draw()
        
        self.mouse_x, self.mouse_y = 1, 1
        self.nearest_cache = 1, 1
        self.fill_cache = ""
        
        self.bind("<Motion>", self.motion)
        self.bind("<B1-Motion>", self.place_move)
        self.bind("<ButtonPress-1>", self.place)
        self.bind("<ButtonRelease-1>", self.place_release)
        self.mainloop()
        
    def get_root(self):
        return self.master.master.get_root()
    
    def draw(self, data=None):
        self.reset()    
        self.delete(tk.ALL)
        
        self.get_root().coord_data['start'] = None
        self.get_root().coord_data['finish'] = None
        
        self.w, self.h = 800, 800
        self.wl, self.hl = self.get_root().options['grid_size'][0], self.get_root().options['grid_size'][1]
        self.ws, self.hs = self.w/self.wl, self.h/self.hl
        
        
        self.grid = {}
        for w in range(self.wl):
            self.grid[w] = {}
            for h in range(self.hl):
                self.grid[w][h] = {}
                if data:
                    self.grid[w][h]['state'] = data[w][h]
                else:
                    self.grid[w][h]['state'] = 0
                if self.grid[w][h]['state'] == 0:
                    self.grid[w][h]['obj'] = self.create_rectangle(self.ws, self.hs, 0, 0, fill='', width=1)
                elif self.grid[w][h]['state'] == 1:
                    self.grid[w][h]['obj'] = self.create_rectangle(self.ws, self.hs, 0, 0, fill='red', width=1)
                    self.get_root().coord_data['start'] = w, h
                elif self.grid[w][h]['state'] == 2:
                    self.grid[w][h]['obj'] = self.create_rectangle(self.ws, self.hs, 0, 0, fill='green', width=1)
                    self.get_root().coord_data['finish'] = w, h
                else:
                    self.grid[w][h]['obj'] = self.create_rectangle(self.ws, self.hs, 0, 0, fill='black', width=1)
                self.move(self.grid[w][h]['obj'], (w*self.ws)+0.45, (h*self.hs)+0.5)
        self.reset()
                
    def motion(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y
                
    def get_nearest(self, x1, y1):
        
        
        
        return int(x1/self.ws), int(y1/self.hs)
    
    def place_move(self, event):
        
        if not self.in_search:
        
            try:
        
                if self.get_root().mode == "wall":
                    w, h = self.get_nearest(event.x, event.y)
                    if (w, h) == self.get_root().coord_data['start']:
                        self.get_root().coord_data['start'] = None
                    elif (w, h) == self.get_root().coord_data['finish']:
                        self.get_root().coord_data['finish'] = None
                    self.itemconfig(self.grid[w][h]['obj'], fill='black')
                    self.grid[w][h]['state'] = 3
                else:
                    self.mouse_x, self.mouse_y = event.x, event.y
                    
            except Exception as e:
                pass
            
    def place(self, event):
        if not self.in_search:
            
            try:
            
                self.reset()
                
                self.nearest_cache = None
                if self.get_root().mode == "start":
                    try:
                        self.itemconfig(self.grid[self.get_root().coord_data['start'][0]][self.get_root().coord_data['start'][1]]['obj'], fill='')
                    except TypeError:
                        pass
                    w, h = self.get_nearest(event.x, event.y)
                    self.itemconfig(self.grid[w][h]['obj'], fill='red')
                    self.grid[w][h]['state'] = 1
                    self.get_root().coord_data['start'] = w, h
                    
                    self.clear_cursor()
                    
                elif self.get_root().mode == "finish":
                    try:
                        self.itemconfig(self.grid[self.get_root().coord_data['finish'][0]][self.get_root().coord_data['finish'][1]]['obj'], fill='')
                    except TypeError:
                        pass
                    w, h = self.get_nearest(event.x, event.y)
                    self.itemconfig(self.grid[w][h]['obj'], fill='green')
                    self.grid[w][h]['state'] = 2
                    self.get_root().coord_data['finish'] = w, h
                    
                    self.clear_cursor()
                    
                elif self.get_root().mode == "wall":
                    w, h = self.get_nearest(event.x, event.y)
                    self.itemconfig(self.grid[w][h]['obj'], fill='black')
                    self.grid[w][h]['state'] = 3
                    
            except Exception as e:
                pass
                
                
    def place_release(self, event):
        if not self.in_search:
            self.reset()
        
    def clear_cursor(self):
        self.nearest_cache = -1, -1
        self.get_root().mainframe.deselect_all()
                
    def get(self):
        grid = []
        for w in self.grid:
            grid.append([])
            for h in self.grid[w]:
                if self.grid[w][h]['state'] == 3:
                    grid[w].append(1)
                else:
                    grid[w].append(0)
        return grid
    
    def reset(self):
        try:
            if not self.in_search:
                self.get_root().status_var.set("\n\n")
                self.nearest_cache = -1, -1
                for coords in self.highlight_cache:
                    self.itemconfig(self.grid[coords[0]][coords[1]]['obj'], fill='')
                self.highlight_cache = []
                
                ## full clear, useful for bugs/errors
                for w in self.grid:
                    for h in self.grid[w]:
                        if (self.grid[w][h]['state']) == 0:
                            self.itemconfig(self.grid[w][h]['obj'], fill='')
        except Exception as e:
            pass
                
        
    def finish_search(self, route):
        try:
            for coords in route:
                if not coords == self.get_root().coord_data['start']:
                    if not coords == self.get_root().coord_data['finish']:
                        self.itemconfig(self.grid[coords[0]][coords[1]]['obj'], fill='red')
                        self.get_root().status_var.set("{}\nRoute length {}".format(self.get_root().status_var.get().split("\n")[0], len(route)))
        except Exception:
            pass
    
    def highlight(self, coords):
        try:
            if not coords == self.get_root().coord_data['start']:
                if not coords == self.get_root().coord_data['finish']:
                    self.highlight_cache.append(coords) if coords not in self.highlight_cache else self.highlight_cache
                    self.itemconfig(self.grid[coords[0]][coords[1]]['obj'], fill='pink')
                    self.get_root().status_var.set("Visited {}\n".format(len(self.highlight_cache)))
        except Exception:
            pass
                
    def export_walls(self):
        grid = []
        for w in self.grid:
            grid.append([])
            for h in self.grid[w]:
                grid[w].append(str(self.grid[w][h]['state']))
            grid[w] = ",".join(grid[w])
        grid = "\n".join(grid)
        return grid
        
    def random_draw(self):
        self.reset()    
        self.delete(tk.ALL)
        
        self.get_root().coord_data['start'] = None
        self.get_root().coord_data['finish'] = None
        
        self.w, self.h = 800, 800
        self.wl, self.hl = self.get_root().options['grid_size'][0], self.get_root().options['grid_size'][1]
        self.ws, self.hs = self.w/self.wl, self.h/self.hl
        
        
        self.grid = {}
        for w in range(self.wl):
            self.grid[w] = {}
            for h in range(self.hl):
                self.grid[w][h] = {}
                self.grid[w][h]['state'] = random.choice([0, 0, 0, 0, 3])
                if self.grid[w][h]['state'] == 0:
                    self.grid[w][h]['obj'] = self.create_rectangle(self.ws, self.hs, 0, 0, fill='', width=1)
                elif self.grid[w][h]['state'] == 1:
                    self.grid[w][h]['obj'] = self.create_rectangle(self.ws, self.hs, 0, 0, fill='red', width=1)
                    self.get_root().coord_data['start'] = w, h
                elif self.grid[w][h]['state'] == 2:
                    self.grid[w][h]['obj'] = self.create_rectangle(self.ws, self.hs, 0, 0, fill='green', width=1)
                    self.get_root().coord_data['finish'] = w, h
                else:
                    self.grid[w][h]['obj'] = self.create_rectangle(self.ws, self.hs, 0, 0, fill='black', width=1)
                self.move(self.grid[w][h]['obj'], (w*self.ws)+0.45, (h*self.hs)+0.5)
        self.reset()
                
    def mainloop(self):
        
        if not self.in_search:
        
            try:
                
                try:
                    self.itemconfig(self.grid[self.nearest_cache[0]][self.nearest_cache[1]]['obj'], fill='{}'.format(self.fill_cache))
                except Exception:
                    pass
                
                w, h = self.get_nearest(self.mouse_x, self.mouse_y)
                self.fill_cache = self.itemcget(self.grid[w][h]['obj'], "fill")
                self.nearest_cache = w, h
                
                
                
                if self.get_root().mode == "start":
                    self.itemconfig(self.grid[w][h]['obj'], fill='red')
                elif self.get_root().mode == "finish":
                    self.itemconfig(self.grid[w][h]['obj'], fill='green')
                elif self.get_root().mode == "wall":
                    self.itemconfig(self.grid[w][h]['obj'], fill='black')
                    
            except Exception:
                pass
        
        
        self.after(1, self.mainloop)
        
