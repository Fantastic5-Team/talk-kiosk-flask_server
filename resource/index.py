from flask import Flask, request, jsonify
import order_nlp as nlp

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


@app.route('/option', methods=['POST'])
def post_nlp_option():
    data = request.get_json()
    print(data)
    result = nlp.set_check(data("text"), data("set"))
    return jsonify(result)


if __name__ == "__main__":
    app.run()
