import pytest

from ancpbids import model_latest
from ancpbids.schema.expr import evaluate


@pytest.mark.parametrize(
    'expression, expected',
    [(case['expression'], case['result'])
     for case in model_latest.document['meta']['expression_tests']],
)
def test_schema_expression_tests(expression, expected):
    assert evaluate(expression) == expected
