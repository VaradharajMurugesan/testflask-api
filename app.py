import os
import mysql.connector
import json
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
        con = getConnection()
        cur = con.cursor()
        cur.execute  (""" SELECT JSON_ARRAYAGG(  
                                JSON_OBJECT(
                                'estimatorID', e.estimatorID,
                                'projectName', e.projectName,
                                'estimatorName', e.estimatorName,
                                'dashBoardName', e.dashBoardName,
                                'totalEfforts_inPersonHours', e.totalEfforts_inPersonHours,
                                'retestingEfforts', e.retestingEfforts,
                                'totalEfforts_inPersonDays', e.totalEfforts_inPersonDays,
                                'created_date',e.created_date,
                                'updated_date',e.updated_date,
                                'taskGroup', 
                            (SELECT JSON_ARRAYAGG(
                                JSON_OBJECT(
                                        'taskGroup_id', tg.taskGroup_id, 
                                        'taskGroupname', tg.taskGroupname,
                                        'estimatorID',tg.estimatorID,
                                        'created_date',tg.created_date,
                                        'updated_date',tg.updated_date,
                                        'tasks', 
                                        (SELECT JSON_ARRAYAGG(
                                            JSON_OBJECT(
                                                'task_id', t.task_id, 
                                                'taskName', t.taskName, 
                                                'totalNum', t.totalNum, 
                                                'totalPerUnit', t.totalPerUnit, 
                                                'totalEffort', t.totalEffort,
                                                'taskGroup_id',t.taskGroup_id,
                                                'created_date',t.created_date,
                                                'updated_date',t.updated_date
                        )
                    ) FROM tasks t where t.taskGroup_id =tg.taskGroup_id )
                )
        ) FROM taskGroup tg  WHERE tg.estimatorID = e.estimatorID )
        )
        )FROM estimator e """)
        rows = cur.fetchall()
        result_json_str=rows[0][0]
        result_json = json.loads(result_json_str)
        return jsonify(result_json)
    
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
