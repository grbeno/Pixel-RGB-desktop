from PIL import Image, ImageDraw, ImageFont 
import os, math
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


" ------------------------------------------------ KÉPELŐKÉSZíTÉS ------------------------------------------------ "


class CropImage:

    " *** HATÁROLÓK SZÁMOLÁSA ÉS ELLENŐRZÉSE *** "

    def __init__(self, im,path,cells, side=None,color=None,jump=None):
        """ A nem kötelező argumentumok az ecsetvonásos daraboláshoz szükségesek """
        self.im = im # ecsetvonásos vagy megmért kép
        self.path = path # ide menti a darabokat!
        self.cells = cells
        self.side = side  
        self.color = color
        self.jump = jump
        self.err, self.top = 0, 5
        self.border = []
        ImageAnalysis.init_image(self, self.im) # <- ImageAnalysis osztályból!
        self.w, self.h = self.width, self.height


    """ Függvények ecsetvonásos kép darabolásához """

    # Határolók számolása **

    def _borders(self):
        #ImageAnalysis.init_image(self, self.im) # <- ImageAnalysis osztályból!
        t, j = self.top, 0 # t-> ellenőrzés vonala
        R,G,B = self.color[0],self.color[1],self.color[2]
        try:
            while j < self.width:
                if self.pix[j,t][0] >= R and self.pix[j,t][1] <= G and self.pix[j,t][2] <= B: # ha ez az (R,G,B), akkor...
                    self.border.append(j)
                    j += self.jump # elugrás a jelöléstől, utolsónál helyet hagyni!
                else:
                    j += 1
            self.image.close()
        except:
            self.image.close()
            return print("Lehetséges hiba: túlfutott a program a képen, adjon meg kisebb ugrásközt!\n")
        self._valid() # **
        if self.err != 0:
            os._exit(1)
            # <- vissza a "menübe"!
        return self.border


    # Validálás **

    def _valid(self):
        if self.side == 1:
            dif = 1
        elif self.side == 2:
            dif = 0
        if self.cells*self.side > len(self.border)-dif:
            self.err = 1
            return print("Hiba: Kevesebb jelölés van mint a megadott paraméter!\n")
        elif self.cells*self.side < len(self.border)-dif:
            self.err = 1
            return print("Hiba: Több jelölés van mint a megadott paraméter!\n")
        else:
            pass

    
    # Darabolás

    def cropByColor(self, img):
        self._borders()
        ImageAnalysis.init_image(self, img) # <- ImageAnalysis osztályból!
        self.top, self.bottom = 5, self.height - 5
        for i in range(0,self.cells*self.side, self.side):
            item = self.image.crop((self.border[i], self.top, self.border[i+1], self.bottom)) # (left,top,right,bottom)
            item.save("%s\\%s%.2d.png" % (self.path,os.path.basename(img)[:-4],(i/self.side)+1))
            item.close()
        self.image.close()

        
    """ Függvény(ek) megmért kép darabolásához """

    # Darabolás
    
    def CropByWidth(self):  
        self.top, self.bottom = 5, self.h - 5
        i, n, border = 0, 0, self.w/self.cells
        while i < self.w:
            if n == self.cells:
                break
            left = i
            right = left + border
            if right >= self.w:
                right = self.w-1
            item = self.image.crop((left, self.top, right, self.bottom))
            item.save("%s%d.png" % (self.path,n+1))
            item.close()
            i += border
            n += 1
        self.image.close()
        


" ------------------------------------------ KÉPELEMZÉS - Inicializálás ------------------------------------------ "

class ImageAnalysis(CropImage):

    " *** KÉPEK ELEMZÉSE *** "
    
    " INICIALIZÁLÁS "

    def __init__(self, jel,c=None,colorS=None,sample=None,limit=None):
        self.path = c.path
        self.im = c.im
        self.im_w, self.im_h = c.w, c.h-10
        self.jel = jel
        self.mod = f"{self.path}mod\\"
        self.stain = f"{self.path}folt\\"
        self.marked = f"{self.path}jelölt\\"
        self.gray = f"{self.path}szürke\\"
        self.resdir = f"{self.path}eredmenyek\\"
        
        self.files = next(os.walk(self.path))[2]

        self.colorS = colorS
        self.sample = sample
        self.limit = limit
        
        # ... <-
        
        # Nevek a fejlécben
        
        self.fname = [f"Kép: {self.jel}"]
        self.sizes = ["Képméret (pixel)"] 
        self.distSum, self.distPerc = ["Távolság pixelek"], ["T_%"]
        self.avgsR, self.avgsG, self.avgsB = ["Átlag(R)"],["Átlag(G)"],["Átlag(B)"]
        self.freq = ["Leggyakoribb szín (szám,szín)"]
        self.light, self.dark = ["Világos"], ["Sötét"]
        
        # ... <-

        self.res_data = () # összegző tuple
        
    # Képet inicializál -> menteni/zárni kell!

    def init_image(self, fname,mode=None):
        self.image = Image.open(fname).convert(mode)
        self.pix = self.image.load()
        self.width, self.height = self.image.size
        self.imsize = self.width*self.height
    

    def mkdirIfNotExists(self, folderPath):
        if os.path.exists(folderPath) == False:
            os.mkdir(folderPath)
        else:
            pass
    

    def fileNameinFolder(self, folder):
        filename = f"{folder}{os.path.basename(os.path.dirname(folder))}_"
        return filename


    def getDataFromImg(self,color,paint=False):
        data = [int(i) for i in range(len(color))]
        for i in range(self.width):
            for j in range(self.height):
                for(id,lower,upper,col) in color:
                    if lower <= self.pix[i,j] and self.pix[i,j] <= upper:
                        if paint == True:
                            self.pix[i,j]=col # módosítja a képet!
                        count=data[id]
                        data[id]=count+1   
                        break
                    else:
                        continue
        return data

    # Azonosítás - alapkép megszámozása
    
    def labelim(self, parcella,jel):
        """ A parcellákat azonosítókkal és osztályzatokkal látja el - az alapképre (self.im <- CropImage) írja """
        self.init_image(self.im)
        draw = ImageDraw.Draw(self.image)
        if parcella > 50:
            font = ImageFont.truetype("arial.ttf", 15)
        else:
            font = ImageFont.truetype("arial.ttf", 25)
        posit = self.im_w/parcella
        step = 25
        for i in range(parcella):
            # Azonosítók
            if i != 0 and i != parcella-1:  # első és utolsó nélkül
                draw.text((step, self.im_h-20), "{:02d}".format(i), (255,255,255), font=font)
            # Osztályzatok
            if len(self.distPerc)>1: # ha vannak!
                draw.text((step, self.im_h/2),str(self.classify(self.distPerc)[i+1]),(255,255,0),font=font)
            step = step + posit
        new= f"{os.path.abspath(os.path.join(self.path,'..'))}{jel}_szamozott.jpg"
        self.image.save(new)
        self.image.close()        
    

    " ------------------------------------------ MÓDSZEREK - FÜGGVÉNYEK ------------------------------------------ "

    # 1. Euklideszi távolság
    
    def _euclidean(self, px): # minta-pixel;vizsgálati pixel
        res, channel = 0, 3 # R-G-B
        for i in range(channel):
            res = res + (self.sample[i]-px[i])**2
        return math.sqrt(res)

    def distance(self, paint=False):
        db = 0
        for i in range(self.width):
            for j in range(self.height):
                if self._euclidean(self.pix[i,j])<=self.limit:
                    if paint is True:
                        self.pix[i,j] = (255,0,0)
                        continue
                    db += 1
        return db

    # 1.1. Bonitálási osztályozás

    def classify(self,nums):
        nums = [float(i) for i in nums[1:]] # A 0. str elemet kihagyja, float(i) <- .2f int(i) <- 0f
        cls = 8 # fokozat/osztályzat
        m = max(nums)
        c = ["Osztályozás"]
        for n in nums:
            c.append(math.ceil(n/m*cls))
        return c

    # Százalékot számol egy elemre
    
    def percent(self, elem):
        p = format(elem/self.imsize*100,'.2f')
        return p
    
    " KÉPET LÉTREHOZÓ/MÓDOSíTÓ FÜGGVÉNYEK "

    # Pixeljelölő
    
    def find_and_mark(self, f):
        self.init_image(f'{self.path}{f}.png',"RGB")
        self.distance(paint=True)
        self.mkdirIfNotExists(self.marked)
        self.image.save(self.fileNameinFolder(self.marked)+str(f)+'.png')
        self.image.close()

    # 3. Foltképek
        
    def stainer(self, f): 
        
        " Szürkeárnyalatos képek "
        
        self.init_image(f'{self.path}{f}.png',"LA")
        self.mkdirIfNotExists(self.gray)
        path = self.fileNameinFolder(self.gray)+str(f)+'.png'
        self.image.save(path)
        self.image.close()
        
        " Színsávok -> foltok "
        
        self.init_image(path,"RGB")
        data = self.getDataFromImg(self.colorS,paint=True)
        self.mkdirIfNotExists(self.stain)
        self.image.save(self.fileNameinFolder(self.stain)+str(f)+'.png')
        self.image.close() 
        
        " Színek relatív gyakorisága "
        
        perc = []
        for n in data:
            perc.append(self.percent(n))
        self.light.append(perc[0])
        self.dark.append(perc[1])
        
    " EGYÉB KÉPINFORMÁCIÓK "

    # 4. Átlagszín
    
    def avg_color(self):
        color_tuple = [None, None, None]
        for channel in range(3):
            pixels = self.image.getdata(band=channel)
            values = []
            for pixel in pixels:
                values.append(pixel)
            color_tuple[channel] = format(sum(values)/len(values),'.0f')
        return tuple(color_tuple)


    # 5. Pixel gyakoriság
    
    def most_freq(self):
        pixels = self.image.getcolors(self.imsize) # (dbszám,rgb)
        most_frequent_pixel = pixels[0]
        for count, color in pixels:
            if count > most_frequent_pixel[0]:
                most_frequent_pixel = (count, color)
        return most_frequent_pixel

    # ... <-


    " ------------------------------------------ MÓDSZEREKET FUTTAT+KIMENET ------------------------------------------ "

    def exec_analysis(self):
        
        # Konvertálás a számsorrend miatt!

        files = []
        for f in self.files:
            f = f[:-4]
            files.append(int(f))
        files = sorted(files)
        
        for f in files:

            " Módszerek "
            
            " 1. Képeket létrehozók/módosítók "
            
            # Foltképek
            #self.stainer(f) 
            
            # Jelölt távolság pixelek
            self.find_and_mark(f)       
            
            # ... <-

            " 2. RGB képeket elemzők " 

            self.init_image(f"{self.path}{f}.png")
            self.sizes.append(self.imsize)
            
            self.distSum.append(self.distance()) # szám
            self.distPerc.append(self.percent(self.distance())) # %
            
            self.avgsR.append(self.avg_color()[0])
            self.avgsG.append(self.avg_color()[1])
            self.avgsB.append(self.avg_color()[2])
            
            # self.freq.append(self.most_freq())
            
            # ... <-
            
            self.fname.append(f) # fájlnév
            
            self.image.close()
 
        
        " Adatlisták -> oszlopok a táblázatban " 
        
        self.res_data = (

            self.fname,
            self.sizes,
            
            self.distSum,
            self.distPerc,
            self.classify(self.distPerc),
            # self.light,
            # self.classify(self.light),
            # self.dark,
            # self.classify(self.dark),
            
            self.avgsR,
            self.avgsG,
            self.avgsB,
            
            # self.freq
            
            # ... <-
            
        )
        return (self.result_table(),self.classify(self.distPerc)) 
    
        
    " KIMENET -> SZÖVEGES FÁJL "

    # Eredmények táblázat
    
    def result_table(self):
        self.mkdirIfNotExists(self.resdir)
        tabla = "%seredmenyek.txt" % self.resdir
        res = open(tabla,"a+")
        for i in range(len(self.files)+1): # +1 a fejlécnek
            for m in self.res_data:
                res.write(f"{m[i]}\t")
            res.write("\n")
        
        " Infók hozzáfűzése "

        res.write(f"\nMinta szín távolságméréshez: {self.sample}\nTávolság: {self.limit}\nDátum: {datetime.now()}\n\n")
        
        # ... <- opcionális
        
        res.close


" ------------------------------------------ KITÖLTŐ ŰRLAP ------------------------------------------ "

class FormClass(tk.Tk):

    def __init__(self):
        super().__init__()
        self.index, self.column = 0, 0
        self.label_width = 30
        self.main_color = "#ffc266"
        self.configure(background= self.main_color) #háttér
        self.hatarolo = tk.IntVar()
        self.hatarolo.set('2')
        self.geometry("700x600")
        self.resizable(height=False, width=False)

    
    " SCROLL BAR "
    """
    def scroll(self):
        scroll_bar = Scrollbar(self, orient="vertical") 
        scroll_bar.grid(
            row=0, 
            column=1,
            sticky = "NS"
        ) 
    """
    
    " FŐ CíMKE "  
 
    def main_label(self, text,pos=0):
        label = ttk.Label (
            self, 
            text=text,
            padding=(20,20), 
            width = self.label_width, 
            font=("TkDefaultFont",14),
            background="#ffff80"
        )
        label.grid(
            sticky="W",
            row=self.index-pos,
            column=self.column,
            columnspan=4,
            ipadx=600
        )
        self.index += 1


    " CíMKE "

    def param_label(self, text,pos=0):
        label = ttk.Label (
            self, 
            text=text, 
            width = self.label_width, 
            font=("TkDefaultFont",12),
            background= self.main_color
        )
        label.grid(
            padx=(0,120),
            pady=(20,10),
            row=self.index-pos,
            column=self.column,
        )
        self.index += 1
    

    " RÁDIÓGOMB "

    def radio_button(self, text,value,pos=0):
        
        style = ttk.Style(self)
        style.configure('Wild.TRadiobutton', background= self.main_color)
        
        radioButton = ttk.Radiobutton (
            self,
            style='Wild.TRadiobutton',
            text=text,
            variable=self.hatarolo,
            value = value
        )
        radioButton.grid(
            row=self.index-pos,
            column=self.column,
        )
        self.index += 1

    
    " SPINBOX "

    def spin_box(self, from_,to_,set_,pos=0):
        
        value_parcella = tk.IntVar()
        value_parcella.set(set_)

        spin = tk.Spinbox (
        self,
        from_=from_,
        to=to_,
        textvariable=value_parcella,
        #state='readonly'
        )
        spin.grid(
            pady=(20,10),
            row=self.index-pos,
            column=self.column
        )
        self.index += 1
        return value_parcella
    
    " COMBOBOX "

    def combo_box(self, values,pos=0):
        sample = tk.StringVar()
        samples = ttk.Combobox(self, textvariable=sample, width=30)
        samples["values"] = (values)
        samples["state"] = "readonly"
        samples.grid(pady=(20,10),row=self.index-pos, column=self.column)
        self.index += 1
        return samples

    
    " SUBMIT GOMB - utolsó elem! "
    
    def submit_button(self, text, submit):
        button = tk.Button(
            self,
            text=text,
            width=15,
            height=2,
            command=submit,
            font=("TkDefaultFont",10),
            fg="blue",
            background="#e6f5ff"
        )
        button.grid(
            pady=(20,30)
        )
        
        # ... <-


" ---------------------------------------- *** A PROGRAM FUTTATÁSA *** ----------------------------------------  "

def submit(): # <- gomb lenyomása után hajtja végre    
    
    # Hibakezelés

    try:
       
        kepjel = jel.get()
        parcella = parcellak.get()
        #noveny = nov.get()

        # Mappák előkészítése
        
        #os.chdir("f:\\temp_f\\pixel") # ideiglenes!
        dir = f"{os.getcwd()}"
        if os.path.exists(f"{dir}\\darabok") == False:
            os.mkdir(f"{dir}\\darabok")
        else:
            pass
        path = f"{dir}\\img\\{kepjel}.jpg"
        darabok_mappa = f"{dir}\\darabok\\{os.path.basename(path)[:-4]}\\"
        if os.path.exists(darabok_mappa) == False:
            os.mkdir(darabok_mappa)
        
        # Képek darabolása
        """
        ha nincs darabolás? ...
        """
        c = CropImage(path,darabok_mappa,parcella)
        c.CropByWidth()
        
        # Képek elemzése
        
        sample = (r.get(), g.get(), b.get()) 
        limit = tav.get()
        colorS = [((0),(151,151,151),(255,255,255),(152,251,152)), ((1),(1,1,1),(150,150,150),(0,100,0))]
        # Elemzés
        a = ImageAnalysis(kepjel,c,colorS,sample,limit)   
        results = a.exec_analysis()
        
        # Alapkép számozása-jelölése
        a.labelim(parcella,kepjel)
    
    except ZeroDivisionError:
        messagebox.showinfo("Pixel", "Nincs pixel találat!")
    
    except Exception as error:
        messagebox.showerror("Hiba", format(error))
    
    else:
        messagebox.showinfo("Info", f"A program sikeresen lefutott!\nAz eredmények és az adatok a {dir} mappában!") 


if __name__ == "__main__":

    " pos=1, ha az előző objektum mellett legyen "
    
    tc = FormClass()
    #tc.scroll()
    tc.main_label("A kép darabolása")
    tc.param_label("Növény: ")
    nov = tc.combo_box(("repce","búza","cukorrépa","cerkospóra","","egyéb"),pos=1)
    tc.param_label("Képjel: ")
    jel = tc.combo_box(("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"),pos=1)
    tc.param_label("Parcellák: ")
    parcellak = tc.spin_box(0,200,set_=50,pos=1)
    #tc.submit_button("Jelölt képekkel", submit)
    tc.main_label("Képek pixelelemzése")
    tc.param_label("Minta RGB:")
    r = tc.spin_box(0,255,set_=220,pos=1)
    g = tc.spin_box(0,255,set_=255)
    b = tc.spin_box(0,255,set_=200)
    tc.param_label("Távolság:")
    tav = tc.spin_box(0,35,set_=50,pos=1)
    tc.submit_button("Elemzés", submit)

    # ... <-

    tc.mainloop()