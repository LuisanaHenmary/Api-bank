Se requiere un entorno virtual para ejecutarlo usar el orm de la db, para crear un entorno virtual y activarlo

# Creacion del entorno virtual
py -m venv venv

# Activacion del entorno virtual
al menos ingrese la ruta del archivo activate.bat, que esta dentro de la carpeta Scripts.

# Para obterner la dependencias usadas en esto, se debe tener el entorno activado
pip install -r requirements.txt

# Para la lista de dependencias
pip list

# Mi version de python 
3.10.6

# Crear la base de datos en mysql para la API (Si esta fuera de la carpeta database)
python database/models.py

# Pero si esta dentro de la carpeta database
python models.py

# Para activar la API
uvicorn main:app --reload

# Y si se quiere ver la documentacion de la API
http://127.0.0.1:8000/redoc

BUENA SUERTE SI ESTO BASTA

