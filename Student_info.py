import mysql.connector

def database_connection():
    try:    
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin'

            )
        db.cursor()
        print("Connected properly")
    except mysql.conector.Error as e:
        print(f"Error :{e}")
    finally:
        if db:
            db.close()

def create_database():
    try:
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin'
        )
        mycursor=db.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS student_details")
        print("Sucessfully created database")
    except mysql.connector.Error as e:
        print(f"Error :{e}")
    finally:
        if db:
            db.close()

# Create Table :

def create_table():
    try:
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin',
            database='student_details'

        )
        mycursor=db.cursor()
        mycursor.execute(""" CREATE TABLE STUDENT_INFO(
                         stuid INT AUTO_INCREMENT PRIMARY KEY,
                         name VARCHAR(255) NOT NULL,
                         study VARCHAR(255) NOT NULL,
                         fee INT NOT NULL
        ) """)
        print("Table created successfully")
    except mysql.connector.Error as e:
        print(f"Error :{e}")
    finally:
        if db:
            db.close()

#INSERT RECORD
def insert_record(name,study,fee):
    try:
        db=mysql.connector.connect(
            host="127.0.0.1", 
            user="root",
            password="admin",
            database="student_details"

        )
        mycursor=db.cursor()
        sql="INSERT INTO student_info (name,study,fee) VALUES (%s,%s,%s)"
        val=(name,study,fee)
        mycursor.execute(sql,val)
        db.commit()
        print("REcord Insert Sucessfully")
    except mysql.connector.Error as e:
        print(f"Error :{e}")
    finally:
        db.close()

#Show record
def read_data():
    try:
        db=mysql.connector.connect(
            host="127.0.0.1", 
            user="root", 
            password="admin",
            database="student_details"
        )
        mycursor=db.cursor()
        mycursor.execute("SELECT * FROM student_info ")
        result=mycursor.fetchall()
        for row in result:
            print(row)
        print("sucessfully read the data ")
    except mysql.connector.Error as e:
        print(f"Error:{e}")
    finally:
        db.close()

#Update the database
def update_record(stuid,name,study,fee):
    try:
        db=mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="admin",
            database="student_details"
        )
        mycursor=db.cursor()
        sql="UPDATE student_info SET name=%s , study=%s,fee=%s WHERE stuid=%s"
        val=(name,study,fee,stuid)
        mycursor.execute(sql,val)
        db.commit()
        print("Sucessfully Updated student_info")
    except mysql.connector.Error as e:
        print(f"Error :{e}")
    finally:
        db.close()


#DELETED Record
def delete_record(stuid):
    try:
        db=mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="admin",
            database="student_details"

        )
        mycursor=db.cursor()
        sql="DELETE FROM STUDENT_INFO WHERE stuid=%s"
        val=(stuid,)
        mycursor.execute(sql,val)
        db.commit()
        print("Record sucessfully deleted")
    except mysql.connector.Error as e:
        print(f"Error :{e}")
    finally:
        db.close()

if __name__== '__main__':



    database_connection()
   
    # create_database()

    # create_table()

    # students=[
    #     ("A","10th",300),
    #     ("B","9th",250),
    #     ("C","8th",200),
    #     ("D","Greduate",300),
    #     ("E","Post-greduate",350),
    #     ("F","PHD",400)

    # ]

    # for stu in students:
    #     insert_record(*stu)

    
    # update_record(1,"G","10th",500)

    # print("\n After Updated")
    # read_data()

    delete_record(1)
    print("\n After deleted")
    read_data()




