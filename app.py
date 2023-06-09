from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db =SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    action_type = db.Column(db.String(50), nullable = False )
    date_created = db.Column(db.DateTime, default= datetime.utcnow)
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=["POST","GET"])
def index():
    if request.method=="POST":
        task_content = request.form['content']
        new_task = Todo(action_type=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was a Problem"


    else:
        tasks= Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/history/')
    except:
        return "Unable to delete that event"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.action_type = request.form['content']
        try:
            db.session.commit()
            return redirect('/history/')
        except:
            return "unable to update event"

    else:
        return render_template('update.html', task=task)

@app.route('/history/', methods=['GET', 'POST'])
def history():
    if request.method=="POST":
        task_content = request.form['content']
        new_task = Todo(action_type=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/history/')
        except:
            return "There was a Problem"


    else:
        tasks= Todo.query.order_by(Todo.date_created).all()
        return render_template("history.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)

