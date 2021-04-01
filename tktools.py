import tkinter as tk
import webbrowser


class Hyperlink(tk.Label):
    def __init__(self, *args, url="", text=""):
        tk.Label.__init__(self, *args)
        
        self.url = url
        self.text = text
        if not text:
            self.text = self.url
            
        self.config(fg="blue", cursor="hand2", font='System, 7', text="{}".format(self.text))
        self.bind("<Button-1>", lambda e: webbrowser.open_new(r"{}".format(url)))
        self.bind("<Enter>", lambda e: e.widget.config(font='System, 7 underline'))
        self.bind("<Leave>", lambda e: e.widget.config(font='System, 7'))
        
        
class ToggleMenu(tk.LabelFrame):
    def __init__(self, *args, **kwargs):
        tk.LabelFrame.__init__(self, *args, text=kwargs['text'])
        self.var = {}
        self.command = kwargs['command']
        
    def sink_all(self):
        for var in self.var:
            self.var[var].config(relief='sunken')
        
    def raise_all(self):
        for var in self.var:
            self.var[var].config(relief='raised')
        self.command(None)
        
    def add_toggle(self, text, image, identifier):
        self.var[identifier] = tk.Button(self, text=text, font='System, 10', image=image, compound="left", command=lambda: self._toggle_id(identifier), width=105, anchor='w')
        self.var[identifier].pack()
        
    def _toggle_id(self, identifier):
        self.sink_all()
        self.var[identifier].config(relief='raised')
        self.command(identifier)
        
class BlueprintFrame(tk.Frame):
    def __init__(self, *args):
        tk.Frame.__init__(self)
        
        
