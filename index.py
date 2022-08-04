from flask import Flask, request, jsonify

app = Flask(__name__)

# 파라미터 전달법
# @app.route('/users/<string:username>')
# def hello_world(username=None):
#     return("Hello {}!".format(username))

# 바디 전달법


@app.route('/nlp/order', methods=['POST'])
def post_nlp_order():
    data = request.get_json()
    print(data)
    return jsonify(data)
