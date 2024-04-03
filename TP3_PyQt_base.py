import sys
import random
from PyQt5.QtWidgets import * 
from datetime import datetime
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pickle
from PyQt5.QtWidgets import QColorDialog




class myHisto:
    """Classe myHisto pour stocker l'histogramme"""

    def __init__(self):
        print('Méthode __init__()  de la classe myHisto')
        self.m_list = []
        self.m_size = 0
        self.m_max = 0

    def total(self):
        """Calcul de la population totale de l'histogramme"""
        total_population = 0
        for value in self.m_list:
            try:
                total_population += int(value)
            except ValueError:
                pass  # Ignore les valeurs qui ne peuvent pas être converties en int
        return total_population

        
        
class MyMainWindow(QMainWindow):
    """ Classe de l'application principale"""

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        # Attributs de la fenetre principale
        self.setGeometry(300, 300, 600, 450)
        self.titleInfo = "SEN"
        self.titleMainWindow = self.titleInfo + datetime.now().strftime("  %H:%M:%S") + ' | Res: ' + str(self.width()) + 'x' + str(self.height())
        self.setWindowTitle(self.titleMainWindow) 
        # Barre de status pour afficher les infos
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Zone d'informations, peut toujours servir")
        self.setMinimumSize(500 , 230)

        # Creation d'une instance de la classe myHisto
        self.mHisto = myHisto()

        self.colorIcon = QIcon()
        self.colorIcon.addPixmap(QPixmap(16, 16))
        self.colorIcon.pixmap(QSize(16, 16)).fill(Qt.red)

        self.painterColor = Qt.red

        # Activer la prise en charge du glisser-déposer
        self.setAcceptDrops(True)


        #mode d'affichage de base en Bar
        self.displayMode = "Bar"


        self.createActions()
        self.createMenus()

     # Surcharge de la méthode dragEnterEvent pour accepter les fichiers
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    # Surcharge de la méthode dropEvent pour gérer le glisser-déposer de fichiers
    def dropEvent(self, event):
        for url in event.mimeData().urls():
            filename = url.toLocalFile()
            self.statusBar.showMessage(f"Fichier glissé-déposé : {filename}")

            # Lire le fichier et affecter à la variable membre
            with open(filename, 'r') as file:
                self.mHisto.m_list.clear()  # Effacer les données précédentes
                for line in file:
                    self.mHisto.m_list.append(line.strip())

    
                self.update()

    def resizeEvent(self,event):
        self.titleMainWindow = self.titleInfo + datetime.now().strftime("  %H:%M:%S") + '| Res: ' + str(self.width()) + 'x' + str(self.height())
        self.setWindowTitle(self.titleMainWindow) 

    def createActions(self):
        """ Créer ici les actions d'item de menu ainsi que connexions signal/slot, à compléter"""
        self.openAct = QAction("&Open",self)
        self.openAct.setShortcut("Ctrl+O")
        self.openAct.triggered.connect(self.openFile)

        self.saveAct = QAction("&Save",self)
        self.saveAct.setShortcut("Ctrl+S")
        self.saveAct.triggered.connect(self.saveFile)

        self.restoreAct = QAction("&Restore",self)  
        self.restoreAct.setShortcut("Ctrl+Z")
        self.restoreAct.triggered.connect(self.restoredFile)

        self.byeAct = QAction("&Bye", self)
        self.byeAct.setShortcut("Ctrl+B")
        self.byeAct.triggered.connect(self.myExit)

        self.exitAct = QAction(" &Quit", self)
        self.exitAct.setShortcut("Ctrl+X")
        self.exitAct.triggered.connect(self.myExit)

        #menu display
        self.ClearAct = QAction("&Clear",self) 
        self.ClearAct.triggered.connect(self.clearFile)

        self.ColorAct = QAction("&Color",self)
        self.ColorAct.triggered.connect(self.selectColor) 


        #menu draw
        self.drawBarAct = QAction("&Bar", self)
        self.drawBarAct.triggered.connect(self.drawBar) 

        self.drawPieAct = QAction("&Pie", self)
        self.drawPieAct.triggered.connect(self.drawPie)
         

        

    def createMenus(self):
        """ Créer ici les menu et les items de menu, à compléter"""
        
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.exitAct)
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.restoreAct)
        fileMenu.addSeparator()  # Ajouter un séparateur
        fileMenu.addAction(self.byeAct)

        fileMenu2 = self.menuBar().addMenu("&Display")
        fileMenu2.addAction(self.ClearAct)
        fileMenu2.addAction(self.ColorAct)

        self.drawMenu = self.menuBar().addMenu("&Draw")
        self.drawMenu.addAction(self.drawBarAct)
        self.drawMenu.addAction(self.drawPieAct)



    def myExit(self):
        """ Slot associé à exitAct, instance de QAction, à compléter """
        self.statusBar.showMessage("Quit ...")
        QApplication.quit()

    def openFile(self):
    
        fileName, _ = QFileDialog.getOpenFileName(self,"Ouvrir un fichier", "", "Data Files (*.dat)",)
        if fileName:
            self.statusBar.showMessage("Histo- gram opened!")

        with open(fileName,'r') as file:
            for line in file:
                self.mHisto.m_list.append(line.strip())

            for i in range(len(self.mHisto.m_list)):
                if int(self.mHisto.m_list[i]) > self.mHisto.m_max:
                    self.mHisto.m_max = int(self.mHisto.m_list[i])
                    self.mHisto.m_size = len(self.mHisto.m_list)

        self.update()

    def paintEvent(self, event):
        """ Dessine les données dans la fenêtre principale """
        if not self.mHisto.m_list:
            self.statusBar.showMessage("Aucune donnée à tracer.")
            return

        data = [int(value) for value in self.mHisto.m_list]
        max_value = max(data)

        painter = QPainter(self)
        total_population = self.mHisto.total()
        painter.setRenderHint(QPainter.Antialiasing)

        # Définir le stylo (pen) en noir
        painter.setPen(QPen(QColor(0, 0, 0)))

        # Définir la brosse (brush) en rouge
        painter.setBrush(self.painterColor)
        

        bar_width = self.width() / len(data)

        if self.displayMode == "Bar":
            for i, value in enumerate(data):
                x = int(i * bar_width)
                bar_height = int((value / max_value) * self.height())
                y = self.height() - bar_height

                # Remplir le rectangle avec un fond rouge
                painter.fillRect(x, y, int(bar_width), bar_height, QColor(255, 0, 0))

                # Dessiner la bordure du rectangle en noir
                painter.drawRect(x, y, int(bar_width), bar_height)

        elif self.displayMode == "Pie":
            # Affichage de l'histogramme sous forme de camembert
            pie_size = min(self.width(), self.height())
            x = (self.width() - pie_size) // 2
            y = (self.height() - pie_size) // 2

            start_angle = 0
            for value in data:
                # Calculer l'angle pour chaque secteur proportionnel à la population du bin
                angle = (value / total_population) * 360

                # Dessiner le secteur avec une couleur aléatoire
                random_color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                painter.setBrush(random_color)
                painter.drawPie(x, y, pie_size, pie_size, int(start_angle * 16), int(angle * 16))

                start_angle += angle

        


    #code pour sauvegarder les paramettre dans un fichier
    def saveFile(self):
        save_path = 'saveHisto.bin' # Nom du fichier dans lequel vous voulez sauvegarder les données avec son chemin
        if not self.mHisto.m_list:
            self.statusBar.showMessage("Aucune donnée à sauvegarder.")
            return

        try:
            with open(save_path, 'wb') as file:
                pickle.dump(self.mHisto.m_list, file)
            self.statusBar.showMessage("Données sauvegardées dans 'saveHisto.bin'.")
        except Exception as e:
            self.statusBar.showMessage(f"Erreur lors de la sauvegarde : {str(e)}")

    
    def clearFile(self):
        self.mHisto.m_list.clear()
        self.statusBar.showMessage(" Histogram cleared!")
        self.update()

    #permet de charger les données sauvegarder
    def restoredFile(self):
        restore_path = 'saveHisto.bin' #Nom du fichier dans lequel vous voulez restaurer les données avec son chemin
        try:
            with open(restore_path, 'rb') as file:
                self.mHisto.m_list = pickle.load(file)
                self.mHisto.m_size = len(self.mHisto.m_list)
                self.mHisto.m_max = max(self.mHisto.m_list) if self.mHisto.m_list else 0
                self.statusBar.showMessage("Données restaurées depuis 'saveHisto.bin'.")
                self.update()
        except FileNotFoundError:
            self.statusBar.showMessage("Fichier 'saveHisto.bin' non trouvé.")
        except Exception as e:
            self.statusBar.showMessage(f"Erreur lors de la restauration : {str(e)}")

    #action a l'appui d'une touche
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self.mHisto.m_list = [random.randint(0, 99) for _ in range(10)]
            self.mHisto.m_size = len(self.mHisto.m_list)
            self.mHisto.m_max = max(self.mHisto.m_list) if self.mHisto.m_list else 0
            self.update()

    def selectColor(self):
        color = QColorDialog.getColor(self.painterColor, self)
        if color.isValid():
            self.painterColor = color  # Mettez à jour la couleur du pinceau avec la nouvelle couleur
            self.colorIcon.addPixmap(QPixmap(16, 16))
            self.colorIcon.pixmap(QSize(16, 16)).fill(color)
            self.ColorAct.setIcon(self.colorIcon)
            self.statusBar.showMessage("Color Change")
            self.update()

    def drawBar(self):
        self.displayMode = "Bar"
        self.setMinimumSize(500, 500) 
        self.update()

    def drawPie(self):
        self.displayMode = "Pie"
        self.setMinimumSize(500, 500)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyMainWindow()
    x = myHisto()
    w.show()
    app.exec_()
