from flaskblog import app # so it will import that "__init__.py" file here. (the "app" variable)
# the python knows that the "__init__.py" file is that package initializer file, so it grabs the "app" instance from there automatically, so we can use "app" instance (Flask) here in "run.py" 

# allows us to run the script using "python3 flaskblog.py" command, but we can use also "flask run"
if __name__ == '__main__': 
    app.run(debug=True)


# so the only job of this file is to grab the "app" (instance of flaskblog) and run it

