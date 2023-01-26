from hack import app, create_db, db
from flask import render_template, redirect, abort, url_for
from flask_login import current_user, login_user, logout_user, login_required
from hack.forms import LoginForm, RegForm, StudentForm
from hack.models import User
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd 
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import pickle 
from matplotlib import style
from werkzeug.utils import secure_filename
import os

create_db(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = StudentForm()
    page_data = ''
    if form.validate_on_submit():
        data = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'student-mat.csv'), sep=';')
        # print(data.head)
        data = data[['G1','G2','G3','studytime','failures','absences','freetime']]
        data['G1'] = form.g1.data
        data['G2'] = form.g2.data
        data['studytime'] = form.studytime.data
        data['failures'] = form.failures.data
        data['absences'] = form.absences.data
        data['freetime'] = form.freetime.data
        predict = 'G3'
        x = np.array(data.drop(predict, 1))
        y = np.array(data[predict])
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)
        pickle_in = open('hack/static/model/studentmodel.pickle', 'rb')
        linear = pickle.load(pickle_in)
        prd = linear.predict(x_test)
        for i in range(len(prd)):
            if prd[i] > 100:
                prd[i] = 100
            page_data = 'Predicted final grade:', prd[i], 'Data: ',x_test[i]
    return render_template('index.html', form=form, data=page_data)

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    mess=''
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            mess = 'Account already exists'
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            if not current_user.is_authenticated:
                login_user(new_user)
                return redirect('/')
            else:
                return redirect('/admin')
    if current_user.is_authenticated:
        if current_user.username != 'xino':
            return abort(404)
    return render_template('reg.html', form=form, mess=mess)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    mess=''
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            mess = 'Email not found'
        else:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                mess = 'Incorrect password'
    if current_user.is_authenticated:
        return abort(404)

    return render_template('login.html', mess=mess, form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

