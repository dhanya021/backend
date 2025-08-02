from flask import Flask
from routes.fake_yield_routes import fake_bp

app = Flask(__name__)
app.register_blueprint(fake_bp)

@app.route('/')
def home():
    return "Yield Prediction Storage Simulator"

if __name__ == '__main__':
    app.run(debug=True)
