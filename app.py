from flask import Flask, render_template, request, url_for
from flaskext.mysql import MySQL
 
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '12345678'
app.config['MYSQL_DATABASE_DB'] = 'flask'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn=mysql.connect()
c = conn.cursor()
c.execute('SELECT Product_Name, Price FROM PRODUCT')
data = c.fetchall()     
checklist = []
checklist1= []
subtotal=0
count=1
@app.route("/")
def main():
    global count
    count=1
    return render_template('index.html',data=data,count=count)

@app.route('/handle_data', methods=['POST'])
def handle_data():
    global subtotal
    global count
    count=count+1
    productname = request.form['itemname']
    productqty =  request.form['quantity']
    c.execute("Update Product SET Quantity= Quantity-%s WHERE Product_Name='%s' " % (productqty,productname))
    conn.commit()    
    c.execute('SELECT * FROM Product')
    row = c.fetchone()
    while row is not None:
         checklist.append(row[0])
         checklist1.append(row[1])
         row=c.fetchone()
    i=0
    while (i<len(checklist)):
        if checklist[i]==productname:
            checklist1[i]=int(checklist1[i])
            productqty=int(productqty)
            subtotal = subtotal+checklist1[i]*productqty
            break;
        i=i+1
    print(subtotal)   
    return render_template('index.html',data=data,count=count)

@app.route('/checkout')
def checkout():
    global subtotal
    print(subtotal)
    return render_template('checkout.html',subtotal=subtotal)

if __name__ == "__main__":
    app.run()

