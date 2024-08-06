from flask import Flask,redirect,url_for,request,render_template,jsonify
#Account creation
'''
users={username,phonenumber,pinnumber,Amount}
user={
    'user1':{accno:[pinno,amount]},
    'user2':{accno:[pinno,amount]},
    'user3':{accno:[pinno,amount]}
}
route one -- enter account number
route two -- options- balance, withdraw,deposit
route three --balance showing amount
route four --withdraw validation and updation the amount
route five --deposit amount entering and updating the amount
'''

app=Flask(__name__)

accounts={'123456':{'pin':'111','balance':30000},
         '123457':{'pin':'112','balance':40000},
         '123458':{'pin':'113','balance':20000},
         '123459':{'pin':'114','balance':1000}}

@app.route('/',methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        account = request.form["Account_number"]
        pin = request.form["Pin"]
        initial_balance = request.form.get('balance',0)
        if account in accounts:
            #print(accounts[account].get('balance'))
            return 'Account already existed',400
        accounts[account]={'pin':pin,'balance':initial_balance}
        #print(accounts)
        return "Account created successfully"
    return render_template('index.html')

@app.route('/all')
def all_accounts():
    l=[{'account':acco , 'balance': details['balance']} for acco,details in accounts.items()]
    #print(l)
    return l
'''
@app.route('/data', methods=['POST'])
def data():
    data = dict(request.form)
    print(data)
    return 'Ok'
'''

@app.route('/alreadyacc',methods = ['GET','POST'])
def alreadyacc():
    if request.method == 'POST':
        account = request.form["Account_number"]
        pin = request.form["Pin"]
        if account in accounts and pin == accounts[account].get('pin'):
            #print("Account exist")
            #return 'Account exist'
            data=(account,pin)
            return redirect(url_for('panel',account=account,pin =pin))
        else:
            return 'Invalid Details'
    
    return render_template('Login.html')

@app.route('/panel/<account>/<pin>')
def panel(account,pin):
    #print(data)
    return render_template('panel.html',account=account,pin =pin)

@app.route('/deposit/<account>/<pin>',methods=['GET','POST'])
def deposit(account,pin):
    
    if request.method == 'POST':
        amount = int(request.form['amount'])
        #print(amount)
        accounts[account]['balance']=accounts[account]['balance'] + amount
        balance = accounts[account]['balance']
        return render_template('balance.html',balance=balance,account=account)
    return render_template('deposit.html')


@app.route('/withdraw/<account>/<pin>',methods=['GET','POST'])
def withdraw(account,pin):
    if request.method == 'POST':
        amount = int(request.form['amount'])
        #print(amount)
        if accounts[account]['balance'] > amount:
            accounts[account]['balance']=accounts[account]['balance'] - amount
        balance = accounts[account]['balance']
        return render_template('balance.html',balance=balance,account=account)
    return render_template('withdraw.html')

@app.route('/balance/<account>/<pin>') # type: ignore
def balance(account,pin):
    if account in accounts and pin == accounts[account].get('pin'):
        balance = accounts[account]['balance']
        return  render_template('balance.html',balance=balance,account=account)

app.run(debug=True,use_reloader=True)