import os
import mysql.connector
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)

app = Flask(__name__)


def getConnection():
    con = mysql.connector.connect(host='emergerejobcareer-mysql.mysql.database.azure.com',
                                    database='estimator',
                                    user='emergere',
                                    password='password-1')   

    return con

@app.route('/Est_Getall',methods=['GET'])
def Get_allEstID_tables():
  try:
      print("Testing the module est getdetails 1243 second run")   
      return jsonify("Success1243 second run")
  
  except Exception as e:
    return jsonify(e,"An ERROR occurred in table GET Method")


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
