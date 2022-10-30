from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel, \
     QVBoxLayout, QTextEdit
from PyQt5.QtGui import QPixmap, QImage, QDesktopServices
from PyQt5.QtCore import QUrl
import requests
import threading


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
        palabras = []
        index = 0
        lista = self.inlineText.text()
        for palabras in lista:
            palabras = lista.split(",")
        #
        # Codigo sin hilos
        # for i in palabras:
        #     self.get_movies(i, index)
        #     index += 3

        threading.excepthook = custom_hook
        thread_lst = [threading.Thread(target=self.get_movies, args=(k, index)) for k in palabras]
        for i in thread_lst:
            i.start()
            index += 3
            print("Start")
        for i in thread_lst:
            i.join()
            print("Return")
        print(thread_lst)
        self.resize(750, 800)

    def get_movies(self, palabra, index):
        url_service_image = "http://clandestina-hds.com:80/movies/title?search="
        url_service_video = "https://clandestina-hds.com/movies/"
        data_total = requests.get(url_service_image + palabra)
        movies_data = data_total.json()
        data_short = movies_data['results'][:3]
        for movie in data_short:
            data_video = requests.get(url_service_video + movie['id'])
            data2_video = data_video.json()
            url_video = data2_video['trailer']['linkEmbed']
            image = Poster(movie['image'], url_video)
            info_movie = QTextEdit("Resumen: " + movie['plot'])
            info_movie.setReadOnly(1)
            if 0 <= index < 3:
                self.lyt_Images_Left.addWidget(image)
                self.lyt_Images_Left.addWidget(info_movie)
            if 3 <= index < 6:
                self.lyt_Images_Center.addWidget(image)
                self.lyt_Images_Center.addWidget(info_movie)
            if index >= 6:
                self.lyt_Images_Right.addWidget(image)
                self.lyt_Images_Right.addWidget(info_movie)
        print(index)
        self.setCentralWidget(self.contenedor)


class Poster(QLabel):
    image_url: str
    video_url: str

    def __init__(self, image_url: str, video_url: str):
        super().__init__()
        self.image_url = image_url
        self.video_url = video_url
        image = QImage()
        image.loadFromData(requests.get(self.image_url).content)
        pixmap = QPixmap(image)
        pixmap = pixmap.scaledToWidth(200)
        self.setPixmap(pixmap)

    def mouseDoubleClickEvent(self, event):
        if self.video_url is not None and self.video_url is not "":
            url = QUrl(self.video_url)
            QDesktopServices.openUrl(url)


app = QApplication([])
window = VentanaPrincipal()
window.show()

app.exec_()
