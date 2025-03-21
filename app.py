from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    categories = ["Single Person", "Family", "Company"]
    return render_template("homepage.html", categories=categories)

@app.route('/budget/<category>', methods=['GET', 'POST'])
def budget(category):
    render_template('budget.html')
    result = None
    error = None

    if request.method == 'POST':
        try:
            salary = float(request.form.get('salary', 0))
            expenses = float(request.form.get('expenses', 0))
            additional_income = float(request.form.get('additional_income', 0))
            goal_amount = float(request.form.get('goal_amount', 0))
            time_limit = float(request.form.get('time_limit', 0))
            
            if salary < 0 or expenses < 0 or additional_income < 0 or goal_amount < 0 or time_limit < 0:
                raise ValueError("Values cannot be negative.")
        except ValueError:
            error = "Please enter valid positive numbers for all fields."
            return render_template("budget.html", category=category, result=result, error=error)
        
        goal_description = request.form.get('goal_description', "reach your goal")
        calculation_type = request.form.get('calculation_type')
        
        monthly_savings = salary + additional_income - expenses
        
        if calculation_type == 'time':
            if monthly_savings > 0:
                time_required = goal_amount / monthly_savings
                result = f"It will take approximately {time_required:.1f} months to {goal_description}."
            else:
                result = "Your monthly savings must be greater than zero to calculate time."
        
        elif calculation_type == 'monthly':
            if time_limit > 0:
                monthly_required = goal_amount / time_limit
                if monthly_required <= monthly_savings:
                    result = f"You need to save approximately {monthly_required:.2f} per month to {goal_description} in {time_limit} months."
                else:
                    result = f"With your current income, you cannot reach your goal in the given time. You need to save {monthly_required:.2f} per month."
            else:
                error = "Please enter a valid time limit greater than zero."
    
    return render_template("budget.html", category=category, result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)
