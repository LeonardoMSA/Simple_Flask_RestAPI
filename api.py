from flask import Flask
from flask_restful import Resource, Api
from secure_check import authenticate, identity
from flask_jwt import JWT, jwt_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'walter'

api = Api(app)
jwt = JWT(app, authenticate, identity)

brands = []

class BrandNames(Resource):

    def get(self, name):

        for brand in brands:
            if brand['name'] == name:
                return brand

        return {'name':None}, 404

    def post(self, name):

        brand = {'name':name}

        brands.append(brand)

        return brand

    def delete(self, name):

        for index, brand in enumerate(brands):
            if brand['name'] == name:
                deleted_brand = brands.pop(index)

                return {'note':'delete_success'}


class AllBrands(Resource):

    @jwt_required
    def get(self):
        return {'brands':brands}

api.add_resource(BrandNames, '/brand/<string:name>')
api.add_resource(AllBrands, '/brands')


if __name__ == '__main__':
    app.run(debug=True)