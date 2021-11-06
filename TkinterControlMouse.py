from PIL import Image
from scipy import *
import numpy
import pyautogui, sys
import keyboard
import os
import math as math
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk
from sys import exit


Precision = 1
Progression = 0

Width = 600
Height = 600


fenetre = Tk()
fenetre.resizable(False, False)
fenetre.title("Dessiner")
canvas = Canvas(fenetre, width=Width, height=Height, bg="#ffffff")
canvas.pack(side = "right")

ELargeur = StringVar(fenetre)
ELargeur.set("Default")

filename = None
oldfilename = None
Final = False
MessageErreur = StringVar()
MessageErreur.set("")
EPrecision = DoubleVar()
ENoir = StringVar()
ETolerance = StringVar()
ESmooting = StringVar()
EPrecision.set(1)
ENoir.set(0)
ButtDessin = 0

if os.path.isfile("Imageaimprimer.png"):os.remove("Imageaimprimer.png")
if os.path.isfile("Imageaafficher.png"):os.remove("Imageaafficher.png")


def binarize_image(img_path, target_path, threshold, Noir, Size,prec):
    image_file = Image.open(img_path)
    image_file = image_file.resize((int(image_file.size[0]*prec),int(image_file.size[1]*prec)))
    image = image_file.convert('L')  # convert image to monochrome
    image = numpy.array(image)
    image = binarize_array(image, threshold, Noir)
    im = Image.fromarray(image)
    im.save(target_path)
    #imsave(target_path, image)
    return image


def binarize_array(numpy_array, threshold, Noir):
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] > threshold:
                numpy_array[i][j] = Noir*255
            else:
                numpy_array[i][j] = 255*(1-Noir)
    return numpy_array
    
def Strategielignes(Array,precision,deg,smoothing):
    L = []
    d = 0 
    Ligne = False
    for x in range(0,len(Array)):
        for y in range(0,len(Array[0])):
            if Array[x][y] == 0 and Ligne == False:
                pos = (x,y)
                d += 1
                Ligne = True
            elif Array[x][y] == 0 and Ligne == True:
                d += 1
            if Ligne == True and ((Array[x][y] == 255) or (y == len(Array[0])-1)):
                if d>smoothing: L.append((pos, d))
                d = 0
                Ligne = False
                
    C = []
    d2 = 0 
    Colonne = False
    for y in range(0,len(Array[0])):
        for x in range(0,len(Array)):
            if Array[x][y] == 0 and Colonne == False:
                pos = (x,y)
                d2 += 1
                Colonne = True
            elif Array[x][y] == 0 and Colonne == True:
                d2 += 1
            if Colonne == True and ((Array[x][y] == 255) or (x == len(Array)-1)):
                if d2>smoothing: C.append((pos, d2))
                d2 = 0
                Colonne = False
    #return L,1
    print(len(L),len(C))
    if len(L) <= len(C):
        return L,1
    else:
        return C,2
    
def Dessiner(LL,strategie,prec,ratio,Pos_Souris,Mx,My):
    if strategie == 1:
        for i in range(0,len(LL)):
            if keyboard.is_pressed('shift + p'):
                popupmsg("Le programme continura à la position de pause","","Pour arrêter le programme appuyez sur: Shift + s","Pour mettre en pause le programme appuyez sur: Shift + p","Temps estimé (restant): " + str(round((len(LL)-i)*(106/523))) + " sec")
                keyboard.wait('shift + p')
            pyautogui.moveTo(Pos_Souris[0]+round((LL[i][0][1]/prec)*ratio)-Mx,Pos_Souris[1]+round((LL[i][0][0]/prec)*ratio)-My)
            pyautogui.drag(round((LL[i][1]/prec)*ratio), 0, button='left')
            if keyboard.is_pressed('S'):
                exit()
    elif strategie == 2:
        for i in range(0,len(LL)):
            if keyboard.is_pressed('shift + p'):
                popupmsg("Le programme continura à la position de pause","","Pour arrêter le programme appuyez sur: Shift + s","Pour mettre en pause le programme appuyez sur: Shift + p","Temps estimé (restant): " + str(round((len(LL)-i)*(106/523))) + " sec")
                keyboard.wait('shift + p')
            pyautogui.moveTo(Pos_Souris[0]+round((LL[i][0][1]/prec)*ratio)-Mx,Pos_Souris[1]+round((LL[i][0][0]/prec)*ratio)-My)
            pyautogui.drag(0,round((LL[i][1]/prec)*ratio), button='left') 
            if keyboard.is_pressed('S'):
                exit()


def LancerDessin():
    global Final
    global fenetre
    global Pos_Souris
    Final = True
    Parametres = Actualiser()
    Dessin, strat = Strategielignes(Parametres[0],Parametres[2],Parametres[1],Parametres[3])
    My, Mx = plus_petite_valeur(Dessin)
    Temps_estime = len(Dessin)*(106/523)
    fenetre.destroy()
    popupmsg("Le programme débutera à la position de la souris"," Pour exécuter le programme apuyer sur: Shift + b","Pour arrêter le programme appuyez sur: Shift + s","Pour mettre en pause le programme appuyez sur: Shift + p","Temps estimé: " + str(round(len(Dessin)*(106/523))) + " sec")
    keyboard.wait('shift + b')
    os.remove("Imageaimprimer.png")    
    Pos_Souris = pyautogui.position()    
    Dessiner(Dessin,strat,Parametres[2],Parametres[3],Pos_Souris,My,Mx)

    
def popupmsg(msg1,msg2,msg3,msg4,msg5):
    popup = Tk()
    popup.wm_title("!")
    Label(popup, text=msg1, foreground = "#000000").pack(side="top", fill="x", pady=5)
    Label(popup, text=msg2, foreground = "#ff0000").pack(side="top", fill="x", pady=0)
    Label(popup, text=msg3, foreground = "#ff0000").pack(side="top", fill="x", pady=0)
    Label(popup, text=msg4, foreground = "#ff0000").pack(side="top", fill="x", pady=0)
    Label(popup, text=msg5, foreground = "#000000").pack(side="top", fill="x", pady=5)
    B1 = Button(popup, text="Okay", command = popup.destroy).pack(side = "left", padx = 10, pady = 10)
    B2 = Button(popup, text="Quit", command = exit).pack(side = "right", padx = 10, pady = 10)
    popup.mainloop()
    

def plus_petite_valeur(L):
    mx = L[0][0][0]
    my = L[0][0][1]
    for i in range(0,len(L)):
        if L[i][0][0] < mx:
            mx = L[i][0][0]
            
    for i in range(0,len(L)):
        if L[i][0][1] < my:
            my = L[i][0][1]
            
    return mx, my
    
def Actualiser():
    global Final
    print("act")
    if filename == None:
        MessageErreur.set("Vous devez ouvrir un fichier")
        return
    if filename != oldfilename:
        img = Image.open(str(filename))
    Tolerance = int(ETolerance.get())
    Noir = int(ENoir.get())
    Precision = EPrecision.get()
    Smooting = ESmooting.get()
    if ELargeur.get() == "Default":
        Largeur = img.size[0]
    else:
        Largeur = int(ELargeur.get())
    Taille = (Largeur, int(img.size[1]*(Largeur/img.size[0])))
    Ratio = Largeur/img.size[0]
    if os.path.isfile("Imageaimprimer.png"):os.remove("Imageaimprimer.png")
    Aprint = binarize_image(str(filename), "Imageaimprimer.png", Tolerance, Noir, Taille, Precision)
    imag = Image.open("Imageaimprimer.png")  # PIL solution
    if img.size[0] > img.size[1]:
        imag = imag.resize((Width, int(Width/(img.size[0]/img.size[1]))))
        canvas.config(width=Width, height=int(Width/(img.size[0]/img.size[1])))
    else:
        imag = imag.resize((int(Height*(img.size[0]/img.size[1])), Height))
        canvas.config(width=int(Height*(img.size[0]/img.size[1])), height=Height)
    #imsave("Imageaafficher.png", imag)
    imag.save("Imageaafficher.png")
    one = PhotoImage(file=r'Imageaafficher.png')
    fenetre.one = one
    canvas.create_image((0,0), image=one, anchor='nw')
    if Final == True:
        return Aprint, Noir, Precision, Ratio,Smooting



def Ouvrir_Fichier():
    global filename
    global oldfilename
    oldfilename = filename
    filename = filedialog.askopenfilename(filetypes = (("PNG,JPG Files","*.png;*.jpg"),("All Files","*.*")))
    MessageErreur.set("")
    Actualiser()
    
    
##Entrees
Label(fenetre, text = "Largeur de l'image:").pack(side = "top")
Entry(fenetre, width = 10, textvariable = ELargeur).pack(side = "top")
Label(fenetre, text = "Precision:").pack(side = "top")
Entry(fenetre, width = 10, textvariable = EPrecision).pack(side = "top")
Label(fenetre, text = "Inversion Noir:").pack(side = "top")
Checkbutton(fenetre,onvalue = "0", offvalue = "1", variable = ENoir).pack(side = "top")
Label(fenetre, text = "Tolérance:").pack(side = "top")
Scale(fenetre, from_=0, to=255, orient=HORIZONTAL, length = 150, variable = ETolerance).pack(side = "top")
Label(fenetre, text = "Smooting:").pack(side = "top")
Scale(fenetre, from_=0, to=5, orient=HORIZONTAL, length = 150, variable = ESmooting).pack(side = "top")

    
##Buttons


Button(fenetre, text = "Ouvrir", command = Ouvrir_Fichier).pack(side = "top",pady = 10)  
Button(fenetre, text = "Actualiser", command = Actualiser).pack(side = "top",pady = 10)  
Button(fenetre, text = "Lancer le dessin", command = LancerDessin).pack(side = "top",pady = 10)  
Label(fenetre, textvariable = MessageErreur, foreground = "#ff0000").pack(side = "top")
MessageErreur.set("")


##




fenetre.mainloop()
if os.path.isfile("Imageaimprimer.png"):os.remove("Imageaimprimer.png")
if os.path.isfile("Imageaafficher.png"):os.remove("Imageaafficher.png")