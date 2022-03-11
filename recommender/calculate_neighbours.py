import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from db import db_queries as projects


def projects_scores_df():
    all_projects = projects.all_project_scores()
    df = pd.DataFrame.from_dict(all_projects)
    return df


# Reference here if needed
def recommend_projects_from_ideal_client_project(ideal_project, filter_id):
    project_df = projects_scores_df()
    project_df.pop('_id')
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
