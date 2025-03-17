from flask import Blueprint
from flask_restx import Namespace

api_bp = Blueprint('api', __name__)
api = Namespace('api', description="Wine Inventory Management API")