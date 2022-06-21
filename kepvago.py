import os
import string
import cv2
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Form(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Képvágó program")
        self.value_entry = tk.StringVar()

    def submit_button(self, text, command):
        button = tk.Button(self, text=text, command=command)
        button.pack()

    def f_dialog(self):
        filepath = filedialog.askopenfilename(initialdir = "/",title = "Tallóz", filetypes = (("png files","*.png"),("all files","*.*")))
        self.value_entry.set(filepath)
        self.destroy()

    def label(self, text):
        label = tk.Label(self, text = text)
        label.pack()

    def set_window(self):
        width = self.winfo_screenwidth()               
        height = self.winfo_screenheight()               
        self.geometry(f'{width}x{height}')
         

class CropRect(Form):

    def __init__(self, path):  # path of image 
        self.window = Form()  # with Tkinter
        self.path = path
        self.img1 = cv2.imread(self.path)
        self.img2 = cv2.cvtColor(self.img1, cv2.COLOR_BGR2RGB) # png!
        self.fig = plt.figure(figsize=(9, 7), dpi=180)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.window)
        self.points = []
        self.pts = []
        
        self.window.protocol('WM_DELETE_WINDOW', lambda:[ self.window.quit(), self.window.destroy()]) # X button - close window
    

    def main_window(self):

        " Set canvas to marking points before cropping "

        " Without Tkinter "

        # self.fig.canvas.mpl_connect('button_press_event', self.__onclick)
        # plt.imshow(self.img2)
        # plt.show()
        # self.__crop()

        " With Tkinter "

        self.window.set_window()

        # File name and save button

        self.window.label('Kép: ' + self.path)
        self.window.submit_button("MENTÉS", self.__crop)  # last proceed
        
        # Canvas, marking points
        
        self.fig.canvas.mpl_connect('button_press_event', self.__onclick)
        plt.imshow(self.img2)

        # Canvas on the window

        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.window.mainloop()


    def __onclick(self,event):
        
        " Onclick event -> draw the points, add pixel's x,y coordinates to list "
        
        if len(self.points) >= 2:  # needed max 2 points!
            self.points = []
            plt.clf()
            plt.imshow(self.img2)
        
        self.points.append((event.xdata,event.ydata))
        plt.plot(event.xdata,event.ydata, marker='.', color='#00FFFF', markersize=5)
        self.fig.canvas.draw()
        

    def __crop(self):
        
        " Crop the image then save the croped one "
        
        self.pts = np.array(self.points, np.dtype('int'))
        
        # Crop the bounding rect
        
        rect = cv2.boundingRect(self.pts)
        x,y,w,h = rect
        cropped = self.img1[y:y+h, x:x+w]

        # Mask the image
        # Soon ...
        
        # Save new image to new folder

        self.__saveNewImg(cropped)

        # Tkinter success

        messagebox.showinfo("Mentés","A kivágott kép elmentve!\n")


    def __saveNewImg(self, image):
        
        folder_name = "img" #self.path[:-4]
        if os.path.exists(folder_name) == False:
            os.mkdir(folder_name)
        
        nums_crp_im = len(os.listdir(folder_name))
        cv2.imwrite(f'{folder_name}\\{string.ascii_uppercase[nums_crp_im]}.jpg', image) # new cropped image


if __name__ == "__main__":

    " Without Tkinter\window1 "

    # image = 'marc_zold_4.png'
    # path = f'f:\\pixel\\repce_2021\\Repce 2021\\kivalasztott\\{image}'

    " With Tkinter "
    
    " 1. Upload window - choose png image "

    window1 = Form()
    window1.title("Kép betöltése")
    window1.geometry('250x250')
    window1.submit_button("KÉP BETÖLTÉSE", window1.f_dialog)
    path = window1.value_entry
    window1.mainloop()
    
    " Start "
    print(path.get())
    t = CropRect(path.get())  #  (path.get()) --> with Tkinter & window1 ; (path) --> without Tkinter or window1 ;
    t.main_window()
        

    