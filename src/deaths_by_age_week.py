#!/usr/bin/env python3
"""
Main file for processing data by age and week
"""


import pandas as pd
import numpy as np

from io import StringIO
from sklearn.preprocessing import LabelEncoder
from loguru import logger
from typing import Dict, List, Tuple, Any, Union

from utils.enums import DatasetName, AgeGroup, Sexes
from utils.variables import path_dict, age_key, sex_key, week_key

def to_categorical(input: pd.Series) -> List[Any]:
    """
    returns the mapping of int to categorical value, and the categorized pandas series
    """

    le = LabelEncoder()
    output: np.ndarray =  le.fit_transform(input)
    le_name_mapping: Tuple[int, str] = tuple(zip(le.transform(le.classes_), le.classes_))
    
    return [le_name_mapping, pd.Series(output)]

def get_rows(data: pd.DataFrame, column_key: str, column_values: List[Any], includes: bool = True):
    """
    input a dataframe, a column key, a list of column values, and a bool for includes (true by default,
    true to return values that match the column_values and false to return values that exclude column_values)

    returns a data frame
    """

    if includes:
        return data[data[column_key].isin(column_values)]
    else:
        return data[~data[column_key].isin(column_values)]


@logger.catch
def main():
    datapath: str = path_dict[DatasetName.sex_age_week]
    
    logger.info(f"Reading data from {datapath}")
    raw: pd.DataFrame = pd.read_csv(datapath)
    
    buf: StringIO = StringIO()
    raw.info(verbose=True, buf=buf)
    logger.info(f"Dataset Length: {len(raw)}")
    logger.info(f"Dataset Summary: {buf.getvalue()}")

    # logger.info("Generating Dataset for Ages 0-24")
    # lets get the death rate over time for ages 0-24
    # ages_0_24: pd.DataFrame = raw[((raw[age_key] == AgeGroup.under_one_year.value) | 
    #                                 (raw[age_key] == AgeGroup.age_1_4.value) |
    #                                 (raw[age_key] == AgeGroup.age_5_14.value) | 
    #                                 (raw[age_key] == AgeGroup.age_15_24.value))
    #                                 &
    #                                 (raw[sex_key] == Sexes.both_sexes.value)
    #                             ]
    # buf: StringIO = StringIO()
    # ages_0_24.info(verbose=True, buf=buf)
    # logger.info(f"Dataset Summary: {buf.getvalue()}")

    # min_week: int = raw[week_key].min()
    # max_week: int = raw[week_key].max()



if __name__ == "__main__":
    main()
