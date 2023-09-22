from flask import Flask, request, render_template, jsonify
import numpy as np
import replicate
import os
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
import pickle as pkl
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime


os.environ['REPLICATE_API_TOKEN'] = "r8_3Cn377wOsZ8ywqtFyCCicG5JwHqpHYS0sONIW"
engine = create_engine('postgresql://fl0user:ClU4ueygKz9G@ep-red-butterfly-89282058.eu-central-1.aws.neon.tech:5432/spaces?sslmode=require')


app = Flask(__name__)


@app.route("/img_det", methods=["GET", "POST"])
def img_nsfw():
    import requests
    if request.method == "POST":
        # Obtener el archivo de imagen desde el formulario
        img = request.files['image']
        print(img)
        # Verificar si se seleccionó un archivo
        if img:
            # Crear una solicitud POST con el archivo de imagen
            url = "https://nsfw-images-detection-and-classification.p.rapidapi.com/adult-content-file"

            # El encabezado Content-Type se configurará automáticamente con 'multipart/form-data'

            # Crea un diccionario para contener los datos del formulario y la imagen
            data = {}
            data['image'] = (img.filename, img, img.content_type)

            # Agrega los encabezados necesarios
            headers = {
                "X-RapidAPI-Key": "c679110cc2msh7f219734fbb8848p15052ejsnd747bb937243",
                "X-RapidAPI-Host": "nsfw-images-detection-and-classification.p.rapidapi.com"
            }

            # Realiza la solicitud POST con los datos y encabezados
            response = requests.post(url, files=data, headers=headers)
            
            # Meter todo en base d datos:

            cols = {
                'user':'-',
                'img': data,
                'response':str(response.json()['objects']),
                'unsafe':str(response.json()['unsafe'])
            }
            index = [int(datetime.now().timestamp())]
            df = pd.DataFrame(cols, index= index)
            df.to_sql(name="pic_control",if_exists='append',con=engine, index = False)
            
            
            return jsonify(response.json())
        return render_template('img_form.html')

    return render_template('img_form.html')

if __name__=="__main__":
    app.run(debug=True, port=8000)