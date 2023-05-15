from flask import Flask
from V1.EdificiosBPV1 import edificiosBP
from V1.SalasBPV1 import salasBP
from V1.ReservasBPV1 import reservasBP

app=Flask(__name__)
app.register_blueprint(edificiosBP)
app.register_blueprint(salasBP)
app.register_blueprint(reservasBP)

@app.route('/',methods=['GET'])
def init():
    return "Escuchando el Servicio REST de Salas"

if __name__=='__main__':
    app.run(debug=True)