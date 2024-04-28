from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
app = Flask(__name__)

#MySQL config
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='users'
mysql=MySQL(app)

# Endpoint root
@app.route('/')
def home():
    return "Selamat datang di API sederhana!"

# Endpoint untuk mendapatkan informasi pengguna berdasarkan ID
@app.route('/users',methods=['GET', 'POST'])
def get_user():
    if request.method == 'GET':
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT * FROM users")

        #Get coloumn names from cursor.description
        column_names=[i[0] for i in cursor.description]

        #Fetch data and format into list of dictionaries
        user=[]
        for row in cursor.fetchall():
            user.append(dict(zip(column_names,row)))
        
        return jsonify(user)
    
        cursor.close()
    elif request.method == 'POST':
        # get data from request
        name = request.json['name']
        age = request.json['age']
        email = request.json['email']

        #open connection and insert to DB
        cursor=mysql.connection.cursor()
        sql= "INSERT INTO users (name, age, email) VALUES (%s, %s, %s)"
        val = (name, age, email)
        cursor.execute(sql,val)

        mysql.connection.commit()

        return jsonify({'message': 'data added successfully'})
        cursor.close()

@app.route('/detailuser', methods=['GET'])
def get_detailuser():
    if 'id' in request.args:
        cursor=mysql.connection.cursor()
        sql="SELECT * FROM users WHERE id = %s"
        val= (request.args['id'])
        cursor.execute(sql,val)
        #Get coloumn names from cursor.description
        column_names=[i[0] for i in cursor.description]

        #Fetch data and format into list of dictionaries
        user= []
        for row in cursor.fetchall():
            user.append(dict(zip(column_names,row)))
        
        return jsonify(user)
 
    cursor.close()

@app.route('/deleteuser', methods=['DELETE'])
def deleteuser():
    if 'id' in request.args:
        cursor=mysql.connection.cursor()
        sql="DELETE FROM users WHERE id = %s"
        val= (request.args['id'])
        cursor.execute(sql,val)

        mysql.connection.commit()

        return jsonify({'message': 'data deleted successfully'})
        cursor.close()
@app.route('/edituser', methods=['PUT'])
def edituser():
    if 'id' in request.args:
        data= request.get_json()
        cursor=mysql.connection.cursor()
        sql="UPDATE users SET name=%s, age=%s, email=%s WHERE id=%s "
        val= (data['name'], data['age'], data['email'], request.args['id'])
        cursor.execute(sql,val)

        mysql.connection.commit()

        return jsonify({'message': 'data updated successfully'})
        cursor.close()
    # else:
    #     return jsonify({"error": "Pengguna tidak ditemukan"}), 404


# Menjalankan server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='50',debug=True)
