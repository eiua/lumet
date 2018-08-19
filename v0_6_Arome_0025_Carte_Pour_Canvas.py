# classes et méthode pour afficher une seule carte à une échéance et à un zoom donné
# le tout dans une fenêtre de lumet.
# Ceci est du code Python3

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

class Arome_0025_Carte_Pour_Canvas(Frame):
    """Exploiter les fichiers Arome 0.025°, dessin de cartes usuelles en météo.
    """
#self,jour,mois,annee,run,type_carte,zoom
    def __init__(self,jour,mois,annee,run,echeance,type_carte,zoom):
        
        Frame.__init__(self)
        
        self.jour = jour
        self.mois = mois
        self.annee = annee
        self.run = run
        self.zoom = zoom
        
        self.echeance = echeance
        
        self.type_de_carte = type_carte
        
        self.nom_fichier_1 = ""
        self.nom_fichier_2 = ""
        self.titre_0 = ""
        self.titre_10 = ""
        self.nom_0 = ""
        self.nom_10 = ""
        
    def construire_Noms(self):
        """Renvoie les différentes chaines de caractères qui serviront de titre,
        nom de fichier à ouvrir et de figure à sauvegarder."""

        if self.type_de_carte == "T2m":

            SP1_IP5 = "SP1"
            titre_00 = 'T2m (°C)'

            if self.zoom == 0:
                nom_00 = '/T2m'
            elif self.zoom == 1:
                nom_00 = '/T2m_zoom'
        
        elif self.type_de_carte == "histo_T2m":
            
            SP1_IP5 = "SP1"
            titre_00 = 'Diagramme T2m (°c)'
            nom_00 = '/histo_T2m'

        elif self.type_de_carte == "histo_Vent10m":
            
            SP1_IP5 = "SP1"
            titre_00 = 'Diagramme Vent à 10m (m/s)'
            nom_00 = '/histo_Vent10m'

        elif self.type_de_carte == "TPW850_Z1.5pvu":
            
            SP1_IP5 = "IP5"
            titre_00 = 'TPW 850hPa et Z1.5pvu'
            nom_00 = '/Z15_pvu_TPW850'

        elif self.type_de_carte == "Jet_Z1.5pvu":
            
            SP1_IP5 = "IP5"
            titre_00 = 'Jet stream et Z1.5pvu'
            nom_00 = '/Z15_pvu_Jet'

        elif self.type_de_carte == "Precips":

            SP1_IP5 = "SP1"
            titre_00 = 'Lame horaire (mm)'

            if self.zoom == 0:
                nom_00 = '/Precips'
            elif self.zoom == 1:
                nom_00 = '/Precips_zoom'

        elif self.type_de_carte == "histo_Precips":
            
            SP1_IP5 = "SP1"
            titre_00 = 'Diagramme lame d\'eau (mm)'
            nom_00 = '/histo_precips'

        elif self.type_de_carte == "DSW":
            
            SP1_IP5 = "SP1"
            titre_00 = 'Down SW (Kw(h)/m2)'
                        
            if self.zoom == 0:
                nom_00 = '/DSW'
            elif self.zoom == 1:
                nom_00 = '/DSW_zoom'
                
        elif self.type_de_carte == "histo_DSW":
            
            SP1_IP5 = "SP1"
            titre_00 = 'Diagramme DSW (Wh/m2)'
            nom_00 = '/histo_DSW'
        
        
        self.nom_fichier_1 = "./Aro_00025/"+ self.jour + self.mois + self.annee + "/AROME_0.025_" + SP1_IP5 +"_"
        self.nom_fichier_2 = "H_" + self.annee + self.mois + self.jour + self.run + "00.grib2"
        
        self.titre_0 = titre_00 + ' Aro 0.025° run ' + self.run + 'h ' + self.jour +'/'+self.mois+'/'+self.annee +'0'
        self.titre_10 = titre_00 + ' Aro 0.025° run ' + self.run + 'h ' + self.jour +'/'+self.mois+'/'+self.annee
        
        self.nom_0 = './Aro_00025/' + self.jour + self.mois + self.annee + nom_00 + '_Aro_0025_' + self.jour + self.mois + self.annee + self.run + '_0'
        self.nom_10 = './Aro_00025/' + self.jour + self.mois + self.annee + nom_00 + '_Aro_0025_' + self.jour + self.mois + self.annee + self.run + '_'
        
    def trouver_indice_echeance(self):
        """
        Méthode qui ouvre le bon fichier au bon indice à partir d'une valeur d'échéance.
        
        Renvoie un fichier ouvert via pygrib et un indice d'échéance (deux de chaque dans le cas de champs à cumul comme les précips et le DSW).
        
        Les fichiers bruts sont organisés par échéances, de +00h à +6h, soit 7 échéances, pour le premier fichier grib2.
        Ensuite chaque fichier contient 6 échéances comme suit : +7h à +12h.
        
        Pour accéder au données à la bonne échéance, il faut donc:
        1 charger le bon fichier
        2 trouver l'indice dans ce fichier qui correspond à notre échéances donnée.
        
        On traduit donc: je veux l'échéance +15h
        par: voici dans le fichier 13-18h.grib2, ce sera l'indice numéro 3.   
        """
        
        if self.type_de_carte == "DSW" or self.type_de_carte == "Precips":
            
            if self.echeance <= 5 :
                indice_echeance_2 = self.echeance
            elif (self.echeance > 5) and (self.echeance <= 11):
                indice_echeance_2 = (self.echeance % 6)
            elif (self.echeance > 11) and (self.echeance <= 17):
                indice_echeance_2 = (self.echeance % 6)
            elif (self.echeance > 17) and (self.echeance <= 23):
                indice_echeance_2 = (self.echeance % 6)
            elif (self.echeance > 23) and (self.echeance <= 29):
                indice_echeance_2 = (self.echeance % 6)
            elif (self.echeance > 29) and (self.echeance <= 35):
                indice_echeance_2 = (self.echeance % 6)
            elif (self.echeance > 35) and (self.echeance <= 41):
                indice_echeance_2 = (self.echeance % 6)

            if self.echeance <= 5:
                t_fichier = 6
                nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
                grbs_2 = pygrib.open(nom_fichier)
            elif self.echeance > 5:
                t_fichier = (int(self.echeance/6) +1 ) * 6
                nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
                grbs_2 = pygrib.open(nom_fichier)

            if self.echeance > 0:
                #cheche = 0
                cheche = self.echeance - 1

                if cheche <= 5 :
                    indice_echeance_1 = cheche
                elif (cheche > 5) and (cheche <= 11):
                    indice_echeance_1 = (cheche % 6)
                elif (cheche > 11) and (cheche <= 17):
                    indice_echeance_1 = (cheche % 6)
                elif (cheche > 17) and (cheche <= 23):
                    indice_echeance_1 = (cheche % 6)
                elif (cheche > 23) and (cheche <= 29):
                    indice_echeance_1 = (cheche % 6)
                elif (cheche > 29) and (cheche <= 35):
                    indice_echeance_1 = (cheche % 6)
                elif (cheche > 35) and (cheche <= 41):
                    indice_echeance_1 = (cheche % 6)        

                if cheche <= 5:
                    t_fichier = 6
                    nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
                    grbs_1 = pygrib.open(nom_fichier)
                elif cheche > 5:
                    t_fichier = (int(cheche/6) +1 ) * 6
                    nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
                    grbs_1 = pygrib.open(nom_fichier)       
        
        else:
            
            if self.echeance <= 6 :
                indice_echeance_2 = self.echeance
                t_fichier = 6
                nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
                grbs_2 = pygrib.open(nom_fichier)
            elif (self.echeance > 6) and (self.echeance <= 12):
                indice_echeance_2 = ((self.echeance - 1) % 6)
                t_fichier = 12
                nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
                grbs_2 = pygrib.open(nom_fichier)
            elif (self.echeance > 12) and (self.echeance <= 18):
                indice_echeance_2 = ((self.echeance - 1) % 6)
                t_fichier = 18
                nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
                grbs_2 = pygrib.open(nom_fichier)
            elif (self.echeance > 18) and (self.echeance <= 24):
                indice_echeance_2 = ((self.echeance - 1) % 6)
                t_fichier = 24
                nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
                grbs_2 = pygrib.open(nom_fichier)
            elif (self.echeance > 24) and (self.echeance <= 30):
                indice_echeance_2 = ((self.echeance - 1) % 6)
                t_fichier = 30
                nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
                grbs_2 = pygrib.open(nom_fichier)
            elif (self.echeance > 30) and (self.echeance <= 36):
                indice_echeance_2 = ((self.echeance - 1) % 6)
                t_fichier = 36
                nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
                grbs_2 = pygrib.open(nom_fichier)
            elif (self.echeance > 36) and (self.echeance <= 42):
                indice_echeance_2 = ((self.echeance - 1) % 6)
                t_fichier = 42
                nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
                grbs_2 = pygrib.open(nom_fichier)

            #if self.echeance <=6 :
             #   t_fichier = 6
              #  nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
               # grbs_2 = pygrib.open(nom_fichier)
            #elif self.echeance > 6:
             #   t_fichier = (int(self.echeance/6) +1 ) * 6
              #  nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
               # grbs_2 = pygrib.open(nom_fichier)  
        
        if self.type_de_carte == "DSW" or self.type_de_carte == "Precips":
            
            return indice_echeance_1,indice_echeance_2,grbs_1,grbs_2
        
        else:
            
            return indice_echeance_2,grbs_2

    def dessiner_fond_carte(self,lons,lats):
        """
        Renvoie un fond de carte géographique sur lequel on tracera le ou les champs météo.
        """
        lon_0 = lons.mean()
        lat_0 = lats.mean()
        
        proj = ccrs.Stereographic(central_longitude=lon_0,central_latitude=lat_0)
            
        f = Figure(figsize=(10,10), dpi=300)
        ax = f.add_subplot(111)
        
        ax = plt.axes(projection=proj)

        #ax.set_extent([lons.min(), lons.max(), lats.min()-0.5, lats.max()])

        #ax.add_feature(cfeature.BORDERS)

        pays = cfeature.NaturalEarthFeature(category='cultural',name='admin_0_countries',
                                           scale='10m',facecolor='none')
        ax.add_feature(pays,edgecolor='black',linewidth=(0.7))

        fleuves = cfeature.NaturalEarthFeature(category='physical',name='rivers_lake_centerlines',
                                           scale='10m',facecolor='none')
        ax.add_feature(fleuves,edgecolor='blue',linewidth=(0.3))
        rivieres = cfeature.NaturalEarthFeature(category='physical',name='rivers_europe',
                                           scale='10m',facecolor='none')
        ax.add_feature(rivieres,edgecolor='blue',linewidth=(0.3))

        if self.zoom == 1:
            ax.set_extent([lons.min(), lons.max(), lats.min(), lats.max()])
        else:
            ax.set_extent([lons.min(), lons.max(), lats.min()-0.5, lats.max()])
            
        return f,ax

class Carte_DSW(Arome_0025_Carte_Pour_Canvas):
    """Renvoie la carte de rayonnement SW descendant (KW/m2/h) prévue par Arome 0.025°."""
    def __init__(self,boss,canev,jour,mois,annee,run,echeance,type_carte,zoom,verification):
        
        Arome_0025_Carte_Pour_Canvas.__init__(self,jour,mois,annee,run,echeance,type_carte,zoom)
        #self,jour,mois,annee,run,type_carte,zoom
        Frame.__init__(self)
        
        self.verification = verification
        self.canev=canev
        #self.echeance = echeance
        
    def envoyer_Carte_Vers_Gui(self):
        
        self.construire_Noms()
        #indice_echeance_1,indice_echeance_2,grbs_1,grbs_2 = 0,0,0,0
        indice_echeance_1,indice_echeance_2,grbs_1,grbs_2 = self.trouver_indice_echeance()
        cheche = self.echeance - 1
        #del(cheche)
        
        if self.echeance > 0:
            print("Échéance: ",self.echeance)
            print("cheche: ",cheche)
            print("indice échéance 1: ",indice_echeance_1)
            print("indice échéance 2: ",indice_echeance_2)
            gt_1 = grbs_1.select(shortName = 'dswrf')[indice_echeance_1]
            print("gt_1: ",gt_1)
        else:
            print("indice échéance 2: ",indice_echeance_2)
            print("Échéance: ",self.echeance)
            
        gt_2 = grbs_2.select(shortName = 'dswrf')[indice_echeance_2]
                
        #print("gt_1: ",gt_1)
        print("gt_2: ",gt_2)
            
        ech_Mois = str(gt_2.validityDate)[4:6]
        ech_Jour = str(gt_2.validityDate)[6:8]

        if gt_2.validityTime<1000:
            ech_Heure = str(gt_2.validityTime)[0]
        else:
            ech_Heure = str(gt_2.validityTime)[0:2]

        print("Champ: ", gt_2.shortName, "    Validité: ", gt_2.validityDate, " à ",gt_2.validityTime)

        validite ="Prévision pour le " + ech_Jour + "/" + ech_Mois+ " " + ech_Heure + "H"

        if self.echeance == 0:
            if self.zoom == 0:
                tt2, lats, lons = gt_2.data()#(lat1=43,lat2=47,lon1=2.25,lon2=7.5)
                grbs_2.close()
            elif self.zoom == 1:
                tt2, lats, lons = gt_2.data(lat1=43,lat2=47,lon1=2.25,lon2=7.5)
                grbs_2.close()

            tt1 = 0

        else:
            if self.zoom == 0:
                tt1, lats, lons = gt_1.data()#(lat1=43,lat2=47,lon1=2.25,lon2=7.5)
                tt2, lats, lons = gt_2.data()
                grbs_1.close()
                grbs_2.close()
            elif self.zoom == 1:
                tt1, lats, lons = gt_1.data(lat1=43,lat2=47,lon1=2.25,lon2=7.5)
                tt2, lats, lons = gt_2.data(lat1=43,lat2=47,lon1=2.25,lon2=7.5)
                grbs_1.close()
                grbs_2.close()

        if self.echeance > 0:
            del(gt_1)
        del(gt_2)

        tete = tt2 - tt1
        
        del(tt1)
        del(tt2)

        tt = (tete/1000)
        del(tete)
        tt = tt.astype(int)
        
        f,ax = self.dessiner_fond_carte(lons,lats)

        #origin='lower'
        #levels = np.arange(1,int(tt.max()),1)
        #levels_contour = np.arange(1,int(tt.max()),2)
        #levels = np.arange(0,4000,50)
        #levels_contour = np.arange(0,4000,50)

        cs=ax.pcolormesh(lons, lats, tt,vmin=0.01,vmax=4000, cmap='jet',transform=ccrs.PlateCarree())

        csb = plt.colorbar(cs)
        csb.set_label("kW/m2/h")

        if self.echeance < 10:
            titre = self.titre_0 + "\n" + validite
            nom = self.nom_0 + str(self.echeance)+'H.png'
        else:
            titre = self.titre_10 + "\n" + validite
            nom = self.nom_10 + str(self.echeance)+'H.png'

        if self.verification == 1:
            print(titre)
            print(nom)
        plt.title(titre)
        #plt.savefig(nom,dpi=300)
        
        plt.show()
        plt.close()
        
        self.canev = FigureCanvasTkAgg(f, self.master)
        self.canev.show()
        self.canev.get_tk_widget().pack(expand=True)
        
        toolbar = NavigationToolbar2TkAgg(self.canev, self.master)
        toolbar.update()
        self.canev._tkcanvas.pack(expand=True)
        
        del(tt)
        del(titre)
        del(nom)
        
        print("coucou")
        
class Carte_Precips(Arome_0025_Carte_Pour_Canvas):
    """Renvoie la carte de lame d'eau horaire (mm) prévue par Arome 0.025°."""

    def __init__(self,boss,canev,jour,mois,annee,run,echeance,type_carte,zoom,verification):
        
        Arome_0025_Carte_Pour_Canvas.__init__(self,jour,mois,annee,run,echeance,type_carte,zoom)
        #self,jour,mois,annee,run,type_carte,zoom
        Frame.__init__(self)
        
        self.verification = verification
        self.canev=canev
        self.echeance = echeance
        
    def envoyer_Carte_Vers_Gui(self):
        
        self.construire_Noms()
        
        indice_echeance_1,indice_echeance_2,grbs_1,grbs_2 = self.trouver_indice_echeance()
        cheche = self.echeance - 1
        #del(cheche)
        
        if self.echeance > 0:
            print("Échéance: ",self.echeance)
            print("cheche: ",cheche)
            print("indice échéance 1: ",indice_echeance_1)
            print("indice échéance 2: ",indice_echeance_2)
            gt_1 = grbs_1.select(shortName = 'tp')[indice_echeance_1]
            print("gt_1: ",gt_1)
        else:
            print("indice échéance 2: ",indice_echeance_2)
            print("Échéance: ",self.echeance)
            
        gt_2 = grbs_2.select(shortName = 'tp')[indice_echeance_2]
                
        ech_Mois = str(gt_2.validityDate)[4:6]
        ech_Jour = str(gt_2.validityDate)[6:8]

        if gt_2.validityTime<1000:
            ech_Heure = str(gt_2.validityTime)[0]
        else:
            ech_Heure = str(gt_2.validityTime)[0:2]

        print("Champ: ", gt_2.shortName, "    Validité: ", gt_2.validityDate, " à ",gt_2.validityTime)

        validite ="Prévision pour le " + ech_Jour + "/" + ech_Mois+ " " + ech_Heure + "H"

        if self.verification == 1:
            print(gt_1)
            print(gt_2)

        if self.echeance == 0:
            if self.zoom == 0:
                tt2, lats, lons = gt_2.data()#(lat1=43,lat2=47,lon1=2.25,lon2=7.5)
                grbs_2.close()
            elif self.zoom == 1:
                tt2, lats, lons = gt_2.data(lat1=43,lat2=47,lon1=2.25,lon2=7.5)
                grbs_2.close()

            tt1 = 0

        else:
            if self.zoom == 0:
                tt1, lats, lons = gt_1.data()#(lat1=43,lat2=47,lon1=2.25,lon2=7.5)
                tt2, lats, lons = gt_2.data()
                grbs_1.close()
                grbs_2.close()
            elif self.zoom == 1:
                tt1, lats, lons = gt_1.data(lat1=43,lat2=47,lon1=2.25,lon2=7.5)
                tt2, lats, lons = gt_2.data(lat1=43,lat2=47,lon1=2.25,lon2=7.5)
                grbs_1.close()
                grbs_2.close()

        if self.echeance > 0:
            del(gt_1)
        del(gt_2)

        tete = tt2 - tt1
        
        del(tt1)
        del(tt2)
        
        tt = np.ma.masked_less(tete, 0.1)

        del(tete)
        
        f,ax = self.dessiner_fond_carte(lons,lats)

        origin='lower'
        #levels = np.arange(round(tt.min()),round(tt.max()),1)
        #levels_contour = np.arange(round(tt.min()),round(tt.max()),2)

        nws_precip_colors = [
        "#04e9e7",  # 0.001 - 0.2 mm
        "#019ff4",  # 0.2 - 0.4 mm
        "#0300f4",  # 0.4 - 0.6 mm
        "#02fd02",  # 0.6 - 0.8 mm
        "#01c501",  # 0.8 - 1.00 mm
        "#008e00",  # 1.00 - 1.50 mm
        "#fdf802",  # 1.50 - 2.00 mm
        "#e5bc00",  # 2.00 - 2.50 mm
        "#fd9500",  # 2.50 - 3.00 mm
        "#fd0000",  # 3.00 - 4.00 mm
        "#d40000",  # 4.00 - 5.00 mm
        "#bc0000",  # 5.00 - 6.00 mm
        "#f800fd",  # 6.00 - 8.00 mm
        "#9854c6",  # 8.00 - 10.00 mm
        "#fdfdfd"   # 10.00+
        ]
        precip_colormap = mcolors.ListedColormap(nws_precip_colors)

        levels = [0.1, 0.2, 0.5, 1, 2, 3, 5, 7.5, 10, 20, 30, 50,
        60, 80, 100, 200]
        norm = mcolors.BoundaryNorm(levels, 15)

        #levels = np.arange(0.05,50,2)
        #levels_contour = np.arange(0.05,50,2)

        cs=plt.pcolormesh(lons, lats, tt, norm=norm, cmap=precip_colormap,transform=ccrs.PlateCarree())

        csb = plt.colorbar(cs)
        csb.set_label("mm")

        if self.echeance < 10:
            titre = self.titre_0 + "\n" + validite
            nom = self.nom_0 + str(self.echeance)+'H.png'
        else:
            titre = self.titre_10 + "\n" + validite
            nom = self.nom_10 + str(self.echeance)+'H.png'

        if self.verification == 1:
            print(titre)
            print(nom)

        plt.title(titre)
        #plt.savefig(nom,dpi=300)
        
        plt.show()
        plt.close()
        
        self.canev = FigureCanvasTkAgg(f, self.master)
        self.canev.show()
        self.canev.get_tk_widget().pack(expand=True)
        
        toolbar = NavigationToolbar2TkAgg(self.canev, self.master)
        toolbar.update()
        self.canev._tkcanvas.pack(expand=True)
        
        del(tt)
        del(titre)
        del(nom)
        
        print("coucou")
        
class Carte_Z15pvu_Jet(Arome_0025_Carte_Pour_Canvas):
    """Renvoie la carte du géopotentiel au niveau Z1.5pvu associée à la température potentielle 
        pseudo-adiabatique au niveau 850hPa (TPw850hPa)  prévue par Arome 0.025°.
        Le niveau Z1.5pvu correspond à la tropopause.
        Permet de regarder le forçage d'altitude (Z1.5pvu) et l'énergie disponible 
        dans les basses couches (TPw850hPa)."""
    
    def __init__(self,boss,canev,jour,mois,annee,run,echeance,type_carte,zoom,verification):
        
        Arome_0025_Carte_Pour_Canvas.__init__(self,jour,mois,annee,run,echeance,type_carte,zoom)
        
        Frame.__init__(self)
        
        self.verification = verification
        self.canev=canev
        #self.echeance = echeance
        
    def envoyer_Carte_Vers_Gui(self):
        
        self.construire_Noms()
        
        indice_echeance,grbs = self.trouver_indice_echeance()
        
        gt_U = grbs.select(shortName='u',level=1500000000)[indice_echeance]
        gt_V = grbs.select(shortName='v',level=1500000000)[indice_echeance]
        gt_pvu = grbs.select(shortName='z',level=1500000000)[indice_echeance]

        if self.verification == 1:
            print(gt_U.shortName,gt_V.shortName,gt_pvu.shortName,gt_U.level,gt_pvu.level)

        if self.verification == 1:
            print(gt_U)
            print(gt_V)
            print(str(gt_U.validityDate)[0:4])

        ech_Mois = str(gt_U.validityDate)[4:6]
        ech_Jour = str(gt_U.validityDate)[6:8]

        if gt_U.validityTime<1000:
            ech_Heure = str(gt_U.validityTime)[0]
        else:
            ech_Heure = str(gt_U.validityTime)[0:2]

        if self.verification == 1:
            print(ech_Mois,ech_Jour,ech_Heure)
            print("écheance:",echeance)

        print("gt_U:",gt_U.validityDate,gt_U.validityTime,"   gt_V:",gt_V.validityDate,gt_V.validityTime,"   gt_pvu:",gt_pvu.validityDate,gt_pvu.validityTime)
        validite ="Prévision pour le " + ech_Jour + "/" + ech_Mois+ " " + ech_Heure + "H"

        vent_Zonal = np.array(gt_U.values)
        vent_Meri = np.array(gt_V.values)

        #print(type(vent_Zonal))

        pvu=gt_pvu.values

        lats,lons=gt_U.latlons()

        del(gt_U)
        del(gt_V)
        del(gt_pvu)
        
        grbs.close()
        
        tt = (vent_Zonal*vent_Zonal + vent_Meri*vent_Meri)**(1/2)
        del(vent_Zonal)
        del(vent_Meri)
        #tt = tt.astype(int)
        Zm = np.ma.array(tt)
        Zm = Zm.astype(int)
        Zm[Zm < 20] = np.ma.masked
        #print(Zm)

        if self.verification == 1:
            len(lons)
            len(lats)

        pvu = (pvu/10)
        pvu =  pvu.astype(int)

        if self.echeance < 10:
            titre = self.titre_0 + "\n" + validite# + str(compteur)+'H'
            nom = self.nom_0 + str(self.echeance)+'H.png'
        else:
            titre = self.titre_10 + "\n" + validite#str(compteur)+'H'
            nom = self.nom_10 + str(self.echeance)+'H.png'

        if self.verification == 1:
            print(titre)
            print(nom)

        f,ax = self.dessiner_fond_carte(lons,lats)
        
        levels = np.arange(20,80,2.5)
        levels_pvu = np.arange(0,12000,1000)

        #bb=ax.contourf(lons, lats, tt, levels,cmap='jet',transform=ccrs.PlateCarree())
        #Zm = np.ma.array(tt)
        #Zm[Zm < 20] = np.ma.masked
        #print(Zm)
        bb = ax.pcolormesh(lons, lats, Zm, vmin=20,vmax=80, cmap='jet',transform=ccrs.PlateCarree())
        if self.verification == 1:
            print("fin pcocolmesh")
        cc = ax.contour(lons, lats, pvu, levels_pvu,transform=ccrs.PlateCarree(),
                      colors=('k'),
                      linewidths=(0.5),
                      origin='lower')
        if self.verification == 1:
            print("fin contour")
        csb = plt.colorbar(bb)
        csb.set_label("Module du jet (m/s)")

        #csb.set_label("Module du Jet (m/s)")
        #ax.barbs(lons,lats, vent_Zonal, vent_Meri, regrid_shape=18,
        #         linewidth=(0.3),transform=ccrs.PlateCarree(),length=5)

        #, regrid_shape=18

        if self.verification == 1:
            print("fin barbs")

        lala_pvu = plt.clabel(cc, fontsize=4, fmt='%1.0f')

        plt.title(titre)
        #plt.savefig(nom,dpi=300)
        
        plt.show()
        plt.close()
        
        self.canev = FigureCanvasTkAgg(f, self.master)
        self.canev.show()
        self.canev.get_tk_widget().pack(expand=True)
        
        toolbar = NavigationToolbar2TkAgg(self.canev, self.master)
        toolbar.update()
        self.canev._tkcanvas.pack(expand=True)
        
        #plt.close()
        del(pvu)
        del(Zm)
        del(tt)
        del(titre)
        del(nom)
        
        print("coucou")
        
class Carte_TPW850_Jet(Arome_0025_Carte_Pour_Canvas):
    """Renvoie la carte du géopotentiel au niveau Z1.5pvu associée à la température potentielle 
        pseudo-adiabatique au niveau 850hPa (TPw850hPa)  prévue par Arome 0.025°.
        Le niveau Z1.5pvu correspond à la tropopause.
        Permet de regarder le forçage d'altitude (Z1.5pvu) et l'énergie disponible 
        dans les basses couches (TPw850hPa)."""
    
    def __init__(self,boss,canev,jour,mois,annee,run,echeance,type_carte,zoom,verification):
        
        Arome_0025_Carte_Pour_Canvas.__init__(self,jour,mois,annee,run,echeance,type_carte,zoom)
        
        Frame.__init__(self)
        
        self.verification = verification
        self.canev=canev
        #self.echeance = echeance
        
    def envoyer_Carte_Vers_Gui(self):
        
        self.construire_Noms()
        
        indice_echeance,grbs = self.trouver_indice_echeance()
        
        gt_1 = grbs.select(shortName = 'papt', level = 850)[indice_echeance]
        gt_2 = grbs.select(shortName = 'z', level = 1500000000)[indice_echeance]

        ech_Mois = str(gt_1.validityDate)[4:6]
        ech_Jour = str(gt_1.validityDate)[6:8]

        if gt_1.validityTime<1000:
            ech_Heure = str(gt_1.validityTime)[0]
        else:
            ech_Heure = str(gt_1.validityTime)[0:2]

        #print("gt_U:",gt_tpw.validityDate,gt_tpw.validityTime)
        validite ="Prévision pour le " + ech_Jour + "/" + ech_Mois+ " " + ech_Heure + "H"

        tt_1 = gt_1.values
        tt_2 = gt_2.values

        lats,lons=gt_1.latlons()

        del(gt_1)
        del(gt_2)
        
        grbs.close()
        
        tt_2 = (tt_2/10)
        tt_2 = tt_2.astype(int)

        tt_1 = (tt_1-273.15)
        tt_1 = tt_1.astype(int)

        f,ax = self.dessiner_fond_carte(lons,lats)
        
        origin='lower'
        levels = np.arange(-40,44,4)
        levels_pvu = np.arange(0,12000,1000)

        cs = ax.pcolormesh(lons, lats, tt_1, vmin=-12, vmax=26,cmap='nipy_spectral',transform=ccrs.PlateCarree())
        cs1 = ax.contour(lons, lats, tt_1, levels,transform=ccrs.PlateCarree(),
                  colors=('k'),
                  linewidths=(0.2),linestyles='dashed',
                  origin=origin)
        cs_pvu = ax.contour(lons, lats, tt_2, levels_pvu,transform=ccrs.PlateCarree(),
                  colors=('k'),
                  linewidths=(0.3),
                  origin=origin)
        csb = plt.colorbar(cs)

        #csb.set_label("Theta'w 850hPa (°C)")

        lala_pvu = plt.clabel(cs_pvu, fontsize=8, fmt='%1.0f')
        lala_tpw = plt.clabel(cs1, fontsize=8, fmt='%1.0f')


        if self.echeance < 10:
            titre = self.titre_0 + "\n" + validite
            nom = self.nom_0 + str(self.echeance)+'H.png'
        else:
            titre = self.titre_10 + "\n" + validite
            nom = self.nom_10 + str(self.echeance)+'H.png'

        ax.set_title(titre)
        #plt.savefig(nom,dpi=300)

        #if self.verification == 1:
        
        #ax.plt.show()
        plt.show()
        plt.close()
        self.canev = FigureCanvasTkAgg(f, self.master)
        self.canev.show()
        self.canev.get_tk_widget().pack(expand=True)
        
        toolbar = NavigationToolbar2TkAgg(self.canev, self.master)
        toolbar.update()
        self.canev._tkcanvas.pack(expand=True)
        
        #plt.close()
        
        del(tt_1)
        del(tt_2)
        del(titre)
        del(nom)
        
        #f = Figure(figsize=(5,5), dpi=100)
        #a = f.add_subplot(111)
        #a = fig
        
        print("coucou")
        
class Carte_T2m(Arome_0025_Carte_Pour_Canvas):
    """Renvoie la carte de températures à deux mètre prévue par Arome 0.025°."""
    def __init__(self,boss,canev,jour,mois,annee,run,echeance,type_carte,zoom,verification):
        
        Arome_0025_Carte_Pour_Canvas.__init__(self,jour,mois,annee,run,echeance,type_carte,zoom)
        
        Frame.__init__(self)
        
        self.verification = verification
        self.canev=canev
        #self.echeance = echeance
        
    def envoyer_Carte_Vers_Gui(self):
        
        self.construire_Noms()
        
        indice_echeance,grbs = self.trouver_indice_echeance()

        gt = grbs.select(shortName = '2t')[indice_echeance]
        
        print("Échéance: ",self.echeance)
        print("indice échéance 1: ",indice_echeance)
                
        ech_Mois = str(gt.validityDate)[4:6]
        ech_Jour = str(gt.validityDate)[6:8]

        if gt.validityTime<1000:
            ech_Heure = str(gt.validityTime)[0]
        else:
            ech_Heure = str(gt.validityTime)[0:2]

        validite ="Prévision pour le " + ech_Jour + "/" + ech_Mois+ " " + ech_Heure + "H"

        if self.zoom == 0:
            tt, lats, lons = gt.data()#(lat1=43,lat2=47,lon1=2.25,lon2=7.5)
        elif self.zoom == 1:
            tt, lats, lons = gt.data(lat1=43,lat2=47,lon1=2.25,lon2=7.5)

        print("Champ: ", gt.shortName, "    Validité: ", gt.validityDate, " à ",gt.validityTime)

        del(gt)
        grbs.close()

        tt = (tt-273.15)
        tt = tt.astype(int)

        f,ax = self.dessiner_fond_carte(lons,lats)

        origin='lower'
        levels = np.arange(-34,44,1)

        levels_contour_2 = np.arange(-40,48,4)

        cc = ax.contour(lons, lats, tt, levels_contour_2,
                      colors=('k'),
                      linewidths=(0.15),
                      origin=origin,transform=ccrs.PlateCarree())

        if self.verification == 1:
            print("fin contour")

        #plt.clabel(cs2, fontsize=4, fmt='%1.0f')

        bb = ax.pcolormesh(lons, lats, tt, vmin=-34,vmax=44, cmap='nipy_spectral',transform=ccrs.PlateCarree())

        csb = plt.colorbar(bb)

        csb.set_label("(°C)")
        #csb.set_label("Module du Jet (m/s)")
        #ax.barbs(lons[::50],lats[::50], vent_Zonal[::50], vent_Meri[::50],transform=ccrs.PlateCarree(),length=5)

        lala_pvu = plt.clabel(cc, fontsize=8, fmt='%1.0f')

        if self.verification == 1:
            print("fin contourf")

        #csb = m.colorbar(cs)
        #csb.set_label("°C")

        if self.echeance < 10:
            titre = self.titre_0 + "\n" + validite
            nom = self.nom_0 + str(self.echeance)+'H.png'
        else:
            titre = self.titre_10 + "\n" + validite
            nom = self.nom_10 + str(self.echeance)+'H.png'

        print(titre)
        print(nom)

        plt.title(titre)
        #plt.savefig(nom,dpi=300)

        #if self.verification == 1:
        plt.show()
        plt.close()
        #self.canev.get_tk_widget().destroy()
        self.canev = FigureCanvasTkAgg(f, self.master)
        self.canev.show()
        self.canev.get_tk_widget().pack(expand=True)
        
        toolbar = NavigationToolbar2TkAgg(self.canev, self.master)
        toolbar.update()
        self.canev._tkcanvas.pack(expand=True)
        
        #print("fin show")
        plt.close()

        del(tt)
        del(titre)
        del(nom)
