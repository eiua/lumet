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

class Arpege_05_Cartes():
    """Exploiter les fichiers Arpege 0.5°, dessin de cartes usuelles en météo et 
    tracé de diagrammes de prévision de divers paramètres courants.
    
    Copyleft Lucas GRIGIS (code sous licence GPL)
    
    #############################################################################
    
    Il faut télécharger les fichiers Arome 0.025° SP1 et IP5 (format .grib2)
    disponibles en téléchargement sur le site de Météo-France:
    https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=131&id_rubrique=51
    
    Ensuite on renome les fichiers:
    écourter par exemple *12H18H* en *18H*, cas particulier: *00H06H* deviendra *6H*
    
    Enregistrer ce présent fichier dans le répertoire racine de votre pojet 
    (dans lequel sera par example lancé votre session jupyter).
    
    Stocker les fichiers de données .grib2 dans un répertoire ./Aro_00025/20602018 
    (date à modifier à votre convenance, mais respecter le format jourmoisannée).
    
    ###############################################################################
    
    Example d'exécution:
    
    ##
    from Arome_0025_Cartes import *
    #Cartes France entière:
    h=Arome_0025_Cartes("20","06","2018","03",zoom = 0,verification = 0)
    h.carte_T2m()
    h.carte_DSW()
    h.carte_Jet_Z15()
    h.carte_Precips()
    
    #Carte zoom région Rhône-Alpes:
    g=Arome_0025_Cartes("20","06","2018","03",zoom = 1,verification = 0)
    g.carte_T2m()
    g.carte_DSW()
    g.carte_Precips()

    g.histogramme_DSW()
    g.histogramme_Precips()
    g.histogramme_T2m()
    g.histogramme_Vent10m()
    ##
    """
    
    def __init__(self,jour,mois,annee,run,zoom,verification):
        """Chaînes de caractères pour les numéros de jour, mois et de l'année.
        Entiers pour le zoom et verification.
        Cartes couvrant la France entière (zoom = 0); ou cartes plus détaillées avec 
        zoom sur la région Rhône-Alpes (zoom = 1).
        Afficher divers paramètres pour vérification du bon déroulement de l'exécution du code."""
        
        self.jour = jour
        self.mois = mois
        self.annee = annee
        self.run = run
        self.zoom = zoom
        self.verification = verification
        
        self.type_de_carte = " "
        
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
        
        
        self.nom_fichier_1 = "./Arp_05/"+ self.jour + self.mois + self.annee + "/ARPEGE_0.5_" + SP1_IP5 +"_"
        self.nom_fichier_2 = "H_" + self.annee + self.mois + self.jour + self.run + "00.grib2"
        
        self.titre_0 = titre_00 + ' Arp 0.5° run ' + self.run + 'h ' + self.jour +'/'+self.mois+'/'+self.annee +'0'
        self.titre_10 = titre_00 + ' Arp 0.5° run ' + self.run + 'h ' + self.jour +'/'+self.mois+'/'+self.annee
        
        self.nom_0 = './Arp_05/' + self.jour + self.mois + self.annee + nom_00 + '_Arp_05_' + self.jour + self.mois + self.annee + self.run + '_0'
        self.nom_10 = './Arp_05/' + self.jour + self.mois + self.annee + nom_00 + '_Arp_05_' + self.jour + self.mois + self.annee + self.run + '_'

    def dessiner_fond_carte(self,lon_0,lat_0,lonn,lonx,latn,latx):
        
        #proj = ccrs.Stereographic(central_longitude=lon_0,central_latitude=lat_0)
        proj = ccrs.NorthPolarStereo(central_longitude=0.0, globe=None)
        
        ax = plt.axes(projection=proj)

        #ax.set_extent([lons.min(), lons.max(), lats.min()-0.5, lats.max()])

        #ax.add_feature(cfeature.BORDERS)

        pays = cfeature.NaturalEarthFeature(category='cultural',name='admin_0_countries',
                                           scale='10m',facecolor='none')
        ax.add_feature(pays,edgecolor='black',linewidth=(0.7))

        fleuves = cfeature.NaturalEarthFeature(category='physical',name='rivers_lake_centerlines',
                                           scale='10m',facecolor='none')
        ax.add_feature(fleuves,edgecolor='blue',linewidth=(0.3))
        #rivieres = cfeature.NaturalEarthFeature(category='physical',name='rivers_europe',
         #                                  scale='10m',facecolor='none')
        #ax.add_feature(rivieres,edgecolor='blue',linewidth=(0.3))

        #ax.set_extent([lonn, lonx, latn + 0.5 , latx])
            
        return ax  
        
    def cartes_T2m(self):
        """Renvoie les cartes de températures à deux mètre prévues par Arome 0.025°.
        Crée une figure par échéance donc une par heure, renvoie et sauvegarde l'intégralité des cartes."""
        
        self.type_de_carte = "T2m"
        self.construire_Noms()
        
        compteur = 0
        
        for t_fichier in (24,48,72,102):

            nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
            grbs = pygrib.open(nom_fichier)

            if t_fichier == 24 or t_fichier == 102:
                ech_U = range(0,9,1)
            else:
                ech_U = range(0,8,1)
            
            for echeance in ech_U:
                
                gt = grbs.select(shortName = '2t')[echeance]
                
                tt,lats,lons = gt.data(lat1=0,lat2=90)
                
                print(lons.min())
                print(lons.max())
                print(lats.min())
                print(lats.max())
                
                ech_Mois = str(gt.validityDate)[4:6]
                ech_Jour = str(gt.validityDate)[6:8]
                
                if gt.validityTime<1000:
                    ech_Heure = str(gt.validityTime)[0]
                else:
                    ech_Heure = str(gt.validityTime)[0:2]
                
                validite ="Prévision pour le " + ech_Jour + "/" + ech_Mois+ " " + ech_Heure + "H"

                print("Champ: ", gt.shortName, "    Validité: ", gt.validityDate, " à ",gt.validityTime)
  
                #if compteur == 0:
                    #lats,lons = gt.latlons()
                
                del(gt)
                #print(type(tt))
                tt = (tt-273.15)
                tt = tt.astype(int)
                
                if self.verification == 1:
                    print("fin calculs")
                
                ax = self.dessiner_fond_carte(0,45,290,40,20,90)
                
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
                
                lala_pvu = plt.clabel(cc, fontsize=4, fmt='%1.0f')
                
                if self.verification == 1:
                    print("fin contourf")
                
                #csb = m.colorbar(cs)
                #csb.set_label("°C")

                if compteur < 10:
                    titre = self.titre_0 + "\n" + validite
                    nom = self.nom_0 + str(compteur)+'H.png'
                else:
                    titre = self.titre_10 + "\n" + validite
                    nom = self.nom_10 + str(compteur)+'H.png'
                
                if self.verification == 1:
                    print(titre)
                    print(nom)
                
                plt.title(titre)
                plt.savefig(nom,dpi=300)

                if self.verification == 1:
                    print("fin savefig")
                
                #if self.verification == 1:
                #plt.show()
                #print("fin show")
                plt.close()

                del(tt)
                del(titre)
                del(nom)

                compteur=compteur+1

            grbs.close()

    def cartes_Precips(self):
        """Renvoie les cartes de lame d'eau horaire (mm) prévues par Arome 0.025°.
        Crée une figure par échéance donc une par heure, renvoie et sauvegarde l'intégralité des cartes."""
        
        self.type_de_carte = "Precips"
        self.construire_Noms()
        
        compteur = 1
        
        for t_fichier in (24,48,72,102):

            nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
            grbs = pygrib.open(nom_fichier)

            if t_fichier == 24 or t_fichier == 102:
                ech_U = range(0,8,1)
            else:
                ech_U = range(0,8,1)

            for echeance in ech_U:
                
                gt = grbs.select(shortName = 'tp')[echeance]

                ech_Mois = str(gt.validityDate)[4:6]
                ech_Jour = str(gt.validityDate)[6:8]
                
                if gt.validityTime<1000:
                    ech_Heure = str(gt.validityTime)[0]
                else:
                    ech_Heure = str(gt.validityTime)[0:2]
                    
                print("Champ: ", gt.shortName, "    Validité: ", gt.validityDate, " à ",gt.validityTime)
                
                validite ="Prévision pour le " + ech_Jour + "/" + ech_Mois+ " " + ech_Heure + "H"
                
                if self.verification == 1:
                    print(gt)

                if compteur == 1:
                    tt1, lats, lons = gt.data(lat1=0,lat2=90)

                    lon_0 = lons.mean()
                    lat_0 = lats.mean()
                    lonn = lons.min()
                    latn = lats.min()
                    lonx = lons.max()
                    latx = lats.max()

                    tt0 = 0

                else:
                    tt0 = tt1

                    tt1, lats, lons = gt.data(lat1=0,lat2=90)
                    
                del(gt)
                
                tete = tt1 - tt0
                
                tt = np.ma.masked_less(tete, 0.1)
                
                if self.verification == 1:
                    print(type(tt))

                ax = self.dessiner_fond_carte(0,45,290,40,20,90)

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
                
                if compteur < 10:
                    titre = self.titre_0 + "\n" + validite
                    nom = self.nom_0 + str(compteur)+'H.png'
                else:
                    titre = self.titre_10 + "\n" + validite
                    nom = self.nom_10 + str(compteur)+'H.png'
                
                if self.verification == 1:
                    print(titre)
                    print(nom)
                
                plt.title(titre)
                plt.savefig(nom,dpi=300)

                #plt.title('T2m (°C) Arp 0.1° 16/05/2018 0Z')
                #plt.savefig("T2m_Arp_01_16052018_0Z.png",dpi=600)

                #if self.verification == 1:
                #plt.show()
                plt.close()

                del(titre)
                del(nom)
                compteur=compteur+1

            grbs.close()

    def cartes_DSW(self):
        """Renvoie les cartes de rayonnement SW descendant (KW/m2/h) prévues par Arome 0.025°.
        Crée une figure par échéance donc une par heure, renvoie et sauvegarde l'intégralité des cartes."""
        
        self.type_de_carte = "DSW"
        
        self.construire_Noms()
        
        compteur = 1
        
        for t_fichier in (24,48,72,102):

            nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
            grbs = pygrib.open(nom_fichier)

            if t_fichier == 24 or t_fichier == 102:
                ech_U = range(0,8,1)
            else:
                ech_U = range(0,8,1)
            
            for echeance in ech_U:
                
                gt = grbs.select(shortName = 'dswrf')[echeance]

                ech_Mois = str(gt.validityDate)[4:6]
                ech_Jour = str(gt.validityDate)[6:8]
                
                if gt.validityTime<1000:
                    ech_Heure = str(gt.validityTime)[0]
                else:
                    ech_Heure = str(gt.validityTime)[0:2]
                    
                print("Champ: ", gt.shortName, "    Validité: ", gt.validityDate, " à ",gt.validityTime)
                
                validite ="Prévision pour le " + ech_Jour + "/" + ech_Mois+ " " + ech_Heure + "H"

                if compteur == 1:
                    #if self.zoom == 0:
                     #   tt1, lats, lons = gt.data()
                    #elif self.zoom == 1:
                    tt1, lats, lons = gt.data(lat1=0,lat2=90)

                    lon_0 = lons.mean()
                    lat_0 = lats.mean()
                    lonn = lons.min()
                    latn = lats.min()
                    lonx = lons.max()
                    latx = lats.max()
                    
                    tt0 = 0

                else:
                    tt0 = tt1
                    
                    #if self.zoom == 0:
                     #   tt1, lats, lons = gt.data()
                    #elif self.zoom == 1:
                    tt1, lats, lons = gt.data(lat1=0,lat2=90)

                del(gt)
                                                  
                tt = tt1 - tt0
                
                tt = (tt/1000)
                tt = tt.astype(int)
                
                ax = self.dessiner_fond_carte(0,45,290,40,20,90)

                #origin='lower'
                #levels = np.arange(1,int(tt.max()),1)
                #levels_contour = np.arange(1,int(tt.max()),2)
                #levels = np.arange(0,4000,50)
                #levels_contour = np.arange(0,4000,50)

                cs=ax.pcolormesh(lons, lats, tt,vmin=0.01,vmax=10000, cmap='jet',transform=ccrs.PlateCarree())

                csb = plt.colorbar(cs)
                csb.set_label("kW/m2/h")
                
                if compteur < 10:
                    titre = self.titre_0 + "\n" + validite
                    nom = self.nom_0 + str(compteur)+'H.png'
                else:
                    titre = self.titre_10 + "\n" + validite
                    nom = self.nom_10 + str(compteur)+'H.png'
                
                if self.verification == 1:
                    print(titre)
                    print(nom)
                plt.title(titre)
                plt.savefig(nom,dpi=300)

                #if self.verification == 1:
                #plt.show()
                    
                plt.close()

                del(titre)
                del(nom)
                compteur=compteur+1

            grbs.close()

        del(compteur)
