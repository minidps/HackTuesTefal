from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def home():
    categories = ["Single Person", "Couple", "Family", "Company"]
    return render_template("home.html", categories=categories)

@app.route('/budget/<category>', methods=['GET', 'POST'])
def budget(category):
    result = None
    if request.method == 'POST':
        try:
            salary = float(request.form.get('salary', 0))
            expenses = float(request.form.get('expenses', 0))
            additional_income = float(request.form.get('additional_income', 0))
        except ValueError:
            salary, expenses,additional_income = 0, 0, 0
        
        
        # Goal fields
        try:
            goal_amount = float(request.form.get('goal_amount', 0))
        except ValueError:
            goal_amount = 0

        goal_description = request.form.get('goal_description', "reach your goal")
        
        calculation_type = request.form.get('calculation_type')
        if calculation_type == 'time':
            try:
                monthly_savings = salary + additional_income - expenses
                if monthly_savings > 0:
                    time_required = goal_amount / monthly_savings
                    result = f"It will take approximately {time_required:.1f} months to {goal_description}."
                else:
                    result = "Please enter a valid monthly savings amount."
            except ValueError:
                result = "Invalid monthly savings input."
        elif calculation_type == 'monthly':
            try:
                time_limit = float(request.form.get('time_limit', 0))
                if time_limit > 0:
                    monthly_required = goal_amount / time_limit
                    if monthly_required<=salary + additional_income:
                        result = f"You need to save approximately {monthly_required:.2f} per month to {goal_description} in {time_limit} months."
                    elif monthly_required>=salary + additional_income:
                        result = f"With your current income you wouldn't be able to get to your goal for the given time. You need to save approximately {monthly_required:.2f} per month to {goal_description} in {time_limit} months."
                else:
                    result = "Please enter a valid time limit."
            except ValueError:
                result = "Invalid time limit input."
    
    return render_template("budget.html", category=category, result=result)

if __name__ == '__main__':
    app.run(debug=True)
