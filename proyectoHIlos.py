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
        self.resize(6000, 2000)
        self.contenedor = QWidget()

        leftcolumna = QWidget()
        centercolumna = QWidget()
        rightcolumna = QWidget()

        self.lytPrincipal = QGridLayout()
        self.lblBusca = QLabel("Palabras de peliculas a buscar: ")

        self.lnedtTexto = QLineEdit()
        self.btnBusca = QPushButton("Buscar")
        self.btnBusca.clicked.connect(self.get_peliculas)

        self.lytPrincipal.addWidget(self.lblBusca, 0, 0)
        self.lytPrincipal.addWidget(self.lnedtTexto, 0, 1)
        self.lytPrincipal.addWidget(self.btnBusca, 0, 2)
        self.lytPrincipal.addWidget(leftcolumna, 1, 0)
        self.lytPrincipal.addWidget(centercolumna, 1, 1)
        self.lytPrincipal.addWidget(rightcolumna, 1, 2)

        self.contenedor.setLayout(self.lytPrincipal)
        self.setCentralWidget(self.contenedor)

    def get_peliculas(self):
        url_servicio = "http://clandestina-hds.com:8090/movies/title?search="
        palabras = []
        lista = self.lnedtTexto.text()
        for palabras in lista:
            palabras = lista.split(",")

        print(palabras)
        for i in palabras:
            r = requests.get(url_servicio + i)
            peliculas_data = r.json()
            for pelicula in peliculas_data['results']:
                print("La pelicula de nombre: {} \n Tiene una URL de imagen: {}".format(pelicula['title'],pelicula["image"]))
                self.mostrarimagenes(pelicula["image"])


    def mostrarimagenes(self, url_image):
        image = QImage()
        image.loadFromData(requests.get(url_image).content)
        image_label = QLabel()
        image_label.setPixmap(QPixmap(image))
        image_label.show()
        self.lytPrincipal.addWidget(image_label)
        self.contenedor.setLayout(self.lytPrincipal)
        self.setCentralWidget(self.contenedor)


app = QApplication([])
window = VentanaPrincipal()
window.show()

app.exec_()
