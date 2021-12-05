import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import json
import os
import http.client, urllib.parse

DIR = os.path.dirname(__file__)
### the map
theMap = 'greece.png'
###
conn = http.client.HTTPConnection('geocode.xyz')

# copy images from https://www.openstreetmap.org/#map=10/38.2444/21.4207&layers=T

class Map(tk.Frame):
    def __init__(self, map):
        tk.Frame.__init__(self)
        self.pack(expand=True, fill='both')
        self.img = tk.PhotoImage(file=os.path.join(DIR, map))
        self.coffeImg = tk.PhotoImage(file = os.path.join(DIR,'myCoffee.gif'))
        self.exit = tk.PhotoImage(file=os.path.join(DIR,'exit.gif'))
        self.canvas = tk.Canvas(self, width=self.img.width(), height=self.img.height())
        print(self.img.width(), self.img.height())
        self.canvas.pack(expand=True)
        self.canvas.create_image(0,0, image=self.img, anchor='nw')
        self.exitMenu = self.canvas.create_image(self.img.width()-self.exit.width(),0, image=self.exit, anchor='nw')
        self.canvas.tag_bind(self.exitMenu,'<Button-1>', lambda e: self.saveMapData(e))
        self.canvas.bind('<Button-1>', lambda e: self.coordinates(e))
        self.readMapData()
        self.showMyCoffee()

    def showMyCoffee(self):
        for city in self.mapping:
            self.canvas.create_image(self.mapping[city]['x'], self.mapping[city]['y'], image = self.coffeImg)

    def readMapData(self):
        jsonFile = theMap.rstrip(".png")+".json"
        print('reading from JSON file...', jsonFile)
        if jsonFile in os.listdir():
            with open(os.path.join(DIR, jsonFile), 'r', encoding='utf-8') as f:
                self.mapping = json.load(f)
        else: self.mapping = {}

    def saveMapData(self, e):
        if self.mapping:
            jsonObject = json.dumps(self.mapping, indent = 4)
            with open(os.path.join(DIR,theMap.rstrip(".png")+".json"), 'w', encoding='utf-8') as f:
                f.write(jsonObject)
        root.destroy()

    def coordinates(self, e):
        print(e.x, e.y)
        reply = simpledialog.askstring(f'Τοπωνύμιο σημείου {e.x},{e.y}', 'όνομα σημείου:', parent=root)
        print(reply)
        if reply:
            try: 
                params = urllib.parse.urlencode({'locate': reply, 'region': 'GR', 'json': 1, })
                conn.request('GET', '/?{}'.format(params))
                res = conn.getresponse()
                data = json.loads(res.read().decode('utf-8'))
                print(data)
                if 'alt' in data and 'loc' in data['alt']:
                    self.mapping[reply] = {'x':e.x, 'y':e.y, 'latt':float(data['latt']), 'longt':float(data['longt'])}
                    messagebox.showinfo('info', f"Προστέθηκαν οι συντεταγμένες για το τοπωνύμιο {reply}")
                else:
                    messagebox.showinfo('error', f"ΣΦΑΛΜΑ! δεν προστέθηκαν οι συντεταγμένες για το τοπωνύμιο {reply}")
            except:
                messagebox.showinfo('error', f"ΣΦΑΛΜΑ! δεν προστέθηκαν οι συντεταγμένες για το τοπωνύμιο {reply}")

            print (self.mapping)

if __name__ == "__main__":
    root = tk.Tk()
    greece = Map(theMap)
    root.mainloop()
