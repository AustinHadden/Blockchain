from flask import Flask, render_template, request
import os
import requests
import sys


app = Flask(__name__)

id_filename = './id.txt'
if os.path.exists(id_filename):
    with open(id_filename, 'r') as f:
        user_id = f.read()
else:
    user_id = None

node = "http://localhost:5000"


@app.route('/')
def root():
    coins = 0
    r = requests.get(url=node+"/chain")
    data = r.json()
    chain = data['chain']
    relevant_transactions = []
    for block in chain:
        transactions = block['transactions']
        for transaction in transactions:
            if transaction['sender'] == user_id:
                coins -= transaction['amount']
                relevant_transactions.append(transaction)
            elif transaction['recipient'] == user_id:
                coins += transaction['amount']
                relevant_transactions.append(transaction)

    return render_template('base.html', title='Home', user_id=user_id,
                            balance=coins, transactions=relevant_transactions)


@app.route('/user', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        global user_id
        if not user_id:
            user_id = request.values['user_id']
            message = f"You've set your ID. Welcome, {user_id}!"
        else:
            user_id = request.values['user_id']
            message = f"You've changed your ID! Your new ID is {user_id}."
    else:
        message = f'Your ID is {user_id}.'
    return render_template('user.html', title='ID', user_id=user_id, message=message)


@app.route('/user/save', methods=['GET'])
def save_id():
    with open(id_filename, 'w') as f:
        f.write(user_id)
    return render_template('save_id.html', title='ID')


if __name__ == '__main__':
    app.run()