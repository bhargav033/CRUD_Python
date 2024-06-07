from flask import Flask,request,jsonify 
import mysql.connector

app=Flask(__name__)

def dbconnection():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='',
        password='',
        database='student_details'

    )

@app.route('/regester',methods=['POST'])
def register():
    data=request.get_json()
    uname=data.get('uname')
    passwod=data.get('passwod')
    repass=data.get('repass')
    if passwod != repass:
        return jsonify({"message":"password and repassword not metch"})
    try:
        db=dbconnection()
        mycursor=db.cursor()
        sql="INSERT INTO register_tab (uname,passwod,repass) VALUES (%s,%s,%s)"
        val=(uname,passwod,repass)
        mycursor.execute(sql,val)
        db.commit()
        return jsonify({"message":"Registration sucessfull "})
    except mysql.connector.Error as e:
        return jsonify({"message":str(e)})
    finally:
        db.close()




@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    uname = data.get('uname')
    passwod = data.get('passwod')
    
    try:
        db = dbconnection()
        mycursor = db.cursor()
        sql = "SELECT uname, passwod FROM register_tab WHERE uname=%s"
        val=(uname,)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        
        if result and result[1] == passwod:
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    except mysql.connector.Error as e:
        return jsonify({"Error": str(e)}), 500
    finally:
        db.close()


if __name__=='__main__':
    app.run(debug=True)
