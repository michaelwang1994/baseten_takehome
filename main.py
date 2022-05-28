import redis_utils
from train import train
import datetime as dt
from flask import request, render_template
import configs
import numpy as np
import joblib
import os
from typing import Tuple


app = configs.create_flask_app(__name__)
logger = configs.create_logger(__name__)
if not os.path.isfile(configs.model_filepath):
    train()

model = joblib.load(configs.model_filepath)
redis_db = redis_utils.create_redis_client()


@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template(
            'index.html',
            **{
                'sep_ln': 0.0,
                'sep_wd': 0.0,
                'pet_ln': 0.0,
                'pet_wd': 0.0
            }
        )
    elif request.method == 'POST':
        timestamp = int(np.datetime64(dt.datetime.now()).astype(int))
        ip = request.remote_addr

        sep_ln = request.form.get('sep_ln')
        sep_wd = request.form.get('sep_wd')
        pet_ln = request.form.get('pet_ln')
        pet_wd = request.form.get('pet_wd')
        inp = [[sep_ln, sep_wd, pet_ln, pet_wd]]
        prediction = int(model.predict(inp)[0])
        prediction_filename = configs.prediction_map[prediction]

        redis_document = {
            'timestamp': timestamp,
            'sep_ln': sep_ln,
            'sep_wd': sep_wd,
            'pet_ln': pet_ln,
            'pet_wd': pet_wd,
            'prediction': prediction
        }
        redis_utils.store(redis_db, ip, redis_document)
        return render_template(
            'index.html',
            **{
                'prediction_image': os.path.join(app.config['UPLOAD_FOLDER'], prediction_filename),
                'sep_ln': sep_ln,
                'sep_wd': sep_wd,
                'pet_ln': pet_ln,
                'pet_wd': pet_wd
            }
        )


def get_min_max_for_key(form, key) -> Tuple[float]:
    range_min = form.get(f'{key}_min')
    if range_min is None or range_min == '':
        range_min = 0.0
    range_max = form.get(f'{key}_max')
    if range_max is None or range_max == '':
        range_max = 2e31 - 1
    return [range_min, range_max]


@app.route('/invocations', methods=['GET', 'POST'])
def get_invocations():
    if request.method == 'POST':
        ip = request.remote_addr
        value_ranges = {}
        for key in ['sep_ln', 'sep_wd', 'pet_ln', 'pet_wd', 'timestamp', 'prediction']:
            value_ranges[key] = get_min_max_for_key(request.form, key)

        return {'invocations': redis_utils.get(redis_db, ip, value_ranges)}
    elif request.method == 'GET':
        return render_template('invocations.html')
