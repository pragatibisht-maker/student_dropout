from flask import Flask
from routes.predict import predict_bp
from model.loader import load_artifacts

app = Flask(__name__)

app.config['ARTIFACTS'] = load_artifacts()
print('[?] Model artifacts loaded and ready.')

app.register_blueprint(predict_bp)

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok', 'message': 'Dropout Risk API is running.'}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
