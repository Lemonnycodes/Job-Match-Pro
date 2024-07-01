import pyomo.environ as pyo
from pyomo.environ import ConcreteModel, Var, ConstraintList, RangeSet, SolverFactory, minimize, maximize
from pyomo.opt import SolverStatus, TerminationCondition
import logging
import json
import csv
import re

logging.basicConfig(filename="dgal_debug.log", level=logging.DEBUG)

class PyomoModel:
    def __init__(self):
        self.model = None
        self.data = []

    def loadthedata(self, data):
        #Loading and preprocessing the data to model.
        self.data = data
        #print("Sample job entry",self.data[0])
        logging.info("Data loaded successfully.")

    def setupthemodel(self):
        #Seting up the Pyomo model with the required variables and parameters.
        self.model = ConcreteModel()
        self.model.realI = RangeSet(0, len(self.data)-1)
        self.model.intI = RangeSet(0, len(self.data)-1)
        self.model.real = Var(self.model.realI, domain=pyo.Reals)
        self.model.int = Var(self.model.intI, domain=pyo.Integers)
        logging.info("Model setup is complete.")

    def define_constraints(self):
        #Defing the model constraints"
        self.model.constraints = ConstraintList()
        for i in self.model.realI:
            self.model.constraints.add(self.model.real[i] >= 0)  
        logging.info("Constraints defined.")

    def solve(self):
        #Solving the optimization model.
        solver = SolverFactory('glpk')
        result = solver.solve(self.model, tee=True)
        self._process_results(result)

    def _process_results(self, result):
        #Process the optimization results and handle possible output"""
        if result.solver.status == SolverStatus.ok and result.solver.termination_condition == TerminationCondition.optimal:
            logging.info("Optimization successful.")
        elif result.solver.termination_condition == TerminationCondition.infeasible:
            logging.info("Model is infeasible.")

    def skill_match(self, job_skills, user_skills):
        #extracting skills has one whole word
        pattern = r'\b(' + '|'.join(re.escape(skill.strip().lower()) for skill in user_skills) + r')\b'
        return bool(re.search(pattern, job_skills.lower()))

    def recommend(self, user_skills, user_experience, user_mode, user_location, skill_match_type, salary_range,preferred_role ):
        #Giving job recommendations based on the user requirement
        self.setupthemodel()
        self.define_constraints()
        self.solve()
        return self.filter_jobs(user_skills, user_experience, user_mode, user_location, skill_match_type, salary_range,preferred_role)


    @staticmethod
    def checkingthesalaryrange(salary_range): 
        if salary_range == 'no preference':
            return 0, float('inf')  
        elif salary_range == '150001-':
            return 150001, float('inf')  #
        else:
            parts = salary_range.split('-')
            return int(parts[0]), int(parts[1])

    def filter_jobs(self, user_skills, user_experience, user_mode, user_location, skill_match_type, salary_range,preferred_role ):
        filtered_jobs = []
        salary_min, salary_max = self.checkingthesalaryrange(salary_range)
        for job in self.data:
            
            try:
                job_salary = int(job['Salary'].replace('$', '').replace(',', ''))
            except ValueError:
                print("Invalid salary data for job ID:", job['Job ID'])
                continue

            if skill_match_type == "all":
                if not all(self.skill_match(job['Skills'], [skill]) for skill in user_skills):
                    continue
            elif skill_match_type == "any":
                if not any(self.skill_match(job['Skills'], [skill]) for skill in user_skills):
                    continue

            if not (job['Location'] == user_location or user_location == "anywhere"):
                continue
            if not (job['Mode of Work'] == user_mode or user_mode == "no preference"):
                continue
            if not (job['Years of Experience'] <= user_experience):
                continue
            if not (salary_min <= job_salary <= salary_max):
                continue
            if preferred_role and not preferred_role.lower() in job['Job Title'].lower():
                continue
            skillsconcat = ', '.join(job['Skills']) if isinstance(job['Skills'], list) else job['Skills']#joining skills that were seperated as indvidual letters
            job_info = {
                'job_id': job['Job ID'],
                'title': job['Job Title'],
                'experience': job['Years of Experience'],
                'skills': skillsconcat,
                'salary': job['Salary'],
                'location': job['Location'],
                'mode_of_work': job['Mode of Work']
            }
            filtered_jobs.append(job_info)

        return filtered_jobs
