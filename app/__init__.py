from flask import Flask

app = Flask(__name__)

# Importing views/routes
from app.main import minha_funcao

# Registering blueprints or routes
app.register_blueprint(minha_funcao)

if __name__ == '__main__':
    app.run()