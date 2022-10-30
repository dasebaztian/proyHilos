# Importar bibliotecas
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel, \
     QVBoxLayout, QTextEdit
from PyQt5.QtGui import QPixmap, QImage
import requests
import threading


# Subclase QMainWindow
def custom_hook(args):
    print(f'Thread failed: {args.exc_value}')


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi buscador")
        self.resize(600, 200)
        self.contenedor = QWidget()
        self.lyt_Images_Left = QVBoxLayout()
        self.lyt_Images_Center = QVBoxLayout()
        self.lyt_Images_Right = QVBoxLayout()
        self.lytPrincipal = QGridLayout()
        self.lblBusca = QLabel("Palabras de películas a buscar: ")
        self.inlineText = QLineEdit()
        self.btnBusca = QPushButton("Buscar")
        self.btnBusca.clicked.connect(self.dividir_texto)
        self.lytPrincipal.addWidget(self.lblBusca, 0, 0)
        self.lytPrincipal.addWidget(self.inlineText, 0, 1)
        self.lytPrincipal.addWidget(self.btnBusca, 0, 2)
        self.lytPrincipal.addLayout(self.lyt_Images_Left, 1, 0)
        self.lytPrincipal.addLayout(self.lyt_Images_Center, 1, 1)
        self.lytPrincipal.addLayout(self.lyt_Images_Right, 1, 2)
        self.contenedor.setLayout(self.lytPrincipal)
        self.setCentralWidget(self.contenedor)

    def dividir_texto(self):
        thread_lst = []
        palabras = []
        index = 0
        lista = self.inlineText.text()
        for palabras in lista:
            palabras = lista.split(",")
        for i in palabras:
            self.get_movies(i, index)
            index += 3

        threading.excepthook = custom_hook
        # thread_lst = [threading.Thread(target=self.get_movies, args=(k, index)) for k in palabras]
        # for i in thread_lst:
        #     i.start()
        #     index += 3
        #     print("Start")
        # for i in thread_lst:
        #     i.join()
        #     print("Return")
        print(thread_lst)
        self.resize(850, 800)

    def get_movies(self, palabra, index):
        url_servicio = "http://clandestina-hds.com:80/movies/title?search="
        r = requests.get(url_servicio + palabra)
        movies_data = r.json()
        data_short = movies_data['results'][:3]
        image = QImage()
        image_label = QLabel()
        for movie in data_short:
            print("La película de nombre: {} \n Tiene una URL de imagen: {}".format(movie['title'],
                                                                                    movie["image"]))
            image.loadFromData(requests.get(movie['image']).content)
            pixi = QPixmap.fromImage(image).scaled(200, 200)
            image_label.setPixmap(QPixmap(pixi))
            image_label.show()
            info_movie = QTextEdit("Resumen: " + movie['plot'])
            info_movie.setReadOnly(1)
            if 0 <= index < 3:
                self.lyt_Images_Left.addWidget(image_label)
                self.lyt_Images_Left.addWidget(info_movie)
            if 3 <= index < 6:
                self.lyt_Images_Center.addWidget(image_label)
                self.lyt_Images_Center.addWidget(info_movie)
            if index >= 6:
                self.lyt_Images_Right.addWidget(image_label)
                self.lyt_Images_Center.addWidget(info_movie)
        print(index)
        self.setCentralWidget(self.contenedor)


app = QApplication([])
window = VentanaPrincipal()
window.show()

app.exec_()
