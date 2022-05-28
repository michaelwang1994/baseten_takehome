import os
from flask import Flask
import logging

data_dir = 'data'
static_dir = 'static'
model_filepath = os.path.join(data_dir, 'model.joblib')
prediction_map = {
    0: 'iris_setosa.png',
    1: 'iris_versicolor.png',
    2: 'iris_verginica.png'
}


def create_flask_app(name) -> Flask:
    app = Flask(name)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.config['UPLOAD_FOLDER'] = static_dir
    return app


def create_logger(name) -> logging.Logger:
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.DEBUG,
    )
    return logging.getLogger(name)
