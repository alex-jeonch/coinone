import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import User
from flask import session
from flask_wtf.csrf import CSRFProtect
from Forms import RegisterForm, LoginForm

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def main():
    if 'userid' in session:
        return render_template('main.html')
    return render_template('main.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userid = request.form.get('userid')
        email = request.form.get('email')
        password = request.form.get('password')
        #re_password = request.form['re-password']

        #if (userid and email and password and re_password) and password == re_password:
        fcuser = User()
        fcuser.userid = userid
        fcuser.email = email
        fcuser.password = password

        db.session.add(fcuser)
        db.session.commit()

        return redirect('/')


    return render_template('register.html')


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm() #로그인폼
    if form.validate_on_submit(): #유효성 검사
        print('{}가 로그인 했습니다'.format(form.data.get('userid')))
        session['userid'] = form.data.get('userid') #form에서 가져온 userid를 세션에 저장
        return redirect('/') #성공하면 main.html로
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')


if __name__ == "__main__":
    # 데이터베이스---------
    basedir = os.path.abspath(os.path.dirname(__file__))  # 현재 파일이 있는 디렉토리 절대 경로
    dbfile = os.path.join(basedir, 'db.sqlite')  # 데이터베이스 파일을 만든다

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 사용자에게 정보 전달완료하면 teadown. 그 때마다 커밋=DB반영
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 추가 메모리를 사용하므로 꺼둔다
    app.config['SECRET_KEY'] = 'hard to guess string'

    #    db = SQLAlchemy() #SQLAlchemy를 사용해 데이터베이스 저장
    db.init_app(app)  # app설정값 초기화
    db.app = app  # Models.py에서 db를 가져와서 db.app에 app을 명시적으로 넣는다
    db.create_all()  # DB생성

    app.run(host="127.0.0.1", port=5000, debug=True)