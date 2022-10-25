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
        self.resize(600, 200)
        self.contenedor = QWidget()
        self.lytPrincipal = QGridLayout()
        self.lblBusca = QLabel("Palabras de películas a buscar: ")
        self.inlineText = QLineEdit()
        self.btnBusca = QPushButton("Buscar")
        self.btnBusca.clicked.connect(self.dividir_texto)
        self.lytPrincipal.addWidget(self.lblBusca, 0, 0)
        self.lytPrincipal.addWidget(self.inlineText, 0, 1)
        self.lytPrincipal.addWidget(self.btnBusca, 0, 2)
        self.contenedor.setLayout(self.lytPrincipal)
        self.setCentralWidget(self.contenedor)

    def dividir_texto(self):
        thread_lst = []
        palabras = []
        lista = self.inlineText.text()
        for palabras in lista:
            palabras = lista.split(",")
        for i in palabras:
            self.get_movies(i)
            # thread_lst = [threading.Thread(target=self.get_movies, args=i)]
        print(thread_lst)

    def get_movies(self, palabra):
        url_servicio = "http://clandestina-hds.com:80/movies/title?search="
        r = requests.get(url_servicio + palabra)
        movies_data = r.json()
        data_short = movies_data['results'][:3]
        for movie in data_short:
            print("La película de nombre: {} \n Tiene una URL de imagen: {}".format(movie['title'],
                                                                                    movie["image"]))
            self.show_images(movie["image"])

    def show_images(self, url_image):
        image = QImage()
        image.loadFromData(requests.get(url_image).content)
        pixi = QPixmap.fromImage(image).scaled(350, 250)
        image_label = QLabel()
        image_label.setPixmap(QPixmap(pixi))
        image_label.show()
        self.lytPrincipal.addWidget(image_label)
        self.contenedor.setLayout(self.lytPrincipal)
        self.setCentralWidget(self.contenedor)
        self.resize(1000, 800)


app = QApplication([])
window = VentanaPrincipal()
window.show()

app.exec_()
