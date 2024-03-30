import pytest
from predictor import tokenize_text, jaccard_similarity, predict_cluster_and_target_distribution


@pytest.mark.parametrize("text, length",
                         [
                             ('I love Python', 3),
                             ('', 0),
                             ('I love Love', 3),
                             ('I love love', 2)
                         ]
                         )
def test_len_set(text, length):
    tokenized_text = tokenize_text(text)
    assert len(tokenized_text) == length


def test_bad_type():
    with pytest.raises(AttributeError):
        tokenize_text(15)


def test_jaccard_similarity():
    text1 = 'I love Python'
    text2 = 'I love Python'
    similarity = jaccard_similarity(text1, text2)
    assert similarity == 1

    text1 = 'I love'
    text2 = 'I love Python'
    similarity = jaccard_similarity(text1, text2)
    assert similarity != 1

    text1 = 'I love Python'
    text2 = 'I Love Python'
    similarity = jaccard_similarity(text1, text2)
    assert similarity != 1

    with pytest.raises(AttributeError):
        text1 = 15
        text2 = 'I love Python'
        jaccard_similarity(text1, text2)

    with pytest.raises(AttributeError):
        text1 = 15
        text2 = 20
        jaccard_similarity(text1, text2)


def test_predict_cluster_and_target_distribution():
    with pytest.raises(AttributeError):
        text = 15
        predict_cluster_and_target_distribution(text)

    text = 'I love Python'
    probability = predict_cluster_and_target_distribution(text)
    assert 0 <= probability <= 1

