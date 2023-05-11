from flask import Flask
from V1.EdificiosBPV1 import edificiosBP

app=Flask(__name__)
app.register_blueprint(edificiosBP)

@app.route('/',methods=['GET'])
def init():
    return "Escuchando el Servicio REST de Salas"

if __name__=='__main__':
    app.run(debug=True)