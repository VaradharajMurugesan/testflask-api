from flask import Flask, request, jsonify
import sqlite3
import json
import mysql.connector
from datetime import datetime
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


token_id = None

@app.route('/validate_token',methods=['GET'])
def validate_token():
    print("intiating")
    global token_id
    try:
        message = None
        args = request.args
        token_id=args.get("tokenID")        
        #set_processcompleted()       
        return jsonify("message: ","Success")
    
    except Exception as e:
        print(e,"Something error in Posting")
        return jsonify("Something wrong")


if __name__ == '__main__':
    app.run(debug=True)


