from flask import Flask,jsonify,request
import mysql.connector

app=Flask(__name__)

def DBconnection():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='',
        password='',
        database='student_details'
    )

@app.route('/insert',methods=['POST'])
def insert_record():
    data=request.get_json()
    sname=data.get('sname')
    std=data.get('std')
    percentage=data.get('percentage')

    try:
        db=DBconnection()
     
        mycursor=db.cursor()
        sql="INSERT INTO student (sname,std,percentage) VALUES (%s,%s,%s)"
        val=(sname,std,percentage)
        mycursor.execute(sql,val)
        db.commit()
        return jsonify({"message":"Sucessfully Record Inserted"}),200
        
    except mysql.connector.Error as e:
        return jsonify({"error":str(e)}),500
    finally:
        db.close()

@app.route("/update",methods=["PUT"])
def update_records():
    try:
        data=request.get_json()
        stuid=data.get('stuid')
        sname=data.get('sname')
        std=data.get('std')
        percentag=data.get('percentage')

        db=DBconnection()
        mycursor=db.cursor()
        sql="UPDATE student SET sname=%s,std=%s,percentage=%s WHERE stuid=%s"
        val=(sname,std,percentag,stuid)
        mycursor.execute(sql,val)
        db.commit()
        return jsonify({"message":"Updated sucessfully"}),200
    except mysql.connector.Error as e:
        return jsonify({"error":str(e)})
    finally:
        db.close()

@app.route("/delete",methods=['DELETE'])
def delete_record():
    try:
        data=request.get_json()
        stuid=data.get('stuid')
       
        db=DBconnection()
        mycursor=db.cursor()
        sql="DELETE FROM student WHERE stuid=%s"
        val=(stuid,)
        mycursor.execute(sql,val)
        db.commit()
        return jsonify({"message":"Sucessfully DELETED"}),200
    except mysql.connector.Error as e:
        return jsonify({"message":str(e)})
    finally:
        db.close()

@app.route("/show_table",methods=['GET'])
def read_data():
    try:
        db=DBconnection()
      
        mycursor=db.cursor()
        mycursor.execute("SELECT * FROM student")
        result=mycursor.fetchall()
        ans=[]
        for row in result:
            ans.append({'stuid':row[0],"sname":row[1],'std':row[2],'percentage':row[3]})
        return jsonify(ans),200
    except mysql.connector.Error as e:
        return jsonify({"message":str(e)})
    finally:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)

        

