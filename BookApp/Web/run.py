from web import create_app, DB


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        DB.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
