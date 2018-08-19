# Lumet v0.6

## Sources des fichiers
Directement sur le site des données publiques de Météo-France:

https://donneespubliques.meteofrance.fr/

Les données Arome 0.01° et 0.025° sont disponibles dans «Modèles et données de prévisions»/«Données de modèle atmosphérique à aire limitée à haute résolution».

https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=131&id_rubrique=51

Un document détaille les données contenues dans les différents fichiers proposés.

Sur le site des données publiques, téléchargez toutes les échéances de type Arome 0.025° SP1 et IP5, vous obtenez des fichiers nommés, par exemple:
    
    AROME_0.025_IP5_00H06H_201806240300.grib2
    
    AROME_0.025_IP5_13H18H_201806240300.grib2

Que vous renommerez en:
    
    AROME_0.025_IP5_6H_201806240300.grib2
    
    AROME_0.025_IP5_18H_201806240300.grib2
    
## Organisation et exécution

Le mieux serait de créer un répertoire pour que ce soit plus facile de vous y retrouver.

Toutes les commandes doivent être lancées dans ce répertoire, commencez donc par:

    cd /chemin_vers_mon_répertoire/mon_répertoire/
    
Tout le code de ce projet est en python3, pour l'éxécuter il faut donc avoir python3 installé sur votre machine et lancer:
    python3 lumet_v_0_6_main.py

Une interface graphique devrait se lancer en quelques secondes et vous permettre d'afficher et de tracer différentes cartes.

### Données Arome 0.025°

Créez un nouveau répertoire dans votre répertoire que vous appellerez "Aro_00025", dans ce nouveau répertoire, créez en encore un autre au format jourmoisannée (par exemple pour le 24 juin 2018 sera 24062018).

    mkdir ./Aro_00025/
    mkdir ./Aro_00025/24062018
    
Stockez les fichiers de données Météo-France que vous avez renommés dans ce répertoire.

Pour faire des gifs avec vos cartes et réduire le poids des histogrammes, exécutez cela dans le répertoire ou sont stockées vos données Météo-France:

    mv ./histo_T2m* ./histo_T2m.png && mv ./histo_Vent10m* ./histo_vent10m.png && mv ./histo_DSW* ./histo_DSW.png && mv ./histo_precips* ./histo_precips.png && convert -scale 800x histo_T2m.png histo_T2m.png && convert -scale 800x histo_precips.png histo_precips.png && convert -scale 800x histo_DSW.png histo_DSW.png && convert -scale 800x histo_vent10m.png histo_vent10m.png && convert -scale 935x -delay 100 DSW_A*.png anim_DSW.gif && convert -scale 935x -delay 100 Precips_A*.png anim_Precips.gif && convert -scale 935x -delay 100 T2m_A*.png anim_T2m.gif && convert -scale 935x -delay 100 DSW_zoom*.png anim_DSW_zoom.gif && convert -scale 935x -delay 100 Precips_zoom*.png anim_Precips_zoom.gif && convert -scale 935x -delay 100 T2m_zoom*.png anim_T2m_zoom.gif && convert -scale 935x -delay 100 Z15_pvu_T*.png anim_Z15_pvu_TPW850.gif && convert -scale 935x -delay 100 Z15_pvu_J*.png anim_Z15_pvu_Jet.gif

### Données Arpege 0.1°

Créez un nouveau répertoire dans votre répertoire que vous appellerez "Arp_01", dans ce nouveau répertoire, créez en encore un autre au format jourmoisannée (par exemple pour le 24 juin 2018 sera 24062018).

    mkdir ./Arp_01/
    mkdir ./Arp_01/24062018
    
Stockez les fichiers de données Météo-France que vous avez renommés dans ce répertoire.

Pour faire des gifs avec vos cartes et réduire le poids des histogrammes, exécutez cela dans le répertoire ou sont stockées vos données Météo-France:

    convert -scale 935x -delay 80 DSW_A*.png anim_DSW.gif && convert -scale 935x -delay 80 DSW_zoom_1*.png anim_DSW_zoom_1.gif && convert -scale 935x -delay 80 DSW_zoom_2*.png anim_DSW_zoom_2.gif && convert -scale 935x -delay 80 DSW_zoom_3*.png anim_DSW_zoom_3.gif && convert -scale 935x -delay 80 T2m_A*.png anim_T2m.gif && convert -scale 935x -delay 80 T2m_zoom_1*.png anim_T2m_zoom_1.gif && convert -scale 935x -delay 80 T2m_zoom_2*.png anim_T2m_zoom_2.gif && convert -scale 935x -delay 80 T2m_zoom_3*.png anim_T2m_zoom_3.gif && convert -scale 935x -delay 80 Precips_A*.png anim_Precips.gif && convert -scale 935x -delay 80 Precips_zoom_1*.png anim_Precips_zoom_1.gif && convert -scale 935x -delay 80 Precips_zoom_2*.png anim_Precips_zoom_2.gif && convert -scale 935x -delay 80 Precips_zoom_3*.png anim_Precips_zoom_3.gif&& convert -scale 935x -delay 80 Pmer_A*.png anim_Pmer.gif && convert -scale 935x -delay 80 Pmer_zoom_1*.png anim_Pmer_zoom_1.gif && convert -scale 935x -delay 80 Pmer_zoom_2*.png anim_Pmer_zoom_2.gif && convert -scale 935x -delay 80 Pmer_zoom_3*.png anim_Pmer_zoom_3.gif

Vous trouverez les figures sorties quotidiennement de ce code sur mon site perso dont vous trouverez l'adresse avec mon compte courriel/xmpp.

Les codes sont placés sous licence GPL, copyleft eiua. 

Les données brutes des fichiers Météo-France Arome et Arpège sont sous license d'état Étalab (https://www.etalab.gouv.fr/wp-content/uploads/2014/05/Licence_Ouverte.pdf), source Météo-France.
