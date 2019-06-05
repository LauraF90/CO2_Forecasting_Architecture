# CO2_Forecasting_Architecture

# Dependencies
pip install entsoe-py

pip install python-forecastio

pip install -U scikit-learn

# database migration
python manage.py makemigrations
python manage.py migrate

# Running
 python manage.py runserver
 
# Remarks
 The model.pkl is the regression model that is used for forecasting -> It can be replaced later in future work with another
 model with the same name.
 
 The forecasts table in database will be emptied everyday at 12 am.
# Web-based API
after runnning the architecture , the forecasts can be seen using the browser using URL:
http://127.0.0.1:8000/forecasts/
 
