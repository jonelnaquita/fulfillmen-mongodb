from flask import Flask, request, Response

from flask_ngrok import run_with_ngrok

import pymongo
import json

with open ('config.json') as file:
    params = json.load(file)['params']
    
app = Flask(__name__)
run_with_ngrok(app)

client = pymongo.MongoClient(params['client_url'])
db = client[params['db']]

@app.route('/webhook', methods = ["GET", "POST"])
def webhook():
    req = request.get_json(force = True)
    query = req['queryResult']['queryText']
    result = req['queryResult']['fulfillmentText']
    action = req['queryResult']['action']
    data = {
        "query": query,
        "result": result,
        "action": action
    }
    
    col = db['chat_data']
    col.insert_one(data)
    print("Data successfully inserted to database") 
    
    return Response(status=200)

if __name__ == "__main__":
    app.run()   
