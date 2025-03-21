from flask import Flask, render_template, request, redirect, session
import traceback
import math
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback_secret_key')

@app.route('/')
def home():
    categories = ["Single Person", "Family", "Company"]
    return render_template("homepage.html", categories=categories)

@app.route('/finance')
def finance():
    category = session.get('category', 'single')
    salary = session.get('salary', 0)
    
    def calculate_net_salary(gross):
        social_security = min(gross, 3800) * 0.1378
        tax = (gross - social_security) * 0.10
        taxes = social_security + tax
        return round(gross - social_security - tax, 2), taxes

    net_salary, taxes = calculate_net_salary(salary)

    if category in ['single', 'family']:
        return render_template("finance.html", taxes=taxes, net_salary=net_salary, **session)
    elif category == 'business':
        return render_template("companybudget.html")
    return redirect('/')

@app.route('/budget/<category>', methods=['GET', 'POST'])
def budget(category):
    error = None

    if request.method == 'POST':
        try:
            # Get form data with default 0 if missing
            salary = float(request.form.get('salary', 0))
            expenses = float(request.form.get('expenses', 0))
            additional_income = float(request.form.get('additional_income', 0))
            goal_amount = float(request.form.get('goal_amount', 0))
            goal_description = request.form.get('goal_description', 'reach your goal')
            time_limit_str = request.form.get('time_limit', 0).strip()
            time_limit = math.ceil(float(time_limit_str)) if time_limit_str else 0
            workers = int(request.form.get('workers', 0))
            customers = int(request.form.get('customers', 0))
            gain = float(request.form.get('gain', 0))
            donations = float(request.form.get('donations', 0))

            # Initialize variables
            time_required = 0
            monthly_required = 0
            savings_warning = None  # New variable for the warning message

            # Calculate monthly savings
            monthly_savings = salary + additional_income - expenses

            # Calculate time required or monthly required based on inputs
            if monthly_savings > 0 and goal_amount > 0:
                if time_limit > 0:
                    monthly_required = goal_amount / time_limit
                    # Check if monthly savings is less than what's required
                    if monthly_savings < monthly_required:
                        savings_warning = f"You cannot save {goal_amount} in {time_limit} months with your current income and expenses."
                    time_required = time_limit
                else:
                    time_required = math.ceil(goal_amount / monthly_savings)
                    monthly_required = monthly_savings

            # Store data in session
            session['salary'] = salary
            session['expenses'] = expenses
            session['additional_income'] = additional_income
            session['monthly_savings'] = monthly_savings
            session['goal_amount'] = goal_amount
            session['goal_description'] = goal_description
            session['time_limit'] = time_limit
            session['time_required'] = time_required
            session['monthly_required'] = monthly_required
            session['category'] = category
            session['workers'] = workers
            session['customers'] = customers
            session['gain'] = gain
            session['donations'] = donations
            session['savings_warning'] = savings_warning  # Add warning to session

            return redirect("/finance")
        except ValueError as e:
            error = "Please enter valid numbers for all fields."

    return render_template("budget.html", category=category, error=error)

if __name__ == '__main__':
    app.run(debug=True)