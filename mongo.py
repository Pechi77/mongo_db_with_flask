from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import re

app = Flask(__name__)

#app.config['MONGO_DBNAME'] = 'prettyprinted_rest'
#app.config['MONGO_URI'] = 'mongodb://pretty:printed@ds011863.mlab.com:11863/prettyprinted_rest'
app.config['MONGO_DBNAME'] = 'offersdb'
app.config['MONGO_URI'] = 'mongodb://iram:iram2018@ds157799.mlab.com:57799/offersdb'


mongo = PyMongo(app)

@app.route('/framework', methods=['GET'])
def get_all_frameworks():
    framework = mongo.db.offers 

    output = []

    for q in framework.find():
        
        output.append({"_id": q["_id"], "preco_change":q["preco_change"],
    "faixa_id":q["faixa_id"],
    "seller":q["seller"],
    "categoria_id":q["categoria_id"] ,
    "date":q["date"],
    "supermarket":q["supermarket"] ,
    "preco":q["preco"],
    "product":q["product"] ,
    "supermarket_id":q["supermarket_id"]})
        print(type(q["product"]))
    return jsonify({'result':output})
        #output.append()
##        output.append({'name' : q['name'], 'language' : q['language']})
##
##    return jsonify({'result' : output})

@app.route('/framework/<name>', methods=['GET'])
def get_one_framework(name):
    framework = mongo.db.offers
    regx = re.compile('^' + re.escape(name))#re.compile("^"+name, re.IGNORECASE)e.compile('^' + re.escape(name))
    #for q in framework.find({"product": {"$regex": '/*'+name+'*/'}}):
    result=[]
    for q in framework.find({"product": {'$regex':name}}):
       # print(type(q))
        #   print(q)
        result.append(q)
    if len(result)!=0:
        return jsonify({"result":result})
    else:
        return "no matching results"

    #q = framework.find_one({'name' : name})

    #if q:
     #   output = {'name' : q['name'], 'language' : q['language']}
    #else:
     #   output = 'No results found'

    #return jsonify({'result' : output})
@app.route('/seller/<name>',methods=["GET"])
def seller_record(name):
    framework=mongo.db.offers
    q=framework.find_one({'seller':name})
    if q:
        return jsonify(q)
    else:
        return "No seller found for {}".format(name)

@app.route('/framework', methods=['POST'])
def add_framework():
    framework = mongo.db.framework 

    name = request.json['name']
    language = request.json['language']

    framework_id = framework.insert({'name' : name, 'language' : language})
    new_framework = framework.find_one({'_id' : framework_id})

    output = {'name' : new_framework['name'], 'language' : new_framework['language']}

    return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)
