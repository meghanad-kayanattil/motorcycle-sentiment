from flask import Flask, render_template, request, flash, redirect, url_for, Response
import helper_functions as hf
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
plt.style.use('plot_style_mk.mplstyle')
import numpy as np
import motorcycles
import matplotlib

app = Flask(__name__)
app.secret_key = "motorcycle"

# First webpage
@app.route("/home", methods=["POST", "GET"])
def index():
    flash("What is the name of the desired motorcycle?", "1")
    flash("Which sub reddit do you want to search?", "2")
    subreds = ['r/royalenfield','r/Harley','r/motorcycles']
    flash("What time frame do you need the data for?", "3")
    time_frame = ['Last 30 days', 'Last 6 months', 'Last 1 year', 'Last 2 years','Last 3 years','Last 4 years','Last 5 years']
    return render_template("index.html", subreds=subreds, timeframe=time_frame)

# Second web page where most of the analysis happpen
@app.route("/Input", methods=["POST", "GET"])
def input():
    if request.form['name_input']=='':
        return redirect(url_for('index'))
    global bikename
    bikename = str(request.form['name_input'])
    subred_name = str(request.form.get('subreds'))[2:]
    timeframe = request.form.get('timeframe')
    current, begenning = hf.time_frame_calculator(timeframe) 
    moto = motorcycles.motorcycles(bikename, subred_name, current, begenning)
    global example_comment
    global len_comments

    example_comment, len_comments,all_comments = moto.get_comments()

    global senti_label
    global senti_count
    senti_label, senti_count = motorcycles.analysis_huggingface(all_comments)

    if len(all_comments) == 0:
        return redirect(url_for("no_data"))
    else:
        flash(str(request.form['name_input']), "1")
        flash(str(request.form.get('subreds')), "2")
        flash('Please confirm and proceed for data retrival and analysis by pressing on the \'Analyze\' button', "3")
        flash(str(current)+' and '+str(begenning), "4")
        return render_template("display.html")

@app.route("/Analyze", methods=["POST", "GET"])
def analyze():
    flash("The sentiment for "+str(bikename)+" is as shown by anlyzing "+str(len_comments)+" available comments", "1")
    flash("One such comment chosen randomly: ", "2")
    flash(str(example_comment), "3")
    # Generate plot
    cmap = matplotlib.cm.get_cmap('hsv')
    colors = np.zeros([15,4])
    for i in range(15):
        colors[i,:] = cmap(i*0.1)

    fig1 = Figure(figsize=(7,7))
    axis1 = fig1.add_subplot(1, 1, 1)
    # axis1.set_title("EmoRoBERTa model")
    axis1.bar(senti_label, senti_count,alpha=0.5, color = colors)
    axis1.set_ylabel('Count')
    axis1.tick_params(axis='x', rotation=90)
    fig1.tight_layout()

    # Convert plot to PNG image
    pngImage1 = io.BytesIO()
    FigureCanvas(fig1).print_png(pngImage1)
    
    # Encode PNG image to base64 string
    pngImageB64String1 = "data:image/png;base64,"
    pngImageB64String1 += base64.b64encode(pngImage1.getvalue()).decode('utf8')

    return render_template("results.html", image1=pngImageB64String1)

@app.route('/no_data', methods=["POST", "GET"])
def no_data():
    return render_template("no_data.html")