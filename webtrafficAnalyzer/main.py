from datetime import date
import os, sys
from asyncio import tasks
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from scrappers import *
import query


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


def Scrap():
    Searchterms = ['sport']
    for searchterm in Searchterms:
        query.CreateSearchtermTable(db, searchterm)
        res = [str(date.today())] + find_articles.Scrap_all(searchterm)
        query.InsertValues(db, searchterm, res)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        try:
            searchterm = request.form['Searchterm']
            return result(searchterm)
        except:
            pass
    return render_template('home.html')

@app.route('/result', methods=['GET'])
def result(searchterm):
    if request.method == 'GET':
        return redirect('/')
    else:
        try:
            states = [state.replace('.csv', '') for state in os.listdir('cleaned_lists')]
            traficRecords = list(query.QueryValues(db, searchterm))
        except OperationalError:
            traficRecords = []
        finally:
            return render_template('result.html',traficRecords=traficRecords,
                                    states=states, searchterm=searchterm)


if __name__ == "__main__":
    #Scrap()
    app.run(debug=True)