from flask import Flask, jsonify, request, abort

app = Flask(__name__)

RATES = {
    "USD": 90.0,
    "EUR": 100.0
}

@app.route('/rate')
def get_rate():
    currency = request.args.get('currency', '').upper()
    
    if currency not in RATES:
        abort(400, description={"message": "UNKNOWN CURRENCY"})
    
    try:
        return jsonify({"rate": RATES[currency]})
    except Exception as e:
        abort(500, description={"message": "UNEXPECTED ERROR"})

if __name__ == '__main__':
    app.run(port=5000)
