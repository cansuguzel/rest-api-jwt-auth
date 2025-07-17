from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
# It initializes the Flask app and runs it in debug mode.
# The app is created using the create_app function defined in app/__init__.py.