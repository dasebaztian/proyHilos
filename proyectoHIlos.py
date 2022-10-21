# Importar bibliotecas
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QImage
import requests
import threading


# Subclase QMainWindow
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi buscador")
        self.resize(6000, 2000)
        self.contenedor = QWidget()

        leftcolumna = QWidget()
        centercolumna = QWidget()
        rightcolumna = QWidget()

        self.lytPrincipal = QGridLayout()
        self.lblBusca = QLabel("Palabras de peliculas a buscar: ")

        self.lnedtTexto = QLineEdit()
        self.btnBusca = QPushButton("Buscar")
        self.btnBusca.clicked.connect(self.dividir_texto)
        self.lytPrincipal.addWidget(self.lblBusca, 0, 0)
        self.lytPrincipal.addWidget(self.lnedtTexto, 0, 1)
        self.lytPrincipal.addWidget(self.btnBusca, 0, 2)
        self.lytPrincipal.addWidget(leftcolumna, 1, 0)
        self.lytPrincipal.addWidget(centercolumna, 1, 1)
        self.lytPrincipal.addWidget(rightcolumna, 1, 2)
        self.contenedor.setLayout(self.lytPrincipal)
        self.setCentralWidget(self.contenedor)

    def dividir_texto(self):
        palabras = []
        lista = self.lnedtTexto.text()
        for palabras in lista:
            palabras = lista.split(",")
        print(palabras)
        for i in palabras:
            self.get_peliculas(i)

    def get_peliculas(self, palabra):
        url_servicio = "http://clandestina-hds.com:80/movies/title?search="
        r = requests.get(url_servicio + palabra)
        peliculas_data = r.json()
        index = 0
        limit = 3
        for pelicula in peliculas_data['results']:
            print("La pelicula de nombre: {} \n Tiene una URL de imagen: {}".format(pelicula['title'],
                                                                                    pelicula["image"]))
            self.mostrarimagenes(pelicula["image"])
            index = index + 1
            if index == limit:
                break

    def mostrarimagenes(self, url_image):
        image = QImage()
        image.loadFromData(requests.get(url_image).content)
        pixi = QPixmap.fromImage(image).scaled(150, 150)
        image_label = QLabel()
        image_label.setPixmap(QPixmap(pixi))

        image_label.show()
        self.lytPrincipal.addWidget(image_label)
        self.contenedor.setLayout(self.lytPrincipal)
        self.setCentralWidget(self.contenedor)


app = QApplication([])
window = VentanaPrincipal()
window.show()

app.exec_()
