# Crear la base de datos en mysql para la API (Si esta fuera de la carpeta database)
python database/models.py

# Pero si esta dentro de la carpeta database
python models.py

Se requiere un entorno virtual para ejecutarlo, para crear un entorno virtual y activarlo

# Creacion del entorno virtual
py -m venv nombre_entorno

# Activacion del entorno virtual
al menos ingrese la ruta del archivo activate.bat, que esta dentro de la carpeta Scripts.

# Para obterner la dependencias usadas en esto, se debe tener el entorno activado
pip install -r requirements.txt

Mi version de python fue la 3.10.6

# Para activar la API
uvicorn main:app --reload

# Y si se quiere ver la documentacion de la API
http://127.0.0.1:8000/redoc

BUENA SUERTE SI ESTO BASTA

