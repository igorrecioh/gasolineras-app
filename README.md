# GasolinerasAPP
[![Pylint](https://github.com/igorrecioh/gasolineras-app/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/igorrecioh/gasolineras-app/actions/workflows/pylint.yml)
## Requisitos
- Python3
- Pip3 actualizado

## Instalación
```bash
# Clona el repositorio
git clone https://github.com/igorrecioh/gasolineras-app.git

# Accede al directorio del proyecto
cd gasolineras-app

# Crea un entorno virtual
python3 -m venv myvenv

# Activa el entorno
. myvenv/bin/activate

# Instala los paquetes necesarios
pip3 install -r requirements.txt

# Ejecuta la app
python main.py
```

## Información

- Esta aplicación proporciona datos sobre el precio de los combustibles
- Se basa en la búsqueda por CCAA, provincia y localidad
- Los datos se obtienen de la API proporcionada por el 
  Ministerio de Asuntos Económicos y Transformación Digital
- Más información --> https://datos.gob.es

## Bugs / mejoras
- En caso de encontrar algún error o si se desea proponer mejoras en la aplicación, 
  abre un issue con la información detallada y se intentará solventar cuanto antes