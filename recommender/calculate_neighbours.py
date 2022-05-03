import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from db import db_queries as projects


def projects_scores_df():
    all_projects = projects.all_project_scores()
    df = pd.DataFrame.from_dict(all_projects)
    return df


def test_project_scores():
    score1 = pd.DataFrame({
        'id': '1',
        'socialOverEnv': 'false',
        'economyOverHealthcare': 'true',
        'povertyOverEducation': 'true',
        'targetedOverDiverse': 'true',
        'managementFees': 'UNDER5',
        'esgOverAll': 'true',
        'shortOverLongTerm': 'true',
        'region': None
    }, index=[0])
    score2 = pd.DataFrame({
        'id': '2',
        'socialOverEnv': 'false',
        'economyOverHealthcare': 'false',
        'povertyOverEducation': 'false',
        'targetedOverDiverse': 'false',
        'managementFees': 'OVER5',
        'esgOverAll': 'false',
        'shortOverLongTerm': 'false',
        'region': None
    }, index=[0])
    score3 = pd.DataFrame({
        'id': '3',
        'socialOverEnv': 'false',
        'economyOverHealthcare': 'false',
        'povertyOverEducation': 'false',
        'targetedOverDiverse': 'false',
        'managementFees': 'NONE',
        'esgOverAll': 'false',
        'shortOverLongTerm': 'false',
        'region': None
    }, index=[0])
    df = pd.concat([score1, score2], ignore_index=True, axis=0)
    df = pd.concat([df, score3], ignore_index=True, axis=0)
    return df


def recommend_projects_from_ideal_client_project(ideal_project, filter_id):
    project_df = projects_scores_df()
    # project_df = test_project_scores()
    project_df = pd.concat([project_df, ideal_project], ignore_index=True, axis=0)
    id_col = project_df.pop('id')
    project_df.insert(0, 'id', id_col)
    project_df['metadata'] = project_df.apply(
        lambda x: ' ' + str(x['socialOverEnv']) + ' ' + str(x['economyOverHealthcare'])
                  + ' ' + str(x['povertyOverEducation']) + ' ' + str(
            x['targetedOverDiverse']) + ' ' + str(x['managementFees']) +
                  ' ' + str(x['esgOverAll']) + ' ' + str(
            x['shortOverLongTerm']) + ' ' + ' '.join(str(x['region'])),
        axis=1)

    # method for following lines came from:
    # https://medium.com/analytics-vidhya/metadata-based-recommender-systems-in-python-c6aae213b25c
    count_vec = CountVectorizer(stop_words='english')
    count_vec_matrix = count_vec.fit_transform(project_df['metadata'])
    cosine_sim_matrix = cosine_similarity(count_vec_matrix, count_vec_matrix)

    mapping = pd.Series(project_df.index, index=project_df['id'])
    project_index = mapping[filter_id]

    similarity_score = list(enumerate(cosine_sim_matrix[project_index]))
    sim_score_sorted = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    similarity_top_2 = sim_score_sorted[1:2]
    project_indices = [i[0] for i in similarity_top_2]
    return project_df['id'].iloc[project_indices]
