import pandas as pd

from app.etl import transform

def test_calculate_stock_total_price():
    # prep
    df = pd.DataFrame({
        'quantity': [10, 5],
        'price': [20.0, 100.0],
        'category': ['toys', 'eletronics']
    })
    expected = pd.Series([200.0, 500.0], name='stock_total_price')

    # action
    result = transform(df)

    # verification
    pd.testing.assert_series_equal(result['stock_total_price'], expected)

def test_normalized_category():
    # prep
    df = pd.DataFrame({
        'quantity': [1, 2],
        'price': [10.0, 20.0],
        'category': ['toys', 'eletronics']
    })
    expected = pd.Series(['TOYS', 'ELETRONICS'], name='normalized_category')

    # action
    result = transform(df)

    # varification
    pd.testing.assert_series_equal(result['normalized_category'], expected)

def test_availability():
    # prep
    df = pd.DataFrame({
        'quantity': [0, 2],
        'price': [10.0, 20.0],
        'category': ['toys', 'eletronics']
    })
    expected = pd.Series([False, True], name='availability')

    # action
    result = transform(df)

    # verification
    pd.testing.assert_series_equal(result['availability'], expected)

# `pytest filename.py` 