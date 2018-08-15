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

class Arome_0025_Cartes():
    """Exploiter les fichiers Arome 0.025°, dessin de cartes usuelles en météo et 
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
        
        
        self.nom_fichier_1 = "./Aro_00025/"+ self.jour + self.mois + self.annee + "/AROME_0.025_" + SP1_IP5 +"_"
        self.nom_fichier_2 = "H_" + self.annee + self.mois + self.jour + self.run + "00.grib2"
        
        self.titre_0 = titre_00 + ' Aro 0.025° run ' + self.run + 'h ' + self.jour +'/'+self.mois+'/'+self.annee +'0'
        self.titre_10 = titre_00 + ' Aro 0.025° run ' + self.run + 'h ' + self.jour +'/'+self.mois+'/'+self.annee
        
        self.nom_0 = './Aro_00025/' + self.jour + self.mois + self.annee + nom_00 + '_Aro_0025_' + self.jour + self.mois + self.annee + self.run + '_0'
        self.nom_10 = './Aro_00025/' + self.jour + self.mois + self.annee + nom_00 + '_Aro_0025_' + self.jour + self.mois + self.annee + self.run + '_'

    def dessiner_fond_carte(self,lon_0,lat_0,lonn,latn,lonx,latx):
        
        proj = ccrs.Stereographic(central_longitude=lon_0,central_latitude=lat_0)
        
        ax = plt.axes(projection=proj)

        pays = cfeature.NaturalEarthFeature(category='cultural',name='admin_0_countries',
                                           scale='10m',facecolor='none')
        ax.add_feature(pays,edgecolor='black',linewidth=(0.7))

        fleuves = cfeature.NaturalEarthFeature(category='physical',name='rivers_lake_centerlines',
                                           scale='10m',facecolor='none')
        ax.add_feature(fleuves,edgecolor='blue',linewidth=(0.3))
        rivieres = cfeature.NaturalEarthFeature(category='physical',name='rivers_europe',
                                           scale='10m',facecolor='none')
        ax.add_feature(rivieres,edgecolor='blue',linewidth=(0.3))
        
        ax.plot([4.875,4.8148,5.7242],[45.775,45.1896,45.1721], 'bo',color="red", markersize=0.5,transform=ccrs.PlateCarree())
        
        if self.zoom == 1:
            ax.set_extent([lonn, lonx, latn, latx])
        else:
            ax.set_extent([lonn, lonx, latn + 0.5 , latx])

        return ax
        
    def charger_Tout(self):
        """Renvoie les cartes du géopotentiel au niveau Z1.5pvu associée à la température potentielle 
        pseudo-adiabatique au niveau 850hPa (TPw850hPa)  prévues par Arome 0.025°.
        Le niveau Z1.5pvu correspond à la tropopause.
        Permet de regarder le forçage d'altitude (Z1.5pvu) et l'énergie disponible 
        dans les basses couches (TPw850hPa).
        Crée une figure par échéance donc une par heure, renvoie et sauvegarde l'intégralité des cartes."""
        
        #self.type_de_carte = "TPW850_Z1.5pvu"
        self.construire_Noms()
        
        compteur = 0
        
        for t_fichier in (6,12,18,24,30,36,42):

            nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
            grbs = pygrib.open(nom_fichier)

            if t_fichier == 6:
                ech_U = range(0,7,1)
            elif t_fichier in (12,18,24,30,36):
                ech_U = range(0,6,1)
            else:
                if self.run == "03":
                    ech_U = range(0,3,1)
                else:
                    ech_U= range(0,6,1)

            for echeance in ech_U:
                
                if self.type_de_carte == "TPW850_Z15pvu":  
                    gt_1 = grbs.select(shortName = 'papt', level = 850)[echeance]
                    gt_2 = grbs.select(shortName = 'z', level = 1500000000)[echeance]
                elif self.type_de_carte == "T2m":
                    gt_1 = grbs.select(shortName = '2t')[echeance]
                
                if compteur == 0:
                    lats,lons=gt_1.latlons()
                    tt = []
                    #tts = []
                    pvu = []
                
                ech_Mois = str(gt_1.validityDate)[4:6]
                ech_Jour = str(gt_1.validityDate)[6:8]
                
                if gt_1.validityTime<1000:
                    ech_Heure = str(gt_1.validityTime)[0]
                else:
                    ech_Heure = str(gt_1.validityTime)[0:2]
                    
                validite ="Prévision pour le " + ech_Jour + "/" + ech_Mois+ " " + ech_Heure + "H"
                
                print(validite)
                print(compteur)
                
                if self.type_de_carte == "TPW850_Z15pvu" or self.type_de_carte == "T2m":
                    tures = gt_1.values - 273.15
                    tt.append(tures.astype(int))
                
                if self.type_de_carte == "TPW850_Z15pvu":
                    pvuz = gt_2.values / 10
                    pvu.append(pvuz.astype(int))
                
                #lat1=45.774,lat2=45.776,lon1=4.874,lon2=4.876
                #print(type(lons))
                #la = lats.astype(float).round(4)
                #print(la)
                #la = np.where(lats == 45.7750)
                #print(la)
                #print(lats[la])
                
                
                
                del(gt_1)
                del(tures)
                
                if self.type_de_carte == "TPW850_Z15pvu":
                    del(gt_2)
                    del(pvuz)
                
                compteur = compteur+1

            grbs.close()
            
        if self.type_de_carte == "TPW850_Z15pvu":
            return(tt,ttt,lons,lats)
        elif self.type_de_carte == "T2m":
            return(tt,lons,lats)
            
    def cartes_TPW850_Z15(self):
        """Renvoie les cartes du géopotentiel au niveau Z1.5pvu associée à la température potentielle ê
        pseudo-adiabatique au niveau 850hPa (TPw850hPa)  prévues par Arome 0.025°.
        Le niveau Z1.5pvu correspond à la tropopause.
        Permet de regarder le forçage d'altitude (Z1.5pvu) et l'énergie disponible 
        dans les basses couches (TPw850hPa).
        Crée une figure par échéance donc une par heure, renvoie et sauvegarde l'intégralité des cartes."""
        
        self.type_de_carte = "TPW850_Z1.5pvu"
        self.construire_Noms()
        
        compteur = 0
        
        for t_fichier in (6,12,18,24,30,36,42):

            nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
            grbs = pygrib.open(nom_fichier)

            if t_fichier == 6:
                ech_U = range(0,7,1)
            elif t_fichier in (12,18,24,30,36):
                ech_U = range(0,6,1)
            else:
                if self.run == "03":
                    ech_U = range(0,3,1)
                else:
                    ech_U= range(0,6,1)

            for echeance in ech_U:

                gt_tpw = grbs.select(shortName = 'papt', level = 850)[echeance]
                gt_pvu = grbs.select(shortName = 'z', level = 1500000000)[echeance]
 
                ech_Mois = str(gt_tpw.validityDate)[4:6]
                ech_Jour = str(gt_tpw.validityDate)[6:8]
                
                if gt_tpw.validityTime<1000:
                    ech_Heure = str(gt_tpw.validityTime)[0]
                else:
                    ech_Heure = str(gt_tpw.validityTime)[0:2]
                
                print("gt_U:",gt_tpw.validityDate,gt_tpw.validityTime)
                validite ="Prévision pour le " + ech_Jour + "/" + ech_Mois+ " " + ech_Heure + "H"

                tt = gt_tpw.values
                pvu = gt_pvu.values

                if compteur == 0:
                    lats,lons=gt_pvu.latlons()

                    lon_0 = lons.mean()
                    lat_0 = lats.mean()
                    lonn = lons.min()
                    latn = lats.min()
                    lonx = lons.max()
                    latx = lats.max()

                del(gt_tpw)
                del(gt_pvu)

                pvu = (pvu/10)
                pvu = pvu.astype(int)
                
                tt = (tt-273.15)
                tt = tt.astype(int)

                ax = self.dessiner_fond_carte(lon_0,lat_0,lonn,latn,lonx,latx)

                origin='lower'
                levels = np.arange(-40,44,4)
                levels_pvu = np.arange(0,12000,1000)
                    
                cs = ax.pcolormesh(lons, lats, tt, vmin=-12, vmax=26,cmap='nipy_spectral',transform=ccrs.PlateCarree())
                cs1 = ax.contour(lons, lats, tt, levels,transform=ccrs.PlateCarree(),
                              colors=('k'),
                              linewidths=(0.2),linestyles='dashed',
                              origin=origin)
                cs_pvu = ax.contour(lons, lats, pvu, levels_pvu,transform=ccrs.PlateCarree(),
                              colors=('k'),
                              linewidths=(0.3),
                              origin=origin)
                csb = plt.colorbar(cs)
                csb.set_label("Theta'w 850hPa (°C)")

                lala_pvu = plt.clabel(cs_pvu, fontsize=4, fmt='%1.0f')
                lala_tpw = plt.clabel(cs1, fontsize=4, fmt='%1.0f')
                

                if compteur < 10:
                    titre = self.titre_0 + "\n" + validite
                    nom = self.nom_0 + str(compteur)+'H.png'
                else:
                    titre = self.titre_10 + "\n" + validite
                    nom = self.nom_10 + str(compteur)+'H.png'

                plt.title(titre)
                plt.savefig(nom,dpi=300)
                
                #if self.verification == 1:
                #plt.show()
                
                plt.close()
                
                compteur = compteur+1
                del(pvu)
                del(tt)
                del(titre)
                del(nom)

            grbs.close()
            
    def cartes_Jet_Z15(self):
        """Renvoie les cartes du géopotentiel au niveau Z1.5pvu associé au module du Jet
        au niveau Z1.5pvu prévues par Arome 0.025°.
        Le niveau Z1.5pvu correspond à la tropopause.
        Permet de regarder les forçages d'altitude.
        Crée une figure par échéance donc une par heure, renvoie et sauvegarde l'intégralité des cartes."""
        
        self.type_de_carte = "Jet_Z1.5pvu"
        
        self.construire_Noms()
        
        compteur = 0
        for t_fichier in (6,12,18,24,30,36,42):

            nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2

            grbs = pygrib.open(nom_fichier)
            
            if t_fichier==6:
                ech_U = range(0,7,1)

            elif t_fichier in (12,18,24,30,36):
                ech_U = range(0,6,1)

            else:
                if self.run == "03":
                    ech_U = range(0,3,1)
                else:
                    ech_U = range(0,6,1)

            for echeance in ech_U:        
                gt_U = grbs.select(shortName='u',level=1500000000)[echeance]
                gt_V = grbs.select(shortName='v',level=1500000000)[echeance]
                gt_pvu = grbs.select(shortName='z',level=1500000000)[echeance]
                
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
                
                print(type(vent_Zonal))
                #vent_Zonal = gt_U.values
                #vent_Meri = gt_V.values
                #print(type(vent_Zonal))
                
                pvu=gt_pvu.values
                
                if compteur == 0:
                    lats,lons=gt_U.latlons()

                    lon_0 = lons.mean()
                    lat_0 = lats.mean()
                    lonn = lons.min()
                    latn = lats.min()
                    lonx = lons.max()
                    latx = lats.max()

                del(gt_U)
                del(gt_V)
                del(gt_pvu)

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
                
                #vent_zonal = np.ma.MaskedArray(vent_Zonal,tt < 20 )
                #vent_meri = np.ma.MaskedArray(vent_Meri, tt < 20 )
                #print(vent_zonal)
                
                pvu = (pvu/10)
                pvu =  pvu.astype(int)
                
                if compteur < 10:
                    titre = self.titre_0 + "\n" + validite# + str(compteur)+'H'
                    nom = self.nom_0 + str(compteur)+'H.png'
                else:
                    titre = self.titre_10 + "\n" + validite#str(compteur)+'H'
                    nom = self.nom_10 + str(compteur)+'H.png'
                
                if self.verification == 1:
                    print(titre)
                    print(nom)
                
                ax = self.dessiner_fond_carte(lon_0,lat_0,lonn,latn,lonx,latx)
                
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
                plt.savefig(nom,dpi=300)

                #if self.verification == 1:
                #plt.show()
                plt.close()
                compteur = compteur + 1

                del(pvu)
                del(Zm)
                del(tt)
                del(titre)
                del(nom)

            grbs.close()
        del(compteur)   
        
    def cartes_T2m(self):
        """Renvoie les cartes de températures à deux mètre prévues par Arome 0.025°.
        Crée une figure par échéance donc une par heure, renvoie et sauvegarde l'intégralité des cartes."""
        start_program = time.time()
        self.type_de_carte = "T2m"
        self.construire_Noms()
        
        compteur = 0
        
        for t_fichier in (6,12,18,24,30,36,42):
            
            if self.verification == 1:
                print("début")
            nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
            
            grbs = pygrib.open(nom_fichier)

            if t_fichier==6:
                echT=range(0,7,1)
            
            elif t_fichier==42:
                if self.run == "03":
                    echT = range(0,3,1)
                else:
                    echT = range(0,6,1)
            
            elif t_fichier in (12,18,24,30,36):
                echT=range(0,6,1)
            
            for echeance in echT:
                start = time.time()
                gt = grbs.select(shortName = '2t')[echeance]
                
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
                
                if compteur == 0:
                    lon_0 = lons.mean()
                    lat_0 = lats.mean()
                    lonn = lons.min()
                    latn = lats.min()
                    lonx = lons.max()
                    latx = lats.max()

                tt = (tt-273.15)
                tt = tt.astype(int)
                
                if self.verification == 1:
                    print("fin calculs")
                
                ax = self.dessiner_fond_carte(lon_0,lat_0,lonn,latn,lonx,latx)
                
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
                print("Total time taken to save fig ",compteur, "is", time.time()-start)

                del(tt)
                del(titre)
                del(nom)

                compteur=compteur+1

            grbs.close()
            
        end_program = time.time()
        print("Total time to complete program is :", end_program - start_program)

    def cartes_Precips(self):
        """Renvoie les cartes de lame d'eau horaire (mm) prévues par Arome 0.025°.
        Crée une figure par échéance donc une par heure, renvoie et sauvegarde l'intégralité des cartes."""
        
        self.type_de_carte = "Precips"
        self.construire_Noms()
        
        compteur = 1
        
        for t_fichier in (6,12,18,24,30,36,42):

            nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
            grbs = pygrib.open(nom_fichier)

            if t_fichier==6:
                echT=range(0,6,1)

            elif t_fichier in (12,18,24,30,36):
                echT=range(0,6,1)
                
            elif t_fichier==42:
                if self.run == "03":
                    echT = range(0,3,1)
                else:
                    echT = range(0,6,1)

            for echeance in echT:
                
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
                    if self.zoom == 0:
                        tt1, lats, lons = gt.data()#(lat1=43,lat2=47,lon1=2.25,lon2=7.5)
                    elif self.zoom == 1:
                        tt1, lats, lons = gt.data(lat1=43,lat2=47,lon1=2.25,lon2=7.5)

                    lon_0 = lons.mean()
                    lat_0 = lats.mean()
                    lonn = lons.min()
                    latn = lats.min()
                    lonx = lons.max()
                    latx = lats.max()

                    tt0 = 0

                else:
                    tt0 = tt1

                    if self.zoom == 0:
                        tt1, lats, lons = gt.data()#(lat1=43,lat2=47,lon1=2.25,lon2=7.5)
                    elif self.zoom == 1:
                        tt1, lats, lons = gt.data(lat1=43,lat2=47,lon1=2.25,lon2=7.5)
                    
                del(gt)
                
                tete = tt1 - tt0
                
                tt = np.ma.masked_less(tete, 0.1)
                
                if self.verification == 1:
                    print(type(tt))

                ax = self.dessiner_fond_carte(lon_0,lat_0,lonn,latn,lonx,latx)

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
        for t_fichier in (6,12,18,24,30,36,42):

            nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2

            grbs = pygrib.open(nom_fichier)

            if t_fichier == 6:
                ech_DSW = range(0,6,1)
            elif t_fichier in (12,18,24,30,36):
                ech_DSW = range(0,6,1)
            else:
                if self.run == "03":
                    ech_DSW = range(0,3,1)
                else:
                    ech_DSW = range(0,6,1)
            
            for echeance in ech_DSW:
                
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
                    if self.zoom == 0:
                        tt1, lats, lons = gt.data()
                    elif self.zoom == 1:
                        tt1, lats, lons = gt.data(lat1=43,lat2=47,lon1=2.25,lon2=7.5)

                    lon_0 = lons.mean()
                    lat_0 = lats.mean()
                    lonn = lons.min()
                    latn = lats.min()
                    lonx = lons.max()
                    latx = lats.max()
                    
                    tt0 = 0

                else:
                    tt0 = tt1
                    
                    if self.zoom == 0:
                        tt1, lats, lons = gt.data()
                    elif self.zoom == 1:
                        tt1, lats, lons = gt.data(lat1=43,lat2=47,lon1=2.25,lon2=7.5)

                del(gt)
                                                  
                tt = tt1 - tt0
                
                tt = (tt/1000)
                tt = tt.astype(int)
                
                ax = self.dessiner_fond_carte(lon_0,lat_0,lonn,latn,lonx,latx)

                #origin='lower'
                #levels = np.arange(1,int(tt.max()),1)
                #levels_contour = np.arange(1,int(tt.max()),2)
                #levels = np.arange(0,4000,50)
                #levels_contour = np.arange(0,4000,50)

                cs=ax.pcolormesh(lons, lats, tt,vmin=0.01,vmax=4000, cmap='jet',transform=ccrs.PlateCarree())

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
        
    def histogramme_DSW(self):
        """Renvoie un diagramme du rayonnement SW descendant (KW/m2/h) prévu par Arome 0.025°.
        Crée une figure unique qui courvre toutes les échéances (les échéances d'Arome 0.025° 
        sont au pas de temps horaire), renvoie et sauvegarde le diagramme."""
        
        self.type_de_carte = "histo_DSW"
        self.construire_Noms()
        
        compteur = 0
        
        if self.run == "03":
            tp = np.arange(39, dtype='f')
            cumul = np.arange(39, dtype='f')
            ctp = np.arange(39)
        else:
            tp = np.arange(43, dtype='f')
            cumul = np.arange(40, dtype='f')
            ctp = np.arange(39)
        for t_fichier in (6,12,18,24,30,36,42):

            nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
            
            grbs = pygrib.open(nom_fichier)

            if t_fichier==6:
                echT=range(0,6,1)
                
            elif t_fichier==42:
                if self.run == "03":
                    echT=range(0,3,1)
                else:
                    echT=range(0,6,1)
            
            elif t_fichier in (12,18,24,30,36):
                echT=range(0,6,1)

            for echeance in echT:
                
                gt = grbs.select(shortName = 'dswrf')[echeance]
                
                print("Champ: ", gt.shortName, "    Validité: ", gt.validityDate, " à ",gt.validityTime)
                
                if compteur == 0:
                    tt1, lats, lons = gt.data(lat1=45.774,lat2=45.776,lon1=4.874,lon2=4.876)
                    tt0 = 0
                    
                else:
                    tt0 = tt1
                    tt1, lats, lons = gt.data(lat1=45.774,lat2=45.776,lon1=4.874,lon2=4.876)
                    
                del(gt)
                
                cumul[compteur] = tt1 / 1000
                tp[compteur] = (tt1 - tt0)/1000
                
                ctp[compteur] = compteur

                compteur=compteur+1
        
            grbs.close()
        
        if self.verification == 1:
            print(len(tp))
            print(len(ctp))
        
        #aa, bb = plt.subplots()
        #aa = plt.plot(ctp, cumul)
        plt.plot(ctp,tp,color='red')

        #aa = plt.plot_date(ctp,cumul,color='blue')
        plt.ylabel("Rayonnement SW descendant (Wh/m2)")
        plt.xlabel('Échéances de prévision (heures)')
        
        plt.title(self.titre_0)
        
        plt.grid()
        plt.savefig(self.nom_0,dpi=300)
        
        #if self.verification == 1:
        #plt.show()
            
        plt.close()
        
    def histogramme_T2m(self):
        """Renvoie un diagramme de la température à deux mètres (°C) prévu par Arome 0.025°.
        Crée une figure unique qui courvre toutes les échéances (les échéances d'Arome 0.025° 
        sont au pas de temps horaire), renvoie et sauvegarde le diagramme."""
        print("début")
        self.type_de_carte = "histo_T2m"
        self.construire_Noms()
        
        compteur = 0

        if self.run == "03":
            tures = np.arange(40, dtype='f')
            ctures = np.arange(40)
        else:
            tures = np.arange(43, dtype='f')
            ctures = np.arange(43)
        
        for t_fichier in (6,12,18,24,30,36,42):

            nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2

            grbs = pygrib.open(nom_fichier)

            if t_fichier==6:
                echT=range(0,7,1)
            
            elif t_fichier==42:
                if self.run == "03":
                    echT=range(0,3,1)
                else:
                    echT=range(0,6,1)
            
            elif t_fichier in (12,18,24,30,36):
                echT=range(0,6,1)
            

            for echeance in echT:
                
                gt = grbs.select(shortName = '2t')[echeance]
                tt, lats, lons = gt.data(lat1=45.774,lat2=45.776,lon1=4.874,lon2=4.876)
                print(tt)
                print(compteur)
                print(lats)
                print(lons)
                tures[compteur] = tt - 273.15
                ctures[compteur]

                if self.verification == 1:
                    print(gt)

                del(gt)
                del(tt)

                compteur=compteur+1
                
            grbs.close()
            
        if self.run == "03":
            tx = np.arange(40, dtype='f')
            tn = np.arange(40, dtype='f')
            tmoy = np.arange(40, dtype='f')
        
            for r in range(0,40,1):
                tx[r] = tures.max()
                tn[r] = tures.min()
                tmoy[r] = tures.mean()
        else:
            tx = np.arange(43, dtype='f')
            tn = np.arange(43, dtype='f')
            tmoy = np.arange(43, dtype='f')
        
            for r in range(0,43,1):
                tx[r] = tures.max()
                tn[r] = tures.min()
                tmoy[r] = tures.mean()
        
        fig,aa = plt.subplots()
        aa = plt.plot(ctures,tures)
        amx = plt.plot(ctures,tx,'--',color='red')
        ami = plt.plot(ctures,tn,'--',color='blue')
        amo = plt.plot(ctures,tmoy,'--',color='grey')
        plt.ylabel('T2m prévue (°C)')
        plt.xlabel('Échéances (heures)')
        plt.title(self.titre_0)
        
        #if self.verification == 1:
        #plt.show()
        plt.grid()
        fig.savefig(self.nom_0,dpi=300)
        
        plt.close()

    def histogramme_Vent10m(self):
        """Renvoie un diagramme du vent à 10m (en moyenne et en rafale) prévu par Arome 0.025°.
        Crée une figure unique qui courvre toutes les échéances (les échéances d'Arome 0.025° 
        sont au pas de temps horaire), renvoie et sauvegarde le diagramme."""
        
        self.type_de_carte = "histo_Vent10m"
        self.construire_Noms()
        
        compteur = 0
        if self.run == "03":
            tures = np.arange(40, dtype='f')
            ff = np.arange(40, dtype='f')
            ctures = np.arange(40)
        else:
            tures = np.arange(43, dtype='f')
            ff = np.arange(43, dtype='f')
            ctures = np.arange(43)
        
        for t_fichier in (6,12,18,24,30,36,42):

            nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
            if self.verification == 1:
                print(nom_fichier)
            grbs = pygrib.open(nom_fichier)

            if t_fichier==6:
                echT=range(0,7,1)

            elif t_fichier==42:
                if self.run == "03":
                    echT=range(0,3,1)
                else:
                    echT=range(0,6,1)

            elif t_fichier in (12,18,24,30,36):
                echT=range(0,6,1)

            for echeance in echT:

                gt = grbs.select(shortName = '10si')[echeance]

                if compteur == 0:
                    tt2 = 0
                elif t_fichier == 6 and echeance > 0:
                    gt2 = grbs.select(shortName = 'gust')[echeance-1]
                    tt2, lats, lons = gt2.data(lat1=45.774,lat2=45.776,lon1=4.874,lon2=4.876)
                else:
                    gt2 = grbs.select(shortName = 'gust')[echeance]
                    tt2, lats, lons = gt2.data(lat1=45.774,lat2=45.776,lon1=4.874,lon2=4.876)
                
                if self.verification == 1:
                    print(gt)
                
                if compteur != 0 and self.verification == 1:
                    print(gt2)

                tt, lats, lons = gt.data(lat1=45.774,lat2=45.776,lon1=4.874,lon2=4.876)
                print("compteur: ",compteur)
                print("vent moyen: ",tt)
                print("FF: ",tt2)
                tures[compteur] = tt
                ff[compteur] = tt2

                ctures[compteur] = compteur                

                del(gt)
                if compteur > 0:
                    del(gt2)
                del(tt)

                compteur=compteur+1
        
            grbs.close()
        
        aa,bb = plt.subplots()
        
        aa = plt.plot(ctures,tures)
        bb = plt.plot(ctures,ff,"--",color='red')
        plt.ylabel('Vent à 10m moyen et ff')
        plt.xlabel('Échéances (heures)')
        plt.title(self.titre_0)
        
        plt.grid()
        
        plt.savefig(self.nom_0,dpi=300)
        
        #if self.verification == 1:
        #plt.show()
            
        plt.close()
        
    def histogramme_Precips(self):
        """Renvoie un diagramme de la lame d'eau horaire et du cumul prévu par Arome 0.025°.
        Crée une figure unique qui courvre toutes les échéances (les échéances d'Arome 0.025° 
        sont au pas de temps horaire), renvoie et sauvegarde le diagramme."""
        
        self.type_de_carte = "histo_Precips"
        self.construire_Noms()
        
        compteur = 0
        
        if self.run == "03":
            tp = np.arange(39, dtype='f')
            cumul = np.arange(39, dtype='f')
            ctp = np.arange(39)
        else:
            tp = np.arange(42, dtype='f')
            cumul = np.arange(42, dtype='f')
            ctp = np.arange(42)
        for t_fichier in (6,12,18,24,30,36,42):

            nom_fichier = self.nom_fichier_1 + str(t_fichier) + self.nom_fichier_2
            grbs = pygrib.open(nom_fichier)

            if t_fichier==6:
                echT=range(0,6,1)
            elif t_fichier==42:
                if self.run == "03":
                    echT=range(0,3,1)
                else:
                    echT=range(0,6,1)
            elif t_fichier in (12,18,24,30,36):
                echT=range(0,6,1)

            for echeance in echT:
                
                gt = grbs.select(shortName = 'tp')[echeance]
                print("Champ: ", gt.shortName, "    Validité: ", gt.validityDate, " à ",gt.validityTime)
                
                if compteur == 0:
                    
                    tt0 = 0
                    tta, lats, lons = gt.data(lat1=45.774,lat2=45.776,lon1=4.874,lon2=4.876)
                    print("compteur: ",compteur)
                    print("tta: ",tta)
                    print(lats,lons)
                    if tta > 0.1:
                        tt1 = tta
                    elif tta <= 0.1:
                        tt1 = 0
                else:
                    tt0 = tt1
                    tt1, lats, lons = gt.data(lat1=45.774,lat2=45.776,lon1=4.874,lon2=4.876)
                    print("compteur: ",compteur)
                    print("tt1: ",tt1)
                    print(lats,lons)
                    if self.verification == 1:
                        print(tt1)
                    
                del(gt)
                
                #print("tt1 :",tt)
                seuil_trace_pluie = tt1 - tt0
                print("seuil trace pluie: ",seuil_trace_pluie)
                
                if tt1 > 0.1:
                    cumul[compteur] = tt1
                elif tt1 <= 0.1:
                    cumul[compteur] = 0
                    
                if (seuil_trace_pluie > 0.1):
                    tp[compteur] = seuil_trace_pluie
                elif (seuil_trace_pluie <= 0.1):
                    tp[compteur] = 0
                    
                #print(tures)
                
                #StartDate = self.jour + "/" + self.mois + "/" + self.annee
                #pan = datetime.strptime(StartDate, "%d/%m/%Y")
                #pann = pan + timedelta(hours=int(self.run)) + timedelta(hours=compteur+1)
                #print(pan)
                #print(pann)
                #ctp.append(pann)
                   
                ctp[compteur] = compteur
                compteur=compteur+1
            
            grbs.close()
            
        if self.verification == 1:
            print(tp)
            print(len(ctp))
        
        aa, bb = plt.subplots()
        aa = plt.plot(ctp, cumul)
        bb = plt.bar(ctp,tp)

        #aa = plt.plot_date(ctp,cumul,color='blue')
        plt.ylabel("Lame d'eau (mm)")
        plt.xlabel('Échéances de prévision (heures)')
        
        plt.title(self.titre_0)
        
        plt.grid()
        
        plt.savefig(self.nom_0,dpi=300)
        
        #if self.verification == 1:
        #plt.show()
            
        plt.close()
