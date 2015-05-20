from flask import Flask
from simulation import Simulation



app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/data/<int:seed>/<int:nodes>/<int:steps>')
def data(seed, nodes, steps):
    s = Simulation(seed, nodes)
    s.run_simulation(steps)
    return s.get_json()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
