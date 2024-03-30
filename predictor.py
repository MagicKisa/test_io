import joblib
import pandas as pd
from nltk.metrics import jaccard_distance

# Загрузка модели
kmeans = joblib.load('kmeans_model.joblib')

# Предположим, у вас есть DataFrame cluster_results с колонками 'cluster_labels' и 'target_labels'
cluster_results = pd.read_csv('cluster_results.csv')

tsne_df = pd.read_csv('tsne_df.csv')


def tokenize_text(text):
    return set(text.split())


def jaccard_similarity(text1, text2):
    # Рассчитываем меру схожести Жаккара
    set1 = tokenize_text(text1)
    set2 = tokenize_text(text2)
    similarity = 1 - jaccard_distance(set1, set2)
    return similarity


# Функция для предсказания кластера и возвращения распределения целевого признака
def predict_cluster_and_target_distribution(new_text):
    
    similarities = cluster_results['source_text'].apply(lambda x: jaccard_similarity(new_text, x))
    predicted_cluster = kmeans.predict([similarities])[0]

    # Получаем вероятности целевого признака из соответствующего кластера
    cluster_data = cluster_results[cluster_results['cluster_labels'] == predicted_cluster]

    # Считаем количество положительных и отрицательных целевых признаков внутри кластера
    positive_count = (cluster_data['target_labels'] == 1).sum()
    total_count = len(cluster_data)

    # Вычисляем вероятность положительного целевого признака внутри кластера
    probability_positive = positive_count / total_count

    return probability_positive
