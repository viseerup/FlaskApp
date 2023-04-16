from flask import Flask, render_template, url_for, request, redirect
import flask_monitoringdashboard as dashboard
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
import os

app = Flask(__name__)
#dashboard.bind(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://chckkmjn:IIXUrHBVSTEIg-Ux6vQ-DH6NIfG1hV7u@hattie.db.elephantsql.com/chckkmjn'
#db = SQLAlchemy(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mydatabase.db')
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    


with app.app_context():
    try:
        db.create_all()
        app.logger.info('Database tables created successfully.')
    except Exception as e:
        app.logger.error(f'Error creating database tables: {e}')




@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)



if __name__ == "__main__":
    app.run(debug=True)