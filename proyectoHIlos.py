# Importar bibliotecas
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QImage
import requests


# Subclase QMainWindow
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        palabrasabuscar = []
        super().__init__()
        self.setWindowTitle("Mi buscador")
        self.resize(600, 200)
        contenedor = QWidget()

        leftcolumna = QLineEdit()
        centercolumna = QLineEdit()
        rightcolumna = QLineEdit()

        lytPrincipal = QGridLayout()
        lblBusca = QLabel("Palabras de peliculas a buscar: ")

        self.lnedtTexto = QLineEdit()
        btnBusca = QPushButton("Buscar")
        btnBusca.clicked.connect(self.dividirTexto)

        lytPrincipal.addWidget(lblBusca, 0, 0)
        lytPrincipal.addWidget(self.lnedtTexto, 0, 1)
        lytPrincipal.addWidget(btnBusca, 0, 2)
        lytPrincipal.addWidget(leftcolumna, 1, 0)
        lytPrincipal.addWidget(centercolumna, 1, 1)
        lytPrincipal.addWidget(rightcolumna, 1, 2)

        contenedor.setLayout(lytPrincipal)
        self.setCentralWidget(contenedor)


    def dividirTexto(self):
        palabras = []
        lista = self.lnedtTexto.text()
        for palabras in lista:
            palabras = lista.split(",")
        self.get_peliculas(palabras)


    def get_peliculas(self, lista):
        url_servicio = "http://clandestina-hds.com:8090/movies/title?search="
        for i in lista:
            r = requests.get(url_servicio+i)
            peliculas_data = r.json()
            for pelicula in peliculas_data['results']:
                print("La pelicula de nombre: {} \n Tiene una URL de imagen: {}".format(pelicula['title'], pelicula["image"]))
                return pelicula["image"]



    def mostrarimagenes(self):
        url_image = "http://clandestina-hds.com:8090/movies/title?search="

        image = QImage()
        image.loadFromData(requests.get(url_image).content)
        image_label = QLabel()
        pixmap = QPixmap(image)
        pixmap2 = pixmap.scaledToWidth(500)
        image_label.setPixmap(pixmap2)
        image_label.show()


app = QApplication([])
window = VentanaPrincipal()
window.show()

app.exec_()
