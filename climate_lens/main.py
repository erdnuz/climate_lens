"""Application entrypoint for local execution."""

from dashboard import app


if __name__ == "__main__":
    app.run(debug=True)
