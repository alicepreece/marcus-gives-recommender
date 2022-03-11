from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
from recommender import calculate_neighbours as calculate

app = Flask(__name__)
api = Api(app)


class Recommendation(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('socialOverEnv')
        parser.add_argument('economyOverHealthcare')
        parser.add_argument('povertyOverEducation')
        parser.add_argument('targetedOverDiverse')
        parser.add_argument('managementFees')
        parser.add_argument('esgOverAll')
        parser.add_argument('shortOverLongTerm')
        parser.add_argument('region')

        args = parser.parse_args()

        new_data = pd.DataFrame({
            'id': args['id'],
            'socialOverEnv': args['socialOverEnv'],
            'economyOverHealthcare': args['economyOverHealthcare'],
            'povertyOverEducation': args['povertyOverEducation'],
            'targetedOverDiverse': args['targetedOverDiverse'],
            'managementFees': args['managementFees'],
            'esgOverAll': args['esgOverAll'],
            'shortOverLongTerm': args['shortOverLongTerm'],
            'region': args['region']
        }, index=[0])
        recommendation = calculate.recommend_projects_from_ideal_client_project(new_data, args['id'])
        return {"R": str(recommendation.array[0])}


api.add_resource(Recommendation, '/calculateRecommendation')


if __name__ == '__main__':
    app.run(port=8010)


