from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

def forecast_fn(x, y, degree=1, n_future=15):
    df = pd.DataFrame({'Time': x, 'Value': y})
    print(df)
    X = df[['Time']].values.reshape(-1, 1)
    Y = df['Value'].values

    # Transform features
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, Y)

    resultlist = []
    for ii in range(1, n_future + 1):
        future_time = X[-1, 0] + ii
        print(future_time,"future_time")
        ft_poly = poly.transform(np.array([[future_time]]))
        pred = model.predict(ft_poly)
        resultlist.append(round(float(abs(pred[0])),2))
    return resultlist


from datetime import datetime, timedelta


def get_dates_between(start_date_str, end_date_str, date_format='%Y-%m-%d'):
    """
    Generates a list of all dates (as strings) between two input date strings, inclusive.

    Args:
        start_date_str: The start date string.
        end_date_str: The end date string.
        date_format: The format of the input/output date strings (default 'YYYY-MM-DD').

    Returns:
        A list of date strings.
    """
    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date_str, date_format).date()
    end_date = datetime.strptime(end_date_str, date_format).date()

    # Calculate the number of days between the dates
    delta = end_date - start_date

    # Generate all dates in the range
    dates_list = []
    for i in range(delta.days + 1):  # +1 to include the end date
        current_date = start_date + timedelta(days=i)
        dates_list.append(current_date.strftime(date_format))  # Convert back to string format

    return dates_list



# Output: ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']
