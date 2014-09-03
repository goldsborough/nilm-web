from flask import render_template
from app import app

import postgres
import os
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

@app.route('/')
def index():
    

    with postgres.Database(url) as db:
        
        # raw data
        data = db.get("data","total, a, b")

        # summary form for the dashboard, returns the
        # maximum, minimum and average for all rows
        summary = postgres.summary(data)

        # For the charts we need the raw data again (string format)
        data = " ".join([str(col) for row in data for col in row])
    
    return render_template('index.html',
                           ovw_max_val=summary[0][0][0],
                           ovw_max_time=summary[0][0][1],
                           ovw_min_val=summary[0][1][0],
                           ovw_min_time=summary[0][1][1],
                           ovw_avg_val=summary[0][2],
                           appA_max_val=summary[1][0][0],
                           appA_max_time=summary[1][0][1],
                           appA_min_val=summary[1][1][0],
                           appA_min_time=summary[1][1][1],
                           appA_avg_val=summary[1][2],
                           appB_max_val=summary[2][0][0],
                           appB_max_time=summary[2][0][1],
                           appB_min_val=summary[2][1][0],
                           appB_min_time=summary[2][1][1],
                           appB_avg_val=summary[2][2],
                           samples = data)
    
@app.errorhandler(404)
def Error404(error):
    return render_template('error.html'), 404
