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

class Aro_0025_Cartes():
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
        
        ax.plot([4.875,4.8148,5.7242],[45.775,45.1896,45.1721], 'bo',color="red", markersize=0.5,transform=ccrs.PlateCarree())
        
        if self.zoom == 1:
            ax.set_extent([lonn, lonx, latn, latx])
        else:
            ax.set_extent([lonn, lonx, latn + 0.5 , latx])
            
        return f,ax
        #return ax
        
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
    
    def TPW850_Z15(self):
        """Renvoie les cartes du géopotentiel au niveau Z1.5pvu associée à la température potentielle 
        pseudo-adiabatique au niveau 850hPa (TPw850hPa)  prévues par Arome 0.025°.
        Le niveau Z1.5pvu correspond à la tropopause.
        Permet de regarder le forçage d'altitude (Z1.5pvu) et l'énergie disponible 
        dans les basses couches (TPw850hPa).
        Crée une figure par échéance donc une par heure, renvoie et sauvegarde l'intégralité des cartes."""
        
        self.type_de_carte = "TPW850_Z1.5pvu"
        #self.type_de_carte = "T2m"
        self.construire_Noms()
        
        print("début charger tout")
        
        #tt = []
        #ttt = []
        tt, pvu, lons , lats = self.charger_Tout()
        #tt = []
        #ttt = []
        #tx = []
        #tn = []
        #ts = []
        
        print("fin charger tout")
        
        """for ii in range(0,39,1):
            
            print("ii: ",ii)
            print(type(tt[ii]))
            print("min: ",tt[ii].min())
            print("max: ",tt[ii].max())
            print("moy: ",tt[ii].mean())
            print("écart type: ",tt[ii].std())
            cc.append(ii)
            ttt.append(tt[ii].min())
            tx.append(tt[ii].max())
            tn.append(tt[ii].mean())
            ts.append(tt[ii])
            
            
        fig,aa = plt.subplots()
        aa = plt.plot(cc,ts)
        amx = plt.plot(cc,tx,'--',color='red')
        amo = plt.plot(cc,tn,'--',color='grey')
        amm = plt.plot(cc,ttt,'--',color='blue')
        plt.ylabel('T2m prévue (°C)')
        plt.xlabel('Échéances (heures)')
        plt.title(self.titre_0)
        
        #if self.verification == 1:
        #plt.show()
        plt.grid()
        fig.savefig(self.nom_0,dpi=300)
        
        plt.close()"""
            
        for ii in range(0,40,1):
        
            if ii == 0:
                lon_0 = lons.mean()
                lat_0 = lats.mean()
                lonn = lons.min()
                latn = lats.min()
                lonx = lons.max()
                latx = lats.max()
                
            f, ax = self.dessiner_fond_carte(lon_0,lat_0,lonn,latn,lonx,latx)

            origin='lower'
            levels = np.arange(-40,44,4)
            levels_pvu = np.arange(0,12000,1000)

            cs = ax.pcolormesh(lons, lats, tt[ii], vmin=-12, vmax=26,cmap='nipy_spectral',transform=ccrs.PlateCarree())
            cs1 = ax.contour(lons, lats, tt[ii], levels,transform=ccrs.PlateCarree(),
                          colors=('k'),
                          linewidths=(0.2),linestyles='dashed',
                          origin=origin)
            cs_pvu = ax.contour(lons, lats, pvu[ii], levels_pvu,transform=ccrs.PlateCarree(),
                          colors=('k'),
                          linewidths=(0.3),
                          origin=origin)
            csb = plt.colorbar(cs)
            csb.set_label("Theta'w 850hPa (°C)")

            lala_pvu = plt.clabel(cs_pvu, fontsize=4, fmt='%1.0f')
            lala_tpw = plt.clabel(cs1, fontsize=4, fmt='%1.0f')


            if ii < 10:
                titre = self.titre_0
                nom = self.nom_0 + str(ii)+'H_tt.png'
            else:
                titre = self.titre_10
                nom = self.nom_10 + str(ii)+'H_tt.png'

            plt.title(titre)
            
            ma_dpi = 146
            plt.savefig(nom, dpi=ma_dpi)

            #if self.verification == 1:
            #plt.show()

            plt.close()
        
    def T2m(self):
        """Renvoie les cartes du géopotentiel au niveau Z1.5pvu associée à la température potentielle 
        pseudo-adiabatique au niveau 850hPa (TPw850hPa)  prévues par Arome 0.025°.
        Le niveau Z1.5pvu correspond à la tropopause.
        Permet de regarder le forçage d'altitude (Z1.5pvu) et l'énergie disponible 
        dans les basses couches (TPw850hPa).
        Crée une figure par échéance donc une par heure, renvoie et sauvegarde l'intégralité des cartes."""
        start_program = time.time()
        #self.type_de_carte = "TPW850_Z1.5pvu"
        self.type_de_carte = "T2m"
        self.construire_Noms()
        
        print("début charger tout")
        
        #tt = []
        #ttt = []
        images = []
        fig_pour_anim = plt.figure()
        tt, lons , lats = self.charger_Tout()
        #tt = []
        #ttt = []
        #tx = []
        #tn = []
        #ts = []
        
        print("fin charger tout")
        
        """for ii in range(0,39,1):
            
            print("ii: ",ii)
            print(type(tt[ii]))
            print("min: ",tt[ii].min())
            print("max: ",tt[ii].max())
            print("moy: ",tt[ii].mean())
            print("écart type: ",tt[ii].std())
            cc.append(ii)
            ttt.append(tt[ii].min())
            tx.append(tt[ii].max())
            tn.append(tt[ii].mean())
            ts.append(tt[ii])
            
            
        fig,aa = plt.subplots()
        aa = plt.plot(cc,ts)
        amx = plt.plot(cc,tx,'--',color='red')
        amo = plt.plot(cc,tn,'--',color='grey')
        amm = plt.plot(cc,ttt,'--',color='blue')
        plt.ylabel('T2m prévue (°C)')
        plt.xlabel('Échéances (heures)')
        plt.title(self.titre_0)
        
        #if self.verification == 1:
        #plt.show()
        plt.grid()
        fig.savefig(self.nom_0,dpi=300)
        
        plt.close()"""
            
        for ii in range(0,40,1):
            start = time.time()
            print("-----------------------------")
            print(ii)
            if ii == 0:
                lon_0 = lons.mean()
                lat_0 = lats.mean()
                lonn = lons.min()
                latn = lats.min()
                lonx = lons.max()
                latx = lats.max()
                
            f, ax = self.dessiner_fond_carte(lon_0,lat_0,lonn,latn,lonx,latx)
            print("fin dessiner fond carte")
            origin='lower'
            levels = np.arange(-40,48,4)
            
            cs = ax.pcolormesh(lons, lats, tt[ii], vmin=-34, vmax=44,cmap='nipy_spectral',transform=ccrs.PlateCarree())
            #print("fin colormesh")
            cs1 = ax.contour(lons, lats, tt[ii], levels,transform=ccrs.PlateCarree(),
                          colors=('k'),
                          linewidths=(0.2),linestyles='dashed',
                          origin=origin)
            #print("fin contour")              
            csb = plt.colorbar(cs)
            #print("fin colorbar")
            csb.set_label("(°C)")
            #print("fin label 1")
            lala_tpw = plt.clabel(cs1, fontsize=4, fmt='%1.0f')
            #print("fin label 2")


            if ii < 10:
                titre = self.titre_0
                nom = self.nom_0 + str(ii)+'H_tt.png'
            else:
                titre = self.titre_10
                nom = self.nom_10 + str(ii)+'H_tt.png'

            tit = plt.title(titre)
            print("fin titre")
            ma_dpi = 300
            plt.savefig(nom, dpi=ma_dpi)
            images.append(f)
            print("fin save")
            print("Total time taken to save fig ",ii, "is", time.time()-start)
            
            
            
            #if self.verification == 1:
            #plt.show()

            plt.close()
        
        print("sortie boucle")
        #line_anim = ArtistAnimation(fig_pour_anim, images, interval=80)
        print("fin list anim")
        
        #line_anim.save('my_animation.mp4',fps=10,writer = 'ffmpeg')
        print("fin anim sauv")
        #plt.show()   
        end_program = time.time()
        print("Total time to complete program is :", end_program - start_program)
