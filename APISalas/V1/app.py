from flask import Flask

app=Flask(__name__)

@app.route('/',methods=['GET'])
def init():
    return "Escuchando el Servicio REST de Salas"

if __name__=='__main__':
    app.run(debug=True)