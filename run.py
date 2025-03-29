import os
from dotenv import load_dotenv
load_dotenv()


from app.routes import register_routes
from app import create_app

app = create_app()
register_routes(app=app)

if __name__ == '__main__':
    # app.run()
    PORT = os.getenv("PORT",4000)
    from waitress import serve
    serve(app, host="0.0.0.0", port=PORT)