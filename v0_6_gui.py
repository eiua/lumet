#from Tkinter import *
import matplotlib
matplotlib.use("TkAgg")
import pygrib

import numpy as np

import time
#from matplotlib.animation import ArtistAnimation

from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cfeature

import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import metpy.plots as metplots

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from tkinter import *
#from Arpege_05_Cartes import *

from v0_6_Arome_0025_Carte_Pour_Canvas import *
from v0_6_Aro_0025_Cartes import *
from v0_6_Arome_0025_Cartes import *
from v0_6_Arpege_05_Cartes import *
from v0_6_Arpege_01_Cartes import *


class Application(Tk):

    def __init__(self):
        
        Tk.__init__(self)        # constructeur de la classe parente

        self.can = Canvas(self, width =50, height =50, bg ="white")
        self.can.pack(side =TOP, padx =5, pady =5)
        
        self.echh = 0
        self.zoomi = 0
        self.chk = 0
        self.ck = IntVar()
        Check_1 = Checkbutton(self,text = "Zoom?",variable = self.ck, command = self.regler_zoom).pack()
        Scale_1 = Scale(self,length = 200, orient = HORIZONTAL, sliderlength = 25, 
              label = "Échéance de prévision +(**)H:",from_ = 0, to = 39, tickinterval = 6, resolution = 1,
              showvalue = 1, command = self.regler_echeance_aro_0025).pack()
        
        B_1 = Button(self, text ="Température à 2m", command =self.dessiner_T2m).pack()
        B_2 = Button(self, text ="TPW850hPa + Jet au niveau Z1.5 pvu", command =self.dessiner_TPW850_Jet).pack()
        B_3 = Button(self, text ="Z1.5pvu + Jet au niveau Z1.5 pvu", command =self.dessiner_Z15pvu_Jet).pack()
        B_4 = Button(self, text ="Précipitations", command =self.dessiner_Precips).pack()
        B_5 = Button(self, text ="Rayonnement SW descendant", command =self.dessiner_DSW).pack()
        
        B_totale_1 = Button(self, text ="Charger tout 1", command =self.charger_tout_1).pack()#hop
        
        B_tout_1 = Button(self, text ="Dessiner toutes les cartes 1", command =self.dessiner_tout_1).pack()
        B_tout_2 = Button(self, text ="Dessiner toutes les cartes 2", command =self.dessiner_tout_2).pack()
        B_tout_3 = Button(self, text ="Dessiner toutes les cartes 3", command =self.dessiner_tout_3).pack()
        B_tout_4 = Button(self, text ="Dessiner toutes les cartes 4", command =self.dessiner_tout_4).pack()
        
        B_tout_5 = Button(self, text ="Dessiner Arpège 0.5°", command =self.dessiner_tout_Arp_05).pack()
        
        B_tout_6 = Button(self, text ="Dessiner Arpège 0.1°", command =self.dessiner_tout_Arp_01).pack()
        Scale_2 = Scale(self,length = 50, orient = HORIZONTAL, sliderlength = 5, 
              label = "Zoom?",from_ = 0, to = 3, tickinterval = 1, resolution = 1,
              showvalue = 1, command = self.regler_zoom_arp_01).pack()
    
    def regler_echeance_aro_0025(self,f):
        
        self.echh = int(f)
        self.event_generate('<Control-Z>')
        
    def regler_zoom_arp_01(self,f):
        
        self.zoomi = int(f)
        self.event_generate('<Control-Z>')

    def regler_zoom(self):
        
        self.chk = self.ck.get()
        self.event_generate('<Control-Z>')
            
    def dessiner_TPW850_Jet(self):
        
        self.c1 = Carte_TPW850_Jet(self,self.can,jour="10",mois="08",annee="2018",run="03",echeance=self.echh
                                         ,type_carte="TPW850_Z1.5pvu",zoom = self.chk,verification = 0)
        self.c1.envoyer_Carte_Vers_Gui()
        
    def dessiner_T2m(self):
        
        self.c2 = Carte_T2m(self,self.can,jour="10",mois="08",annee="2018",run="03",echeance=self.echh
                                         ,type_carte="T2m",zoom = self.chk,verification = 0)
        self.c2.envoyer_Carte_Vers_Gui()

    def dessiner_Z15pvu_Jet(self):

        self.c3 = Carte_Z15pvu_Jet(self,self.can,jour="10",mois="08",annee="2018",run="03",echeance=self.echh
                                         ,type_carte="Jet_Z1.5pvu",zoom = self.chk,verification = 0)
        self.c3.envoyer_Carte_Vers_Gui()
        
    def dessiner_Precips(self):
        self.c4 = Carte_Precips(self,self.can,jour="10",mois="08",annee="2018",run="03",echeance=self.echh
                                         ,type_carte="Precips",zoom = self.chk,verification = 0)
        self.c4.envoyer_Carte_Vers_Gui()        
    
    def dessiner_DSW(self):
        self.c5 = Carte_DSW(self,self.can,jour="10",mois="08",annee="2018",run="03",echeance=self.echh
                                         ,type_carte="DSW",zoom = self.chk,verification = 0)
        self.c5.envoyer_Carte_Vers_Gui()
        
    def dessiner_tout_1(self):
        self.tout_1=Arome_0025_Cartes("10","08","2018","03",zoom = 0,verification = 0)
        self.tout_1.cartes_T2m()
        
    def dessiner_tout_2(self):
        self.tout_2=Arome_0025_Cartes("10","08","2018","03",zoom = 0,verification = 0)
        self.tout_2.cartes_Jet_Z15()
        self.tout_2.cartes_DSW()
        self.tout_2.cartes_Precips()
        
    def dessiner_tout_3(self):
        self.tout_3=Arome_0025_Cartes("10","08","2018","03",zoom = 0,verification = 0)
        self.tout_3.cartes_TPW850_Z15()
        
        self.tout_3bis=Arome_0025_Cartes("10","08","2018","03",zoom = 1,verification = 0)
        self.tout_3bis.cartes_T2m()
        
    def dessiner_tout_4(self):
        self.tout_4=Arome_0025_Cartes("10","08","2018","03",zoom = 1,verification = 0)
        self.tout_4.cartes_DSW()
        self.tout_4.cartes_Precips()

        self.tout_4.histogramme_DSW()
        self.tout_4.histogramme_Precips()
        self.tout_4.histogramme_T2m()
        self.tout_4.histogramme_Vent10m()
        
    def dessiner_tout_Arp_05(self):
        self.tout_5=Arpege_05_Cartes("10","08","2018","00",zoom = 0,verification = 0)
        self.tout_5.cartes_T2m()
        self.tout_5.cartes_DSW()
        self.tout_5.cartes_Precips()
        
    def dessiner_tout_Arp_01(self):
        self.tout_6=Arpege_01_Cartes("10","08","2018","00",zoom = self.zoomi,verification = 0)
        self.tout_6.cartes_Pmer()
        self.tout_6.cartes_T2m()
        self.tout_6.cartes_DSW()
        self.tout_6.cartes_Precips()
        if self.zoomi == 3:
            self.tout_6.histogramme_T2m()
            self.tout_6.histogramme_Vent10m()
            self.tout_6.histogramme_Precips()
