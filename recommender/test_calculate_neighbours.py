import unittest
import pandas as pd

from recommender.calculate_neighbours import recommend_projects_from_ideal_client_project


class TestCalculateNeighbours(unittest.TestCase):

    def test_recommend_projects_from_ideal_client_project(self):
        new_scores = pd.DataFrame({
            'id': '-1',
            'socialOverEnv': 'true',
            'economyOverHealthcare': 'true',
            'povertyOverEducation': 'true',
            'targetedOverDiverse': 'true',
            'managementFees': 'UNDER5',
            'esgOverAll': 'true',
            'shortOverLongTerm': 'true',
            'region': None
        }, index=[0])
        result = recommend_projects_from_ideal_client_project(new_scores, '-1')
        self.assertEqual('1', result.array[0])
