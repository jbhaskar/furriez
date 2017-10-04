
from flask import request, render_template
from app import app
from flask_jwt_extended import JWTManager, jwt_required, create_access_token,  get_jwt_identity
from werkzeug.security import safe_str_cmp
import json
from pymongo import MongoClient
from models import User
import bson
from bson.json_util import dumps
from bson  import ObjectId
from bson import json_util
import requests

client = MongoClient("localhost", 27017)
db = client.furriesDev
users = db.users
posts = db.posts
app.config['SECRET_KEY'] = 'super-secret'

fb_app_id = "1310235199099226"
fb_app_token = "8c9ef6c5c7e383a07517f99fe26ae191"
fb_me_url = "https://graph.facebook.com/v2.10/me?fields=id,name&access_token="

jwt = JWTManager(app)

def verify_fb_creds(fb_user_token):
    r = requests.get("%s%s" % (fb_me_url, fb_user_token)).json()
    if r.get('id', None):
        user = users.find_one({ "fb_user_id" : r.get('id', None) })
        if (user == None):
            user_id = users.save({ "fb_user_id" : r['id'], "name" : r['name'], "fb_access_token" : fb_user_token })
            user = users.find_one({"_id" : user_id})
        return user

@app.route('/login', methods = ['POST'])
def login():
    provider = request.json.get('provider', None)
    if provider == 'facebook':
        access_token = request.json.get('access_token', None)
        user = verify_fb_creds(access_token)
        print user
        if user:
            user = users.find_one({"_id" : user['_id']})
            user['fb_data'] = request.json
            users.save(user)
            ret = {'access_token': create_access_token( identity = str(user["_id"]) ) }
        else:
            return dumps({"msg": "Invalid fb access token"}), 401
    elif provider == "google":
        pass
    else:
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username:
            return dumps({"msg": "Missing username parameter"}), 400
        if not password:
            return dumps({"msg": "Missing password parameter"}), 400

        user = users.find_one({ "username" : username })
        if user and password != user['password']:
            return dumps({"msg": "Bad username or password"}), 401
        ret = {'access_token': create_access_token(identity=str(user["_id"]))}

    return dumps(ret, indent=4), 200


@app.route('/article/<id>', methods = ['GET'])
@jwt_required
def get_article(id):
    post = posts.find_one({"_id": ObjectId(id)})
    import pdb
    pdb.set_trace()
    return dumps({ 'success': True, 'data': post }, indent=4)

# type = 1 => article
@app.route('/article', methods = ['POST'])
@jwt_required
def add_article():
    current_user = get_jwt_identity()
    post = {
        'type': 1,
        'owner': current_user
    }

    post['data'] = request.json['data']
    post['_id'] = posts.insert(post)
    return dumps({ 'success': True, 'data': post }, indent=4)


# type = 2 => question
@app.route('/question', methods = ['POST'])
@jwt_required
def add_question():
    post = {
        'type': 2,
        'owner': current_user
    }

    post['data'] = request.json['data']
    post['_id'] = posts.insert(post)
    return dumps({ 'success': True, 'data': post }, indent=4)

@app.route('/question/<id>', methods = ['GET'])
@jwt_required
def get_question(id):
    post = posts.find_one({"_id": ObjectId(id)})
    return dumps({ 'success': True, 'data': post }, indent=4)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/protected')
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return '====== %s' % current_user

@app.route('/me')
@jwt_required
def me():
    current_user = get_jwt_identity()
    user = users.find_one({"_id" : ObjectId(current_user)})
    return dumps(user, indent=4)