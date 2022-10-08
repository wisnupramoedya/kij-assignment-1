from flask import Flask, render_template
from flask_assets import Bundle, Environment
from api.controllers.EncryptionController import encryption_controller
from api.common.config import Config
import mongoengine

app = Flask(__name__, static_url_path='/statics', static_folder='api/statics', template_folder='api/templates')
app.register_blueprint(encryption_controller)
app.config[Config.UPLOAD_FOLDER.name] = Config.UPLOAD_FOLDER.value

css = Bundle('src/main.css', output='dist/main.css', filters='postcss')
assets = Environment(app)
assets.register('main_css', css)
css.build()

db = mongoengine
db.connect("kij_db")

@app.route("/")
def show():
    return render_template('post.html')


if __name__ == "__main__":
    app.run(debug=True)


# from encryptions.aes import AES
# from encryptions.des import DES
# from encryptions.rc4 import RC4
# from operation.ofb import OFB

# text = bytes("There was no time. He ran out of the door without half the stuff he needed for work, but it didn't matter. He was late and if he didn't make this meeting on time, someone's life may be in danger.", 'UTF-8')

# aes_obj = AES()
# des_obj = DES()
# rc4_obj = RC4()

# IV = bytes("oniichan", "UTF-8")
# key = "akuadalahlolicon"
# print(key)
# ofb_mode = OFB(IV).set_class(rc4_obj)
# cipher_text = ofb_mode.encrypt(key, text)
# plain_text = ofb_mode.decrypt(key, cipher_text)

# # print(text)

# # print(type(text))
# print(cipher_text)
# # print(type(cipher_text))
# print(plain_text)
# # print(type(plain_text))
