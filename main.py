import sys
from PyQt5 import QtWidgets

from gas_main_window import Ui_MainWindow

import gas


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Variables
        self.provinces = {}
        self.cities = {}
        self.stations = []

        # Buttons
        self.ui.salirBtn.clicked.connect(self.close)

        # Comboboxes
        self.ui.comunidadCB.addItem("Seleccione CCAA")
        self.ui.comunidadCB.model().item(0).setEnabled(False)
        self.ui.comunidadCB.setCurrentIndex(0)
        self.ui.comunidadCB.currentTextChanged.connect(self.ccaa_selected)
        self.comunidades = gas.get_comunidades()

        if self.comunidades == {}:
            self.statusBar().showMessage("Error de conexión, salga de la aplicación y reinténtelo")
        else:
            for comunidad in self.comunidades:
                self.ui.comunidadCB.addItem(comunidad)

        self.ui.provinciaCB.addItem("Seleccione Provincia")
        self.ui.provinciaCB.setEnabled(False)
        self.ui.provinciaCB.model().item(0).setEnabled(False)
        self.ui.provinciaCB.setCurrentIndex(0)
        self.ui.provinciaCB.currentTextChanged.connect(self.province_selected)

        self.ui.municipioCB.addItem("Seleccione Municipio")
        self.ui.municipioCB.setEnabled(False)
        self.ui.municipioCB.model().item(0).setEnabled(False)
        self.ui.municipioCB.setCurrentIndex(0)
        self.ui.municipioCB.currentTextChanged.connect(self.city_selected)

        self.ui.direccionCB.addItem("Seleccione Gasolinera")
        self.ui.direccionCB.setEnabled(False)
        self.ui.direccionCB.model().item(0).setEnabled(False)
        self.ui.direccionCB.setCurrentIndex(0)
        self.ui.direccionCB.currentTextChanged.connect(self.station_selected)

    def ccaa_selected(self):
        print(self.ui.comunidadCB.currentText())
        self.ui.provinciaCB.clear()
        self.ui.municipioCB.setEnabled(False)

        self.provinces = \
            gas.get_provincias(self.comunidades.get(self.ui.comunidadCB.currentText()))
        self.ui.provinciaCB.addItem("Seleccione Provincia")
        self.ui.municipioCB.addItem("Seleccione Municipio")

        for province in self.provinces:
            self.ui.provinciaCB.addItem(province)

        self.ui.provinciaCB.setEnabled(True)

    def province_selected(self):
        print("Provincia: " + self.ui.provinciaCB.currentText())
        self.ui.municipioCB.clear()

        if self.ui.provinciaCB.currentIndex() != -1 and self.ui.provinciaCB.currentIndex() != 0:
            self.cities = gas.get_municipios(self.provinces.get(self.ui.provinciaCB.currentText()))
            self.ui.municipioCB.addItem("Seleccione Municipio")

            for city in self.cities:
                self.ui.municipioCB.addItem(city)

            self.ui.municipioCB.setEnabled(True)

    def city_selected(self):
        print("Municipio: " + self.ui.municipioCB.currentText())
        self.ui.direccionCB.clear()

        if self.ui.municipioCB.currentIndex() != -1 and self.ui.municipioCB.currentIndex() != 0:
            self.stations = gas.get_estaciones_por_ciudad(
                self.cities.get(self.ui.municipioCB.currentText()))
            self.ui.direccionCB.addItem("Seleccione Gasolinera")

            for station in self.stations:
                print(station)
                self.ui.direccionCB\
                    .addItem(str(station['Rótulo']) + " - " + str(station['Dirección']))

            self.ui.direccionCB.setEnabled(True)

    def station_selected(self):
        self.ui.sp95E5LCD.display(0.0)
        self.ui.sp98E5LCD.display(0.0)
        self.ui.sp95E10LCD.display(0.0)
        self.ui.sp95E5PremiumLCD.display(0.0)
        self.ui.sp98E10LCD.display(0.0)

        self.ui.gasoleoALCD.display(0.0)
        self.ui.gasoleoBLCD.display(0.0)
        self.ui.gasoleoPremiumLCD.display(0.0)

        self.ui.biodieselLCD.display(0.0)
        self.ui.bioetanolLCD.display(0.0)

        self.ui.gncLCD.display(0.0)
        self.ui.gnlLCD.display(0.0)
        self.ui.glpLCD.display(0.0)
        self.ui.hidrogenoLCD.display(0.0)
        if self.ui.direccionCB.currentIndex() != -1 and self.ui.direccionCB.currentIndex() != 0:
            station = self.stations[self.ui.direccionCB.currentIndex() - 1]
            if station['Precio Gasolina 95 E5'] != '':
                self.ui.sp95E5LCD.display(float(station['Precio Gasolina 95 E5'].replace(',', '.')))

            if station['Precio Gasolina 98 E5'] != '':
                self.ui.sp98E5LCD.display(float(station['Precio Gasolina 98 E5'].replace(',', '.')))

            if station['Precio Gasolina 95 E5 Premium'] != '':
                self.ui.sp95E5PremiumLCD.display(
                    float(station['Precio Gasolina 95 E5 Premium'].replace(',', '.')))

            if station['Precio Gasolina 95 E10'] != '':
                self.ui.sp95E10LCD.display(
                    float(station['Precio Gasolina 95 E10'].replace(',', '.')))

            if station['Precio Gasolina 98 E10'] != '':
                self.ui.sp98E10LCD.display(
                    float(station['Precio Gasolina 98 E10'].replace(',', '.')))

            if station['Precio Gasoleo A'] != '':
                self.ui.gasoleoALCD.display(float(station['Precio Gasoleo A'].replace(',', '.')))

            if station['Precio Gasoleo B'] != '':
                self.ui.gasoleoBLCD.display(float(station['Precio Gasoleo B'].replace(',', '.')))

            if station['Precio Gasoleo Premium'] != '':
                self.ui.gasoleoPremiumLCD.display(
                    float(station['Precio Gasoleo Premium'].replace(',', '.')))

            if station['Precio Biodiesel'] != '':
                self.ui.biodieselLCD.display(float(station['Precio Biodiesel'].replace(',', '.')))

            if station['Precio Bioetanol'] != '':
                self.ui.bioetanolLCD.display(float(station['Precio Bioetanol'].replace(',', '.')))

            if station['Precio Gas Natural Comprimido'] != '':
                self.ui.gncLCD.display(
                    float(station['Precio Gas Natural Comprimido'].replace(',', '.')))

            if station['Precio Gas Natural Licuado'] != '':
                self.ui.gnlLCD.display(
                    float(station['Precio Gas Natural Licuado'].replace(',', '.')))

            if station['Precio Gases licuados del petróleo'] != '':
                self.ui.glpLCD.display(
                    float(station['Precio Gases licuados del petróleo'].replace(',', '.')))

            if station['Precio Hidrogeno'] != '':
                self.ui.hidrogenoLCD.display(float(station['Precio Hidrogeno'].replace(',', '.')))


app = QtWidgets.QApplication([])
application = MainWindow()
application.show()
sys.exit(app.exec())
