import random
from flask import *
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = '' # add secret key

@app.route('/')
def home():
  return render_template('login.html')

@app.route('/getOTP', methods=['POST'])
def getOTP():
  phone_number = request.form['number']
  val = getOTPapi(phone_number)
  if val:
    return render_template('enterOTP.html')

@app.route('/validateOTP', methods=['POST'])
def validateOTP():
  otp = request.form['otp']
  if 'response' in session:
    res = session['response']
    session.pop('response', None)
    if res == otp:
      return 'You are Authorized, Thank You'
    else:
      return 'You are not Authorized, Sorry'

def generateOTP():
  return random.randrange(100000, 999999)

def getOTPapi(phone_number):
  account_sid = '' # add s_id
  auth_token = '' # add auth token
  client = Client(account_sid, auth_token)
  otp = generateOTP()
  session['response'] = str(otp)
  body = 'Your OTP is ' + str(otp)
  message = client.messages.create(
    from_='', # add number
    body=body,
    to=phone_number
  )
  if message.sid:
    return True
  else:
    return False

if __name__ == '__main__':
  app.run(debug=True)