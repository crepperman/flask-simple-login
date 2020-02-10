
from flask_bootstrap import Bootstrap
from flask import Flask, Response, redirect, url_for, request, session, abort ,render_template
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import json

app = Flask(__name__)


# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'simple-login'
)

bootstrap = Bootstrap()

# flask-login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


@app.route('/')
def hello_world():
    #return 'Hello World!'
    return render_template('index.html',alert="index")


@app.route('/register',methods=['POST','GET'])
def register():
    with open('./member.json','r') as file_object:
        member = json.load(file_object)
    if request.method == 'POST':
        print("reg")
        print(request)
        if request.values['userid'] in member:
            if request.values['send'] == 'register':
                for find in member:
                    if member[find]['nick'] == request.values['username']:
                        return render_template('register.html', alert='this account and nickname are used.')
        else:
            for find in member:
                if member[find]['nick'] == request.values['username']:
                    return render_template('register.html', alert='this nickname are used.',id=request.values['userid'], pw=request.values['pwd'])

            member[request.values['userid']] = {'password': request.values['userpwd'],'nick': request.values['username']}
            with open('./member.json', 'w') as outfile:
                json.dump(member, outfile)
            return render_template('index.html')
    else:
        return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        print("POST")
        with open('./member.json', 'r') as file_object:
            member = json.load(file_object)
        print(request.values['userid'],)
        if request.values['userid'] in member:
            if member[request.values['userid']]['password']==request.values['userpwd']:
                session['username'] = request.values['userid']
                return render_template('index.html', alert="Logined")
            else:
                return render_template('index.html',alert="Your password is wrong, please check again!")
        else:
            return render_template('index.html',alert="Your account is unregistered.")
    else:
        return render_template('index.html')


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)

if __name__ == '__main__':
    app.run()
    bootstrap.init_app(app)
    login_manager.init_app(app)
