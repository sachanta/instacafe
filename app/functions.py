from flask import render_template, flash, redirect
from sqlalchemy import create_engine, select, MetaData, Table, and_, func, cast, Date
from app import app
from app import forms

#Pandas and Matplotlib
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#other requirements
import io


def create_figure(x,y):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.patch.set_facecolor('#E8E5DA')

    ax.bar(x, y, color="#304C89")

    plt.xticks(rotation=30, size=10)
    plt.ylabel("Revenue", size=12)

    return fig

def get_average_check():
    average_check = {}
    connection, table = get_connection()
    stmt = select(cast(table.columns.date_time, Date), func.avg(table.columns.total)).group_by(
        table.columns.date_time.cast(Date))
    rev = connection.execute(stmt).fetchall()
    for item in rev:
        date = item[0].strftime('%Y/%m/%d')
        revenue = float(item[1])
        average_check[date] = revenue
    connection.close()
    return average_check


def get_tips():
    tips = {}
    connection, table = get_connection()
    servers = get_servers(connection, table)
    for server in servers:
        #print(str(server))
        stmt = select([
            func.sum(table.columns.tips)]
        ).where(table.columns.server == str(server)).where(and_(table.columns.date_time >= '2021-03-16 00:00:00', table.columns.date_time <= '2021-11-17 00:00:00'))
        results = connection.execute(stmt).fetchall()
        #print(int(results[0]))
        if results[0][0] is None:
            tips[str(server)] = 0
        else:
            tips[str(server)] = float(results[0][0])
    connection.close()
    return tips


def get_revenue_by_date():
    revenue_by_date = {}
    connection, table = get_connection()
    stmt = select(cast(table.columns.date_time, Date), func.sum(table.columns.total)).group_by(table.columns.date_time.cast(Date))
    rev = connection.execute(stmt).fetchall()
    for item in rev:
        date = item[0].strftime('%Y/%m/%d')
        revenue = float(item[1])
        revenue_by_date[date] = revenue
    connection.close()
    return revenue_by_date


def get_guests_by_date():
    guests_by_date = {}
    connection, table = get_connection()
    stmt = select(cast(table.columns.date_time, Date), func.sum(table.columns.guests)).group_by(table.columns.date_time.cast(Date))
    rev = connection.execute(stmt).fetchall()
    for item in rev:
        date = item[0].strftime('%Y/%m/%d')
        guests = int(item[1])
        guests_by_date[date] = guests
    connection.close()
    return guests_by_date


def plot_get_revenue_by_hour_of_date():
    hours = []
    revenue = []
    plot_get_revenue_by_hour_of_date = {}
    connection, table = get_connection()
    stmt = select(func.date_format(table.columns.date_time, '%H'), func.sum(table.columns.total)).group_by(func.date_format(table.columns.date_time, '%H')).order_by(func.date_format(table.columns.date_time, '%H'))
    rev = connection.execute(stmt).fetchall()
    for item in rev:
        hours.append (item[0])
        revenue.append(float(item[1]))
        plot_get_revenue_by_hour_of_date['hours'] = hours
        plot_get_revenue_by_hour_of_date['revenue'] = revenue
    connection.close()
    return plot_get_revenue_by_hour_of_date


def plot_get_revenue_by_date():
    dates = []
    revenue = []
    plot_revenue_by_date = {}
    connection, table = get_connection()
    stmt = select(cast(table.columns.date_time, Date), func.sum(table.columns.total)).group_by(table.columns.date_time.cast(Date))
    rev = connection.execute(stmt).fetchall()
    for item in rev:
        dates.append (item[0].strftime('%Y/%m/%d'))
        revenue.append(float(item[1]))
        plot_revenue_by_date['dates'] = dates
        plot_revenue_by_date['revenue'] = revenue
    connection.close()
    return plot_revenue_by_date


def get_min_date():
    connection, table = get_connection()
    stmt = select([
        func.min(table.columns.date_time)]
    )
    results = connection.execute(stmt).fetchall()
    print(results[0][0])
    if results[0][0] is not None:
        return results[0][0]
    connection.close()
    return None


def get_max_date():
    connection, table = get_connection()
    stmt = select([
        func.max(table.columns.date_time)]
    )
    results = connection.execute(stmt).fetchall()
    print(results[0][0])
    if results[0][0] is not None:
        return results[0][0]
    connection.close()
    return None


def get_tips_by_date():
    tips = {}
    connection, table = get_connection()
    servers = get_servers(connection, table)
    print(get_min_date())
    print(get_max_date())

    for server in servers:
        print(str(server))
        stmt = select([
            func.sum(table.columns.tips)]
        ).where(table.columns.server == str(server)).where(and_(table.columns.date_time >= '2021-03-16 00:00:00', table.columns.date_time <= '2021-11-17 00:00:00'))
        results = connection.execute(stmt).fetchall()
        #print(int(results[0]))
        if results[0][0] is None:
            tips[str(server)] = 0
        else:
            tips[str(server)] = float(results[0][0])
    connection.close()
    return tips


def get_connection():
    engine = create_engine('mysql://srikar:srikar@localhost/instabase_cafeteria')
    connection = engine.connect()
    metadata = MetaData(bind=None)
    checks = Table(
        'checks',
        metadata,
        autoload=True,
        autoload_with=engine
    )
    return connection, checks


def get_servers(connection, checks):
    stmt = select([
            checks.columns.server]
        ).distinct()
    results = connection.execute(stmt).fetchall()
    servers = []
    for result in results:
        servers.append(result[0])
    return servers