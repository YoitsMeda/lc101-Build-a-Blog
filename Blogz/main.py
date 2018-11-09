from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://newblog:things123@localhost:8889/newblog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String (2000))



    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
    blogs= Blog.query.all()

    return render_template('main.html', blogs=blogs)

@app.route('/add',methods=['POST', 'GET'])
def newblog():
    if request.method=='POST':
        title = request.form["Title"]
        body = request.form["Body"]
        newblog = Blog(title,body)
        db.session.add(newblog)
        db.session.commit()
        return redirect('/display?id={}'.format(newblog.id))
    else:
        return render_template("add.html")

@app.route('/display', methods=['GET'])
def display():
    id=request.args.get("id")
    blog = Blog.query.filter_by(id=id).first()
    return render_template('display.html', Title=blog.title, Body=blog.body)


#
# @app.route('/delete-task', methods=['POST'])
# def delete_task():
#
#     task_id = int(request.form['task-id'])
#     task = Task.query.get(task_id)
#     db.session.delete(task)
#     db.session.commit()

if __name__ == '__main__':
    app.run()
