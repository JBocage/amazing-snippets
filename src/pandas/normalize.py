"""
> author: JBocage

This script shows how to normalize pandas dataframes.

For gaussian normalisation

@snip:norm

For min-max normalisation

@snip:minmax
"""

# @begin:useful_part
import pandas as pd
df = pd.read_csv('./data/rice_beef_coffee_price_changes.csv')
df = df.drop('Month', axis=1)

# @begin:norm
gaussian_normalized_df=(df-df.mean())/df.std()
# @end:norm

# @begin:minmax
minmax_normalized_df=(df-df.min())/(df.max()-df.min())
# @end:minmax
# @end:useful_part