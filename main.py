from tools import sum

from flask import Flask, send_file, render_template
import numpy as np
import matplotlib.pyplot as plt
import base64
import io


app = Flask(__name__)

@app.route("/")
def hello_world():
    c = sum(1,2)


    return f"<p style='color:red'>Hello, World!</p>"


@app.route("/web_sum")
def web_sum():
    c = sum(1,2)
    nums = list(range(100))

    return f"<p>c= {c}</p>"


@app.route('/post/<float:post_id>')
def show_post(post_id):
    
    with open("data.txt", "a") as file:
        file.write(f"{post_id}\n")

        return f'Saved {post_id}!!'


@app.route('/read')
def read_post():
    
    with open("data.txt", "r") as file:
        data = file.readlines()

        return f'data: {data}!!'


@app.route('/plot')
def plot_data():
    # Step 1: Read data from a file (adjust this according to your file format)
    # For example, if it's a CSV file, you might use pandas to read it
    data = np.loadtxt('data.txt')  # Replace with your file path and reading method

    # Step 2: Generate the plot
    plt.figure()
    plt.plot(data)  # Adjust this according to how you want to plot your data
    plt.xlabel('X-axis label')
    plt.ylabel('Y-axis label')
    plt.title('Your Plot Title')

    # Step 3: Save plot to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Step 4: Return the buffer in the response
    return send_file(buf, mimetype='image/png')


@app.route('/show_plot')
def show_plot():
    # Generate the plot (same as before)
    data = np.loadtxt('data.txt')
    plt.figure()
    plt.plot(data)
    plt.xlabel('X-axis label')
    plt.ylabel('Y-axis label')
    plt.title('Your Plot Title')

    # Convert plot to a base64 string
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Render HTML template with base64 image
    return render_template('plot_template.html', image=base64_img)
