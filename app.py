from flask import Flask # Importa a biblioteca Flask do módulo flask para criar a aplicação web.
from routes.rota_produtos import produtos_bp #
from routes.rota_usuarios import usuarios_bp
from routes.rota_relatorios import relatorios_bp
from database.db import db


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///foodstock.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.register_blueprint(produtos_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(relatorios_bp)

db.init_app(app)

app.register_blueprint(produtos_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)