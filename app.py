import random
from re import A, T
from urllib import request
import uuid
from flask import Flask
from flask import jsonify
from flask import request
from flask_uuid import FlaskUUID

app = Flask(__name__)
FlaskUUID(app)

notes = []
memo = {}

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/notes', methods=['GET', 'POST', 'PUT'])
def get_or_post_notes():
    if request.method == "POST":
        note = request.get_json()["content"]
        notes.append(note);
        return {"index": len(notes) - 1, "content": note}
    if request.method == "GET":
        return  jsonify(notes)
    
@app.route('/notes/<int:index>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def get_add_update_delete_specific_note(index):
    if request.method == "POST":
        note = request.get_json()["content"]
        notes.insert(index,note);
        return {"index": index, "content": note}
    if request.method == "GET":
        return {"index": index, "content": notes[index]}
    if request.method == "PUT":
        note = request.get_json()["content"]
        notes[index] = note
        return {"index": index, "content": note}
    if request.method == "DELETE":
        notes.pop(index)
        return '', 204

@app.route('/documents', methods=['POST'])
def create_document():
    doc = request.get_json()["content"]
    doc_id= uuid.uuid4()
    f = open(f"{doc_id}.txt", "x")
    f.write(doc)
    f.close()
    return str(doc_id)

@app.route('/documents/<string:doc_id>', methods=['GET'])
def read_document(doc_id):
    f = open(f"{doc_id}.txt", "r")
    doc = f.read()
    return {"docId": doc_id, "content": doc}

@app.route('/math/<num1>/<num2>/<amount>', methods=['GET'])
def perfrom_math(num1, num2, amount):
    num1, num2, amount = float(num1), float(num2), int(amount)
    for _ in range(amount):
        num1 * num2;
    return "Done"

@app.route('/factorial/<int:num>', methods=['GET'])
def get_factorial(num):
    if num in memo:
        return memo[num]
    else:
        res = 1
        for i in range(1, num + 1):
            res *= i
        memo[num] = res
        return {"product": res}
    
@app.route('/coordinates/<int:amount>', methods=['GET'])
def get_coordinates(amount):
    res = []
    for _ in range(amount):
        lattitude = random.random() * 180 - 90
        longitude = random.random() * 360 - 180
        nsHemisphere = "North" if lattitude > 0 else "South";
        ewHemisphere = "East" if longitude > 0  else "West";
        cordinate = {"lattitude": lattitude, "longitude": longitude, "nsHemisphere": nsHemisphere, "ewHemisphere":ewHemisphere}
        res.append(cordinate)
    return jsonify(res)
    

if __name__ == '__main__':
    app.run()