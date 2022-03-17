# pandas

This directory contains code snippets for quick pandas data treatment.
<hr style="border:2px solid gray"> </hr>

## Structure 
```
pandas/
├── data/
│   ├── moscow_real_estate_sale.csv
│   └── rice_beef_coffee_price_changes.csv
├── make_categories.py
└── normalize.py
```

<hr style="border:2px solid gray"> </hr>

## data
>
>Contains sample databases used in the pandas dir scripts.
---
## make_categories.py
>> author: JBocage
>
>This script shows how to transform a column into categorical data.
>
>The snippet useful is
>
>```python
>COLUMN_TO_CATEGORIZE = 'metro'
>
>import pandas as pd
>df = pd.read_csv('./data/moscow_real_estate_sale.csv')
>df = pd.concat((df.drop(COLUMN_TO_CATEGORIZE, axis=True), pd.get_dummies(df[COLUMN_TO_CATEGORIZE])), axis=1)
>```

---
## normalize.py
>> author: JBocage
>
>This script shows how to normalize pandas dataframes.
>
>For gaussian normalisation
>
>```python
>gaussian_normalized_df=(df-df.mean())/df.std()
>```
>
>For min-max normalisation
>
>```python
>minmax_normalized_df=(df-df.min())/(df.max()-df.min())
>```

---




<sub>This doc was automatically generated with makedoc v1.1.6 on  03/17/22 18:17:24 