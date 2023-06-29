from __init__ import create_app, DB


if __name__ == "__main__":
    DB.create_all(app=create_app())
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
