from flask import render_template, flash, redirect, send_file, make_response, url_for, Response
from app import app
from app import forms, functions

#Pandas and Matplotlib
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#other requirements
import io


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/')
def home():
    tips = functions.get_tips()
    revenue = functions.get_revenue_by_date()
    average_check = functions.get_average_check()
    guests = functions.get_guests_by_date()
    return render_template("index.html", tips=tips, revenue=revenue, average_check=average_check, guests=guests)


@app.route('/tips')
def tips():
    tips = functions.get_tips()
    revenue = None
    average_check = None
    guests = None
    return render_template("index.html", tips=tips, revenue=revenue, average_check=average_check, guests=guests)


@app.route('/revenue')
def revenue():
    tips = None
    revenue = functions.get_revenue_by_date()
    average_check = functions.get_average_check()
    guests = None
    return render_template("index.html", tips=tips, revenue=revenue, average_check=average_check, guests=guests)


@app.route('/analytics')
def analytics():
    tips = None
    revenue = None
    average_check = None
    guests = functions.get_guests_by_date()
    return render_template("index.html", tips=tips, revenue=revenue, average_check=average_check, guests=guests)


@app.route('/tips_by_date')
def tips_by_date():
    results = functions.get_tips()
    return render_template("tips_by_date.html", tips=results)


@app.route('/plot_revenue_by_date.png')
def plot_revenue_by_date_png():
    plot_revenue_by_date = functions.plot_get_revenue_by_date()
    fig = functions.create_figure(plot_revenue_by_date['dates'], plot_revenue_by_date['revenue'])
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/plot_revenue_by_hour.png')
def plot_revenue_by_hour_png():
    plot_revenue_by_date = functions.plot_get_revenue_by_hour_of_date()
    fig = functions.create_figure(plot_revenue_by_date['hours'], plot_revenue_by_date['revenue'])
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')



