import os
import pandas as pd
from helpers import get_data, graph, get_path, apology
from flask import Flask, render_template, request, redirect

#list of paths that answer possible queries
paths = []
paths.append(get_path('EMPLOYMENT','Civilian','Employed'))
paths.append(get_path('EMPLOYMENT','Civilian','Unemployed'))
paths.append(get_path('COMMUTING','alone',''))
paths.append(get_path('COMMUTING','carpooled',''))
paths.append(get_path('INCOME','Median',''))
paths.append(get_path('INCOME','Mean',''))
paths.append(get_path('INCOME','Less',''))
paths.append(get_path('HEALTH','With',''))
paths.append(get_path('HEALTH','No',''))

#list of possible queries
queries = [
'What is the number of American civilians who were employed?',
'What is the number of American civilians who were unemployed?',
'What is the number of American commuters who drove to work alone?',
'What is the number of American commuters who carpooled to work?',
'What is the median American household income?',
'What is the mean American household income?',
'What is the number of American households with annual income under $10,000?',
'What is the number of Americans with health insurance?',
'What is the number of Americans without health insurance?',
]

# Configure application
app = Flask(__name__)


@app.route("/")
def index():
    """Display homepage"""
    return render_template("index.html")

@app.route("/query", methods=["GET", "POST"])
def query():
    """Submits query for graph"""

    # user reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("query.html", queries=queries)

    # user reached route via POST (as by submitting a form via POST)
    else:

        # ensure query was submitted
        q = request.form.get("queries")
        if not q:
            return apology("Apologies, a query must be selected!", 400)

        else:
            #find index of query
            index = 0
            for i in range(len(queries)):
                if q == queries[i]:
                    index = i

            #use index to get path of query, which we then plug into function to get data
            data = get_data(paths[index])

            #create new graph, then edit html file to display png image of this graph back to user
            graph(data)

            #display page back to user
            return render_template('graph.html', queries=queries, q=q)


@app.route("/graph", methods=["GET", "POST"])
def graphed():
    """Graph based on query submission"""

    # user reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("graph.html", queries=queries, q=q)

    # user reached route via POST (as by submitting a form via POST)
    else:
        #pull query from user
        q = request.form.get("queries")

        #find index of query
        index = 0
        for i in range(len(queries)):
            if q == queries[i]:
                index = i

        #use index to get path of query, which we then plug into function to get data
        data = get_data(paths[index])

        #create new graph, then edit html file to display png image of this graph back to user
        graph(data)
        # redirect to query page
        return render_template("graph.html", queries=queries, q=q)

if __name__ == "__main__":
    app.run()