from flask import Flask, render_template, request, redirect, session
import traceback

app = Flask(__name__)
app.secret_key = 'your_muihihi_secret_key_here'

@app.route('/')
def home():
    categories = ["Single Person", "Family", "Company"]
    return render_template("asdasdasd.html", categories=categories)

@app.route('/finance')
def finance():
    # Retrieve data from session
    finance_data = {
        'salary': session.get('salary', 0),
        'expenses': session.get('expenses', 0),
        'additional_income': session.get('additional_income', 0),
        'monthly_savings': session.get('monthly_savings', 0),
        'goal_amount': session.get('goal_amount', 0),
        'goal_description': session.get('goal_description', 'reach your goal'),
        'time_limit': session.get('time_limit', 0),
        'monthly_required': session.get('monthly_required', '')
    }
    return render_template("finance.html", **finance_data)

@app.route('/budget/<category>', methods=['GET', 'POST'])
def budget(category):
    result = None
    error = None

    if request.method == 'POST':
        try:
            # Get form data with default 0 if missing
            salary = float(request.form.get('salary', 0))
            expenses = float(request.form.get('expenses', 0))
            additional_income = float(request.form.get('additional_income', 0))
            goal_amount = float(request.form.get('goal_amount', 0))
            time_limit_str = request.form.get('time_limit', 0).strip()
            time_limit =float(time_limit_str) if time_limit_str else 0

            # Validate non-negative inputs
            if any(value < 0 for value in [salary, expenses, additional_income, goal_amount, time_limit]):
                raise ValueError("All values must be positive numbers.")

            # Get optional fields
            goal_description = request.form.get('goal_description', "reach your goal")
            calculation_type = request.form.get('calculation_type')

            # Calculate monthly savings
            monthly_savings = salary + additional_income - expenses

            if goal_amount <= 0:
                result = f"You don't need to save anything to {goal_description}."
            elif monthly_savings <= 0:
                result = "You cannot reach your goal with your current income and expenses."
            else:
                time_required = goal_amount / monthly_savings
                result = f"It will take approximately {time_required:.1f} months to {goal_description}."

            
            if time_limit <= 0:
                error = "Time limit must be greater than zero."
            else:
                monthly_required = goal_amount / time_limit
                if monthly_required <= monthly_savings:
                    result = f"You need to save approximately {monthly_required:.2f} per month to {goal_description} in {time_limit} months."
                else:
                    result = f"You need {monthly_required:.2f} per month, but you only save {monthly_savings:.2f}. Adjust your income or expenses."


            # Store data in session
            session['salary'] = salary
            session['expenses'] = expenses
            session['additional_income'] = additional_income
            session['monthly_savings'] = monthly_savings
            session['goal_amount'] = goal_amount
            session['goal_description'] = goal_description
            session['time_limit'] = time_limit
            session['monthly_required'] = monthly_required if monthly_required else error

            return redirect("/finance")
        except ValueError as e:
            error = str(e) + traceback.format_exc() if str(e) else "Please enter valid numbers for all fields."

    return render_template("budget.html", category=category, result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)