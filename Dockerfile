# Indicar cual es la imagen base a utilizar
FROM python:3.12-slim

# establecer el directorio de trabajo 
WORKDIR /app

# Copiamos el archivo de requerimientos
COPY requirements.txt .

# instalamos las librerias a utilizar
RUN pip install --no-cache-dir -r requirements.txt

# copiamos todo el contenido
COPY . .

# Exporner el puerto predeterminado de flask
EXPOSE 5000

# definimos el comando para ejecutar la aplicacion
CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000" ]
