from flask import Flask, request, jsonify, render_template
import re
import sympy as sp
import math

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Function to convert usual math symbols to Python-readable format
def convert_to_python_expression(expression):
    expression = expression.replace('×', '*')
    expression = expression.replace('÷', '/')
    expression = re.sub(r'(\d+)\^(\d+)', r'\1**\2', expression)
    expression = re.sub(r'√(\d+)', r'sp.sqrt(\1)', expression)
    return expression

# Function to parse and solve the expression
def solve_math_expression(expression):
    try:
        python_expression = convert_to_python_expression(expression)
        print(f"Converted expression: {python_expression}")
        result = sp.sympify(python_expression)
        return result
    except Exception as e:
        return str(e)

# Route to handle math tasks
@app.route('/solve', methods=['GET', 'POST'])
def solve_tasks():
    if request.method == 'POST':
        math_tasks = request.form.get('math_tasks', '')
        if not math_tasks:
            return jsonify({"error": "No math tasks provided."}), 400

        tasks = [task.strip() for task in re.split(r'[;\n]+', math_tasks) if task.strip()]
        results = {task: str(solve_math_expression(task)) for task in tasks}

        return render_template('results.html', results=results)

    return render_template('upload.html')

# Compound interest calculation function
def calculate_compound_interest(principal, rate, time, frequency):
    try:
        amount = principal * (1 + rate / frequency) ** (frequency * time)
        interest = amount - principal
        return {"amount": round(amount, 2), "interest": round(interest, 2)}
    except Exception as e:
        return str(e)

# Route for compound interest form
@app.route('/compound_interest', methods=['GET', 'POST'])
def compound_interest():
    if request.method == 'POST':
        try:
            principal = float(request.form.get('principal', 0))
            rate = float(request.form.get('rate', 0)) / 100
            time = float(request.form.get('time', 0))
            frequency = int(request.form.get('frequency', 1))

            result = calculate_compound_interest(principal, rate, time, frequency)
            return render_template('compound_result.html', result=result)
        except ValueError:
            return jsonify({"error": "Please enter valid numbers."}), 400

    return render_template('compound_form.html')

# Pension savings calculation function
@app.route('/pension_savings', methods=['GET', 'POST'])
def pension_savings():
    if request.method == 'POST':
        try:
            current_age = int(request.form.get('current_age'))
            retirement_age = int(request.form.get('retirement_age'))
            monthly_savings = float(request.form.get('monthly_savings'))
            annual_return = float(request.form.get('annual_return')) / 100

            years_to_save = retirement_age - current_age
            total_months = years_to_save * 12
            future_value = 0

            for month in range(1, total_months + 1):
                future_value += monthly_savings * (1 + annual_return / 12) ** (total_months - month)

            return render_template('pension_result.html', total_savings=round(future_value, 2))
        except ValueError:
            return jsonify({"error": "Invalid input. Please enter valid numbers."}), 400

    return render_template('pension_savings.html')

# Mortgage calculator function
@app.route('/mortgage_calculator', methods=['GET', 'POST'])
def mortgage_calculator():
    if request.method == 'POST':
        try:
            principal = float(request.form.get('principal'))
            annual_rate = float(request.form.get('annual_rate')) / 100  # Convert to decimal
            years = int(request.form.get('years'))

            # Calculate monthly rate
            monthly_rate = annual_rate / 12
            number_of_payments = years * 12

            # Calculate monthly payment using the mortgage formula
            monthly_payment = (principal * monthly_rate * math.pow(1 + monthly_rate, number_of_payments)) / \
                              (math.pow(1 + monthly_rate, number_of_payments) - 1)

            return render_template('mortgage_result.html', monthly_payment=round(monthly_payment, 2))
        except ValueError:
            return jsonify({"error": "Invalid input. Please enter valid numbers."}), 400

    return render_template('mortgage_calculator.html')

if __name__ == '__main__':
    app.run(debug=True)



