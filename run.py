from flaskblog import create_app 

app = create_app() # remember that we can pass an argument there as configuration, but it using the config class already as it's default

# allows us to run the script using "python3 flaskblog.py" command, but we can use also "flask run"
if __name__ == '__main__': 
    app.run(debug=True)



