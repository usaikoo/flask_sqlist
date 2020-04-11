from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy 
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///mydb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(200))
    lastname = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = User.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>',methods=["GET","POST"])
def update(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.firstname = request.form['firstname']
        user.lastname = request.form['lastname']
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.commit()
        return redirect('/')
    else:
        users = User.query.all()
        page ='updatehome'
        return render_template('home.html',page=page,users=users,user=user)

@app.route('/', methods=['GET','POST'])
def get():
    if request.method == "GET":
        users = User.query.all()
        page ='home'
        user = User(firstname='',lastname='',email='',password='')
        return render_template('home.html',users=users,page=page,user=user)
    else:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        newUser = User(firstname=firstname,lastname=lastname,email=email,password=password)
        db.session.add(newUser)
        db.session.commit()
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)