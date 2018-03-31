from flask import Flask, request, make_response
from flask import render_template
import json
import urllib2


app = Flask(__name__)

def check_tokeninfo(token):
        URL="https://www.googleapis.com/oauth2/v3/tokeninfo"
        contents=None
        userid=None
        username=None
        try:
                contents = json.loads(urllib2.urlopen(URL+"?id_token="+token).read())
		print contents
        except:
                pass
        if not contents:
                return "not authorised", userid, username, False
        else:
                return token, contents['sub'], contents['given_name'], True





@app.route('/',methods=['GET', 'POST'])
@app.route('/hello.html',methods=['GET', 'POST'])
def hello():
    userid=None
    username=None 
   
    if 'session_token' in request.cookies:
        print request.cookies['session_token']
        token, userid, username,  authorised = check_tokeninfo( request.cookies['session_token'] )
    else:
        print "not authenticated"
        authorised=False

    if not authorised:
        return "<p>Access Denied</p><a href=\"/login.html\">Try again</a>"


    var="here is a variable"
    var_list=[ userid,username ]    
    var_dict={ "listname" : "hello" }  

    return render_template("alex.html", var=var, var_list=var_list, var_dict=var_dict)

@app.route('/login.html')
def login():
    return render_template('login.html')



@app.route('/authorise.html',methods=[ 'POST' ] )
def authorise():
    userid=None
    username=None
    response=make_response("")
    idtoken=request.form['idtoken']
    print idtoken
    token, userid, username, authenticated=check_tokeninfo(idtoken)
    if authenticated:
        print userid, username	
	response.set_cookie('session_token',value=idtoken)	

    return response


