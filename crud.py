import mysql.connector

try:
    db = mysql.connector.connect(
        host ="127.0.0.1",
        user = "root",
        password = "admin"

                                )
    mycursor = db.cursor()
    print("Connection sucessfully")
except:
    print("Not connected to MySQL")

#create database
def create_database():
    try:
        db=mysql.connector.connect(
            host ="127.0.0.1",
            user = "root",
            password = "admin"

        )
        mycursor=db.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS  employee_db")
        print("Database successfully created")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        db.close()

#Create Table
def create_table():
    try:
        db=mysql.connector.connect(
            host ="127.0.0.1",
            user = "root",
            password = "admin",
            database = "employee_db"
        )
        mycursor=db.cursor()
        mycursor.execute("""CREATE TABLE employees_detail (
                         id INT AUTO_INCREMENT PRIMARY KEY,
                         name VARCHAR(255) NOT NULL,
                         designation VARCHAR(255) NOT NULL,
                         age INT NOT NULL
                         )
                         """)
        print("Table created successfully")
    except mysql.connector.Error as err:
        print(f"error {err}")
    finally:
        db.close()

# READ THE DATA FROM TABLE
def read_data():
    try:
        db=mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="admin",
            database="employee_db"
        )
        mycursor=db.cursor()
        mycursor.execute("SELECT * FROM employees_detail")
        result=mycursor.fetchall()
        for row in result:
            print(row)
        print("TABLE SHOW SUCESSFULLY")
    except mysql.connector.Error as err:
        print(f"Error :{err}")
    finally:
        db.close()

#Insert record 
def insert_record(name,designation,age):
    try:
        db=mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="admin",
            database="employee_db"
        )
        mycursor=db.cursor()
        sql="INSERT INTO employees_detail (name,designation,age) VALUES (%s,%s,%s)"
        val=(name,designation,age)
        mycursor.execute(sql,val)
        db.commit()
        print("record sucessfully insert ")
    except mysql.connector.Error as err:
        print(f"error {err}")
    finally:
        db.close()

def update_record(id,name,designation,age):
    try:
        db=mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="admin",
            database="employee_db"
        )
        mycursor=db.cursor()
        sql="UPDATE employees_detail SET name=%s , designation=%s ,age=%s WHERE id=%s"
        val=(name,designation,age,id)
        mycursor.execute(sql,val)
        db.commit()
        print("UPDATE SUCESSFULLY")
    except mysql.connector.Error as err:
        print(f"Error :{err}")
    finally:
        db.close()

#Delete the record 
def delete_record(emp_id):
    try:
        db=mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin',
            database='employee_db'
        )
        mycursor=db.cursor()
        sql="DELETE FROM employees_detail WHERE id=%s"
        val=(emp_id,)
        mycursor.execute(sql,val)
        db.commit()
        print("RECORD DELETED SUCCESSFULLY")
    except mysql.connector.Error as err:
        print(f"{err}")
    finally:
        db.close()



if __name__ == "__main__":
    # create_database()

    #create_table()

    # employee=[
    #     ("John Doe","Software Engineer", 30),
    #     ("Jane Smith", "Data Analyst",28),
    #     ("Mike Johnson", "Project Manager",34),
    #     ("Emily Davis", "HR Manager",43),
    #     ("William Brown", "Intern",25),
    #     ("Linda White", "Team Lead",32),
    #     ("Robert Black","Director",45)
    # ]
    # for emp in employee:
    #     insert_record(*emp)

    
    #read_data()

    #update_record(1,"John Doe","Software Engineer",31)

    # print("\nAfter Update")
    # read_data()

    delete_record(3)

    print("\nAfter Deleted")
    read_data()
