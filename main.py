import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from gas_main_window import Ui_MainWindow

import gas


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_window = Ui_MainWindow()
        self.ui_window.setupUi(self)

        # Menu
        self.ui_window.actionVersion.triggered.connect(self.about)
        self.ui_window.actionSalir.triggered.connect(self.close)

        # Variables
        self.provinces = {}
        self.cities = {}
        self.stations = []

        # Comboboxes
        self.ui_window.comunidadCB.addItem("Seleccione CCAA")
        self.ui_window.comunidadCB.model().item(0).setEnabled(False)
        self.ui_window.comunidadCB.setCurrentIndex(0)
        self.ui_window.comunidadCB.currentTextChanged.connect(self.ccaa_selected)
        self.comunidades = gas.get_comunidades()

        if self.comunidades == {}:
            self.statusBar().showMessage("Error de conexión, salga de la aplicación y reinténtelo")
        else:
            for comunidad in self.comunidades:
                self.ui_window.comunidadCB.addItem(comunidad)

        self.ui_window.provinciaCB.addItem("Seleccione Provincia")
        self.ui_window.provinciaCB.setEnabled(False)
        self.ui_window.provinciaCB.model().item(0).setEnabled(False)
        self.ui_window.provinciaCB.setCurrentIndex(0)
        self.ui_window.provinciaCB.currentTextChanged.connect(self.province_selected)

        self.ui_window.municipioCB.addItem("Seleccione Municipio")
        self.ui_window.municipioCB.setEnabled(False)
        self.ui_window.municipioCB.model().item(0).setEnabled(False)
        self.ui_window.municipioCB.setCurrentIndex(0)
        self.ui_window.municipioCB.currentTextChanged.connect(self.city_selected)

        self.ui_window.direccionCB.addItem("Seleccione Gasolinera")
        self.ui_window.direccionCB.setEnabled(False)
        self.ui_window.direccionCB.model().item(0).setEnabled(False)
        self.ui_window.direccionCB.setCurrentIndex(0)
        self.ui_window.direccionCB.currentTextChanged.connect(self.station_selected)

    def ccaa_selected(self):
        print(self.ui_window.comunidadCB.currentText())
        self.ui_window.provinciaCB.clear()
        self.ui_window.municipioCB.setEnabled(False)

        self.provinces = \
            gas.get_provincias(self.comunidades.get(self.ui_window.comunidadCB.currentText()))
        self.ui_window.provinciaCB.addItem("Seleccione Provincia")
        self.ui_window.municipioCB.addItem("Seleccione Municipio")

        for province in self.provinces:
            self.ui_window.provinciaCB.addItem(province)

        self.ui_window.provinciaCB.setEnabled(True)

    def province_selected(self):
        print("Provincia: " + self.ui_window.provinciaCB.currentText())
        self.ui_window.municipioCB.clear()

        if self.ui_window.provinciaCB.currentIndex() != -1 and self.ui_window.provinciaCB.currentIndex() != 0:
            self.cities = gas.get_municipios(self.provinces.get(self.ui_window.provinciaCB.currentText()))
            self.ui_window.municipioCB.addItem("Seleccione Municipio")

            for city in self.cities:
                self.ui_window.municipioCB.addItem(city)

            self.ui_window.municipioCB.setEnabled(True)

    def city_selected(self):
        print("Municipio: " + self.ui_window.municipioCB.currentText())
        self.ui_window.direccionCB.clear()

        if self.ui_window.municipioCB.currentIndex() != -1 and self.ui_window.municipioCB.currentIndex() != 0:
            self.stations = gas.get_estaciones_por_ciudad(
                self.cities.get(self.ui_window.municipioCB.currentText()))
            self.ui_window.direccionCB.addItem("Seleccione Gasolinera")

            for station in self.stations:
                print(station)
                self.ui_window.direccionCB\
                    .addItem(str(station['Rótulo']) + " - " + str(station['Dirección']))

            self.ui_window.direccionCB.setEnabled(True)

    def station_selected(self):
        self.reset_displays()
        if self.ui_window.direccionCB.currentIndex() != -1 and self.ui_window.direccionCB.currentIndex() != 0:
            station = self.stations[self.ui_window.direccionCB.currentIndex() - 1]
            if station['Precio Gasolina 95 E5'] != '':
                self.ui_window.sp95E5LCD.display(float(station['Precio Gasolina 95 E5'].replace(',', '.')))

            if station['Precio Gasolina 98 E5'] != '':
                self.ui_window.sp98E5LCD.display(float(station['Precio Gasolina 98 E5'].replace(',', '.')))

            if station['Precio Gasolina 95 E5 Premium'] != '':
                self.ui_window.sp95E5PremiumLCD.display(
                    float(station['Precio Gasolina 95 E5 Premium'].replace(',', '.')))

            if station['Precio Gasolina 95 E10'] != '':
                self.ui_window.sp95E10LCD.display(
                    float(station['Precio Gasolina 95 E10'].replace(',', '.')))

            if station['Precio Gasolina 98 E10'] != '':
                self.ui_window.sp98E10LCD.display(
                    float(station['Precio Gasolina 98 E10'].replace(',', '.')))

            if station['Precio Gasoleo A'] != '':
                self.ui_window.gasoleoALCD.display(float(station['Precio Gasoleo A'].replace(',', '.')))

            if station['Precio Gasoleo B'] != '':
                self.ui_window.gasoleoBLCD.display(float(station['Precio Gasoleo B'].replace(',', '.')))

            if station['Precio Gasoleo Premium'] != '':
                self.ui_window.gasoleoPremiumLCD.display(
                    float(station['Precio Gasoleo Premium'].replace(',', '.')))

            if station['Precio Biodiesel'] != '':
                self.ui_window.biodieselLCD.display(float(station['Precio Biodiesel'].replace(',', '.')))

            if station['Precio Bioetanol'] != '':
                self.ui_window.bioetanolLCD.display(float(station['Precio Bioetanol'].replace(',', '.')))

            if station['Precio Gas Natural Comprimido'] != '':
                self.ui_window.gncLCD.display(
                    float(station['Precio Gas Natural Comprimido'].replace(',', '.')))

            if station['Precio Gas Natural Licuado'] != '':
                self.ui_window.gnlLCD.display(
                    float(station['Precio Gas Natural Licuado'].replace(',', '.')))

            if station['Precio Gases licuados del petróleo'] != '':
                self.ui_window.glpLCD.display(
                    float(station['Precio Gases licuados del petróleo'].replace(',', '.')))

            if station['Precio Hidrogeno'] != '':
                self.ui_window.hidrogenoLCD.display(float(station['Precio Hidrogeno'].replace(',', '.')))

    def reset_displays(self):
        self.ui_window.sp95E5LCD.display(0.0)
        self.ui_window.sp98E5LCD.display(0.0)
        self.ui_window.sp95E10LCD.display(0.0)
        self.ui_window.sp95E5PremiumLCD.display(0.0)
        self.ui_window.sp98E10LCD.display(0.0)

        self.ui_window.gasoleoALCD.display(0.0)
        self.ui_window.gasoleoBLCD.display(0.0)
        self.ui_window.gasoleoPremiumLCD.display(0.0)

        self.ui_window.biodieselLCD.display(0.0)
        self.ui_window.bioetanolLCD.display(0.0)

        self.ui_window.gncLCD.display(0.0)
        self.ui_window.gnlLCD.display(0.0)
        self.ui_window.glpLCD.display(0.0)
        self.ui_window.hidrogenoLCD.display(0.0)

    @staticmethod
    def about():
        msg = QMessageBox()
        msg.setWindowTitle("Sobre esta aplicación")
        msg.setText("GasolinerasApp alpha")
        msg.exec_()

app = QtWidgets.QApplication([])
application = MainWindow()
application.show()
sys.exit(app.exec())
