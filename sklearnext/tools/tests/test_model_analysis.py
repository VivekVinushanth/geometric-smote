"""
Test the model_analysis module.
"""

import pytest
from numpy.testing import assert_array_equal
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.datasets import make_classification

from ...tools import report_model_search_results
from ...model_selection import ModelSearchCV

X_clf, y_clf = make_classification()
CLASSIFIERS = [
    ('knn', KNeighborsClassifier()),
    ('dtc', DecisionTreeClassifier()),
    ('pip', Pipeline([('scaler', MinMaxScaler()), ('knn', KNeighborsClassifier())]))
]
CLASSIFIERS_PARAM_GRIDS = {'dtc__max_depth': [2, 5], 'pip__knn__n_neighbors': [3, 5]}
BASIC_COLUMNS = ['models', 'params', 'mean_fit_time']


@pytest.mark.parametrize('scoring,sort_results', [
    (None, None),
    (None, 'mean_fit_time'),
    (None, 'mean_test_score'),
    ('accuracy', None),
    ('recall', 'mean_fit_time'),
    ('recall', 'mean_test_score'),
    (['accuracy', 'recall'], None),
    (['accuracy', 'recall'], 'mean_fit_time'),
    (['accuracy', 'recall'], 'mean_test_accuracy'),
    (['accuracy', 'recall'], 'mean_test_recall')
])
def test_report_model_search_results(scoring, sort_results):
    """Test the output of the model search report function."""
    mscv = ModelSearchCV(CLASSIFIERS, CLASSIFIERS_PARAM_GRIDS, scoring=scoring, refit=False, verbose=False)
    mscv.fit(X_clf, y_clf)
    report = report_model_search_results(mscv, sort_results)
    assert len(report.columns) == (len(mscv.scorer_) if isinstance(mscv.scoring, list) else 1) + len(BASIC_COLUMNS)
    if sort_results is not None:
        assert_array_equal(report[sort_results], report[sort_results].sort_values(ascending=(sort_results == 'mean_fit_time')))