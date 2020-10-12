from flaskblog import app #so it will import that "__init__.py" file here. (the "app" variable)

# allows us to run the script using "python3 flaskblog.py" command, but we can use also "flask run"
if __name__ == '__main__': 
    app.run(debug=True)

