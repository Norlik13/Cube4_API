from flask import Flask
from config import Config
from flask_restx import Api
from routes import *
from routes.Color_route import api as color_api
from routes.Cepage_route import api as cepage_api
from routes.Appellation_route import api as appellation_api
from routes.Provider_route import api as provider_api
from routes.Customer_route import api as customer_api
from routes.Orders_route import api as orders_api
from routes.Wine_route import api as wine_api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    api = Api(
        app,
        version='1.0',
        title='Wine Inventory API',
        description='API for managing wines, customers, orders, and providers.',
        doc='/swagger'  # Swagger UI available at /swagger
    )
    
    api.add_namespace(color_api, path='/colors')
    api.add_namespace(cepage_api, path='/cepages')
    api.add_namespace(appellation_api, path='/appellations')
    api.add_namespace(provider_api, path='/providers')
    api.add_namespace(customer_api, path='/customers')
    api.add_namespace(orders_api, path='/orders')
    api.add_namespace(wine_api, path='/wines')  # Add Wine namespace

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
