from flask import Flask, request, jsonify
import order_nlp as nlp

app = Flask(__name__)

# 파라미터 전달법
# @app.route('/users/<string:username>')
# def hello_world(username=None):
#     return("Hello {}!".format(username))

# 바디 전달법


@app.route('/order', methods=['POST'])
def post_nlp_order():
    data = request.get_json()
    result = nlp.add_menu(data["text"])
    print(result)
    return jsonify(result)


@app.route('/order/conflict', methods=['POST'])
def post_nlp_order_conflict():
    data = request.get_json()
    print("text:", data["text"], "menu_id:", data["menu_id"])
    result = nlp.conflict_menu_select(data["text"], data["menu_id"])
    print("result:", result)
    return jsonify(result)


@app.route('/option', methods=['POST'])
def post_nlp_option():
    data = request.get_json()
    result = nlp.select_option(data["text"])
    return jsonify(result)


@app.route('/set', methods=['POST'])
def post_nlp_set():
    data = request.get_json()
    result = nlp.set_check(data["text"], data["set"])
    return jsonify(result)


@app.route('/confirm', methods=['POST'])
def post_nlp_confirm():
    data = request.get_json()
    result = nlp.confirm(data["text"])
    print(result)
    return jsonify(result)


@app.route('/takeout', methods=['POST'])
def post_nlp_takeout():
    data = request.get_json()
    result = nlp.takeout(data["text"])
    print(result)
    return jsonify(result)


if __name__ == "__main__":
    app.run(port=8000, debug=False)
