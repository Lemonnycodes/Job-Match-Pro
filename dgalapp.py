#Decision model based on Pyomo model
from flask import Flask, request, render_template #importing necessary libraries
import json
import sys
sys.path.append("./lib")
from dgalPy import PyomoModel

app = Flask(__name__)

# Loading job data and sending it to the dgal model
model = PyomoModel()
with open('jsoninput_jobdata.json', 'r') as file:
    jobs = json.load(file)
model.loadthedata(jobs)


@app.route('/', methods=['GET', 'POST']) #establishing flask path to connect with index.html
def index():
    searchperformed = False 
    jobrecommendations = []
    if request.method == 'POST': #Taking all user input from the form
        searchperformed = True
        userinpskills = request.form.get('skills', '').split(',')
        userinpexperience = request.form.get('experience', '0')  #Here I am getting experience as string
        if userinpexperience.isdigit():  #converting to int if user input is digit
            userinpexperience = int(userinpexperience)
        else:
            userinpexperience = 0  # Default to 0 if not a valid number is entered
        userinpmode = request.form.get('mode', 'no preference')
        userinplocation = request.form.get('location', 'anywhere')
        salaryinprange = request.form.get('salary_range', 'no preference')
        requiredskillmatch = request.form.get('skill_match_type', 'any')
        preferredrole = request.form.get('role', '')
        jobrecommendations = model.recommend(userinpskills, userinpexperience, userinpmode, userinplocation,requiredskillmatch, salaryinprange,preferredrole)#passing it to perform the recommendation to the dgalPy file
    return render_template('dgalindex.html', recommendations=jobrecommendations, search_performed=searchperformed,form_data=request.form)#to print the results

if __name__ == '__main__':
    app.run(debug=True)

