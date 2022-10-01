from flask import Flask
from api.controllers.EncryptionController import encryption_controller
from api.common.config import Config

app = Flask(__name__)
app.config[Config.UPLOAD_FOLDER.name] = Config.UPLOAD_FOLDER.value

app.register_blueprint(encryption_controller)


@app.route("/")
def show():
    return "Hai"


if __name__ == "__main__":
    app.run(debug=True)
