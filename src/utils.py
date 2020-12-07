import pandas as pd

def missing_zero_values_table(df):
    """
    https://stackoverflow.com/questions/37366717/pandas-print-column-name-with-missing-values
    """
    zero_val = (df == 0.00).astype(int).sum(axis=0)
    mis_val = df.isnull().sum()
    mis_val_percent = 100 * df.isnull().sum() / len(df)
    mz_table = pd.concat([zero_val, mis_val, mis_val_percent], axis=1)
    mz_table = mz_table.rename(
    columns = {0 : 'Zero Count', 1 : 'Na Count', 2 : '% of Total'})
    mz_table['Zero + Na Count'] = mz_table['Zero Count'] + mz_table['Na Count']
    mz_table['% Zero + Na Count'] = 100 * mz_table['Zero + Na Count'] / len(df)
    mz_table['Data Type'] = df.dtypes
    mz_table = mz_table[
        mz_table.iloc[:,1] != 0].sort_values(
    '% of Total', ascending=False).round(1)
    return mz_table