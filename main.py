from flask import Flask, render_template
from flask_assets import Bundle, Environment
from flask_cors import CORS
from flask_socketio import SocketIO, send
from api.controllers.EncryptionController import encryption_controller
from api.common.config import Config
import mongoengine

app = Flask(__name__, static_url_path='/statics', static_folder='api/statics', template_folder='api/templates')
cors = CORS(app)
app.register_blueprint(encryption_controller)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config[Config.UPLOAD_FOLDER.name] = Config.UPLOAD_FOLDER.value
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')

css = Bundle('src/main.css', output='dist/main.css')
assets = Environment(app)
assets.register('main_css', css)
css.build()

db = mongoengine
db.connect("kij_db")

@socketio.on("message")
def handle_update(data: str):
    if (data == "UPDATE"):
        send(data, broadcast=True, include_self=False)

@app.route("/")
def show():
    return render_template('post.html')


if __name__ == "__main__":
    socketio.run(app, debug=True)

# from encryptions.aes import AES
# from encryptions.des import DES
# from encryptions.rc4 import RC4
# from operation.ofb import OFB

# text = bytes("There was no time. He ran out of the door without half the stuff he needed for work, but it didn't matter. He was late and if he didn't make this meeting on time, someone's life may be in danger.", 'UTF-8')
# text = bytes('Good work! Your implementation is correct', 'UTF-8')
# aes_obj = AES()
# des_obj = DES()
# rc4_obj = RC4()

# # IV = bytes("oniichan", "UTF-8")
# IV = b'oniichan'
# key = "not-so-random-key"
# # print(key)

# cipher_text = RC4().encrypt(key, text)
# plain_text = RC4().decrypt(key, cipher_text)

# print(text)

# print(type(text))
# print(f'cipher_text: {cipher_text}')
# print(type(cipher_text))
# print(f'plain_text: {plain_text}')
# print(type(plain_text))