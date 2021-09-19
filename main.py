from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
import numpy as np
import datetime
import os, csv, uuid
import re
from optimize import general_optimize_iterated

#
#########
# Links #
#########
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route('/test', methods=['POST'])
def test():
    print(dict(request.form))
    return "Test"

@app.route('/results', methods=['GET', 'POST'])
def results():
    print("fuck")
    print(dict(request.form))
    names, compat = extract_data(dict(request.form))
    mps = np.ceil(compat)
    best = general_optimize_iterated(compat, mps)
    pairs = []
    for x, y in best:
        pairs.append((names[x], names[y]))
    print(pairs)
    return render_template("results.html", pairs=pairs)


def extract_data(form_dict):
    print(form_dict)
    name_nums = [key[6] for key in form_dict.keys() if key.startswith("name")]
    N = len(name_nums)
    names = ["Ford", "Lexus", "BMW", "Honda"]
    for i in name_nums:
        names.append(form_dict["names[" + str(i) + "]"])

    compat = np.zeros([2*N, 2*N])
    for i in range(N):
        for j in range(N):
            if i != j:
                num_string = name_nums[j]
                compat[i, j] = int(form_dict["compat[" + str(i) + "][" + num_string + "]"]) * 0.01
    return names, compat

if __name__ == '__main__':
    app.run(debug=True)
