"""
> author: JBocage

This script shows how to transform a column into categorical data.

The snippet useful is

@snip:useful_part
"""

# @begin:useful_part
COLUMN_TO_CATEGORIZE = 'metro'

import pandas as pd
df = pd.read_csv('./data/moscow_real_estate_sale.csv')
df = pd.concat((df.drop(COLUMN_TO_CATEGORIZE, axis=True), pd.get_dummies(df[COLUMN_TO_CATEGORIZE])), axis=1)
# @end:useful_part