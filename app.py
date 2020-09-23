from flask import Flask, jsonify, request, json
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask import jsonify, request
from werkzeug.security import check_password_hash,generate_password_hash
from fuzzywuzzy import process
import speech_recognition as sr
import pymongo
import joblib
import gensim
import scipy
import random


app = Flask(__name__)

app.secret_key = "secretkey123"

app.config['MONGO_URI'] = "mongodb+srv://pasi96:pasiya96@cluster0.cb5lr.mongodb.net/smart_interview_system?ssl=true&ssl_cert_reqs=CERT_NONE"
app.config['JWT_SECRET_KEY'] = 'secret'
mongo = PyMongo(app)
myclient = pymongo.MongoClient("mongodb+srv://pasi96:pasiya96@cluster0.cb5lr.mongodb.net/smart_interview_system?ssl=true&ssl_cert_reqs=CERT_NONE")
mydb = myclient["smart_interview_system"]

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


CORS(app)

@app.route('/')
def home():
    return 'Home'

# create interview
@app.route('/createInterview',  methods=['POST'])
def create_interview():
    _json = request.json
    _interviewname = _json["int_name"]
    _date = _json["date"]

    collectionName = mydb[_interviewname]

    if _interviewname and _date  and request.method == "POST":

        collectionName.insert_one({"name": _interviewname, "date": _date, "state": False})
        resp = jsonify("Interview Created Successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()

# delete interview


@app.route('/deleteInterview/<name>', methods=['DELETE'])
def delete_interview(name):
    collectionName = mydb[name]
    collectionName.drop()
    resp = jsonify("Interview Details Deleted Successfully")
    resp.status_code = 200
    return resp

# Add candidate details to the interview


@app.route('/createCandidate/<name>', methods=['POST'])
def create_candidate(name):
    _json = request.json
    _name = _json["name"]
    _email = _json["email"]

    collectionName = mydb[name]
    all_candidates = collectionName.find()
    canidate_list = []

    for x in all_candidates:
        canidate_list.append(x)

    def auto_id():
        last_element = canidate_list[len(canidate_list) - 1]
        last_id = last_element["_id"]
        get_dig = last_id.split("_")
        int_dig = int(get_dig[2])
        new_id = "C_NEW_" + str(int_dig+1)
        return new_id

    if(len(canidate_list) == 1):
        canidate = {
            "_id": "C_NEW_1",
            "name": _name,
            "email": _email,
            "oralanswers": [],
            "oralstate": False,
            "oraltestscore": 0,
            "writtenanswers": [],
            "writtenstate": False,
            "writtenscore": 0
        }
    else:
        canidate = {
            "_id": auto_id(),
            "name": _name,
            "email": _email,
            "oralanswers": [],
            "oralstate": False,
            "oraltestscore": 0,
            "writtenanswers": [],
            "writtenstate": False,
            "writtenscore": 0
        }

    if _name and _email and request.method == "POST":
        collectionName.insert_one(canidate)
        resp = jsonify("Cadidate Added successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()

# Remove candidate from interview


@app.route('/deleteCandidate/<id>/<name>', methods=['DELETE'])
def delete_candidate(id, name):
    collectionName = mydb[name]
    collectionName.delete_one({"_id": id})
    resp = jsonify("Interview Details Deleted Successfully")
    resp.status_code = 200
    return resp


@app.route('/updateCandidate/<id>/<name>', methods=['PUT'])
def update_candidate(id, name):
    _json = request.json
    _name = _json["name"]
    _email = _json["email"]

    collectionName = mydb[name]
    collectionName.update_one({"_id": id}, {"$set": {"name": _name, "email": _email }})
    resp = jsonify("Details updated successfully")
    resp.status_code = 200
    return resp


@app.route('/getCandidates/<name>', methods=['GET'])
def get_candidates(name):
    collectionName = mydb[name]
    result = collectionName.find().sort("oralstate")
    resp = dumps(result[1:])
    return resp


# Add questions to the interview


@app.route('/addQuestion/<name>', methods=['POST'])
def add_question(name):
    _json = request.json
    _question = _json["question"]
    _keywords = _json["keywords"]
    _defans = _json["answer"]

    collectionName = mydb[name + "_Quiz"]
    all_quiz = collectionName.find()
    quiz_list = []

    for x in all_quiz:
        quiz_list.append(x)

    def auto_id():
        last_element = quiz_list[len(quiz_list) - 1]
        last_id = last_element["_id"]
        get_dig = last_id.split("_")
        int_dig = int(get_dig[2])
        new_id = "Q_ID_" + str(int_dig + 1)
        return new_id

    if (len(quiz_list) == 0):
        question = {
            "_id": "Q_ID_1",
            "question": _question,
            "keywords": _keywords,
            "def_ans": _defans
        }
    else:
        question = {
            "_id": auto_id(),
            "question": _question,
            "keywords": _keywords,
            "def_ans": _defans
        }

    if _question and _keywords and request.method == "POST":
        collectionName.insert_one(question)
        resp = jsonify("Question Added successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()

# Remove question


@app.route('/deleteQuiz/<id>/<name>', methods=['DELETE'])
def delete_quiz(id, name):
    collectionName = mydb[name + "_Quiz"]
    collectionName.delete_one({'_id': id})
    resp = jsonify("User deleted successfully")
    resp.status_code =200
    return resp

# Edit question


@app.route('/updateQuestion/<id>/<name>', methods=['PUT'])
def update_question(id, name):
    _json = request.json
    _question = _json["question"]
    _keywords = _json["keywords"]

    collectionName = mydb[name]
    collectionName.update_one({"_id": id}, {"$set": {"question": _question, "keywords": _keywords }})
    resp = jsonify("Question updated successfully")
    resp.status_code = 200
    return resp

# Select all questions


@app.route('/getQuestions/<name>')
def get_quewstion_list(name):
    collectionName = mydb[name + "_Quiz"]
    result = collectionName.find()
    array_of_result = list(result)
    dump_arr =[]
    id = random.sample(range(1, len(array_of_result)), 10)
    print(id)
    for item in array_of_result:
        item_id = item["_id"]
        for i in id:
            if int(item_id[5:6]) == i :
                dump_arr.append(item)

    print(dump_arr)
    resp = dumps(dump_arr)
    return resp

@app.route('/getAllQuestions/<name>')
def get_all_quewstion_list(name):
    collectionName = mydb[name + "_Quiz"]
    result = collectionName.find()
    resp = dumps(result)
    return resp


# Select all interviews


@app.route('/getInterviews')
def get_interview():
    result = mydb.list_collection_names()
    expected_result = []

    for name in result:
        name_splits= name.split("_")
        if(name_splits[0] == 'interview' and len(name) == 18):
            collectionName = mydb[name]
            res = collectionName.find_one({"name": name})
            if(res['state'] == False):
                expected_result.append({"name": name})
    print(expected_result)
    return dumps(expected_result)

# Select all interviews


@app.route('/getArchives')
def get_archive():
    result = mydb.list_collection_names()
    expected_result = []

    for name in result:
        name_splits= name.split("_")
        if(name_splits[0] == 'interview' and len(name) == 18):
            collectionName = mydb[name]
            res = collectionName.find_one({"name": name})
            if(res['state'] == True):
                expected_result.append({"name": name})
    print(expected_result)
    return dumps(expected_result)

# Get question for particular interview


@app.route('/getQuestions/<name>')
def get_question_list(name):
    collectionName = mydb[name]
    result = collectionName.find()
    resp = dumps(result)
    return resp

# Add keywords


@app.route('/addSpecificKey/<name>', methods=['POST'])
def add_specific(name):
    _json = request.json
    _keywords = _json["keywords"]

    keySet = {
        "_id": "spec_keywords",
        "keywords": _keywords
    }
    collectionName = mydb[name + "_Quiz"]
    if _keywords and request.method == "POST":
        collectionName.insert_one(keySet)
        resp = jsonify("Keyset Added successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()


# Register User

@app.route('/users/register', methods=["POST"])
def register():
    users = mongo.db.user
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()

    user_id = users.insert({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'created': created
    })

    new_user = users.find_one({'_id': user_id})

    result = {'email': new_user['email'] + ' registered'}

    return jsonify({'result': result})

# Validate user


@app.route('/users/login', methods=['POST'])
def login():
    users = mongo.db.user
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = ""

    response = users.find_one({'email': email})

    if response:
        if bcrypt.check_password_hash(response['password'], password):
            access_token = create_access_token(identity = {
                'first_name': response['first_name'],
                'last_name': response['last_name'],
                'email': response['email']
            })
            result = jsonify({'token':access_token})
        else:
            result = jsonify({"error":"Invalid username and password"})
    else:
        return not_found()
    return result


# Error function


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }

    resp = jsonify(message)

    resp.status_code = 404

    return resp

# Get all user details


@app.route('/getAllusers')
def uers():
    users =mongo.db.user.find()
    resp = dumps(users)
    return  resp

# Search User


@app.route('/users/<id>')
def user(id):
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return  resp

# Remove user


@app.route('/deleteUser/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({'_id': ObjectId(id)})
    resp = jsonify("User deleted successfully")
    resp.status_code =200
    return resp

# Voice detection endpoint


@app.route('/api/voice/<name>/<id>/<voice>')
def process_voice(name, id, voice):
    collectionName = mydb[name + "_Quiz"]

    get_question = collectionName.find_one({'_id': id})
    print(get_question.get('_id'))

    listofkeyword = get_question['keywords']
    print(listofkeyword)
    listoffound = []

    def getmatch(query, choices, limit=len(listofkeyword)):
        result = process.extract(query, choices, limit=limit)
        return result

    def get_matching_words():
        voice_text = voice
        check_acc = calculate_sim(voice_text, get_question.get('question'))
        results = voice_text.split(" ")
        for match in results:
            allres = getmatch(match.lower(), listofkeyword)
            for matches in allres:
                if (matches[1] > 80):
                    object1 = {
                        "word": matches[0],
                        "pct": matches[1]
                    }
                    listoffound.append(object1)
        return [id, listoffound, voice_text, check_acc]

    res = get_matching_words()
    print(res)
    resp = dumps(res)
    return resp


# Add processed data to database


@app.route('/addVocalData/<id>/<name>/<ans>', methods=['POST'])
def add_vocal_interview_data(id, name, ans):
    _json = request.json

    collectionName = mydb[name]
    _RES = collectionName.find_one({'_id': id})
    print(type(ans))

    keySet = _json

    collectionName = mydb[name]
    if ans and request.method == "POST":
        collectionName.update_one({'_id': id}, {'$push': {'oralanswers': keySet}})
        resp = jsonify("Answer Added successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()



#update state


@app.route('/changeState/<id>/<name>/<score>', methods=['POST'])
def change_state(id, name, score):


    collectionName = mydb[name]
    _RES = collectionName.find_one({'_id': id})
    current_state = _RES.get('oralstate')

    if request.method == "POST":
        collectionName.update_one({'_id': id}, {'$set': {'oralstate': not current_state, 'oraltestscore': float(score) }})
        resp = jsonify("State Updated")
        resp.status_code = 200
        return resp
    else:
        return not_found()


#update state


@app.route('/changeInterviewState/<name>', methods=['POST'])
def change_state_int(name):

    collectionName = mydb[name]
    _RES = collectionName.find_one({'name': name})
    current_state = _RES.get('state')

    if request.method == "POST":
        collectionName.update_one({'name': name}, {'$set': {'state': not current_state}})
        resp = jsonify("State Updated")
        resp.status_code = 200
        return resp
    else:
        return not_found()



# Calculate accuracy of candidate's answer


def calculate_sim(answer, def_answer):
    print("Provided Answer: {}".format(answer))
    print("Pre-defined Answer: {}".format(def_answer))
    ans_vec = model.infer_vector(gensim.utils.simple_preprocess(answer))
    def_ans_vec = model.infer_vector(gensim.utils.simple_preprocess(def_answer))

    sim = 1 - scipy.spatial.distance.cosine(ans_vec, def_ans_vec)
    print("Similarity : {}".format(sim))
    return sim * 100

# Process and handle voice inputs


def processVoice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=5)
        print("Say something!")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return print("Google could not understand audio")
    except sr.RequestError as e:
        return print("Google error; {0}".format(e))


if __name__ == "__main__":
    model = joblib.load('doc2vec-model.pkl')
    print('Model Loaded.')
    app.run(debug=True)

