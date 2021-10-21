from Web import create_app, DB


if __name__ == "__main__":
    DB.create_all(app=create_app())
    app = create_app()
    app.run(debug=True)
