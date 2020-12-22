#!/usr/bin/env python3
"""
Main file for processing data by age and week
"""


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from io import StringIO
from os.path import join
from sklearn.preprocessing import LabelEncoder
from loguru import logger
from typing import Dict, List, Tuple, Any, Union

from utils.enums import DatasetName, AgeGroup, Sexes
from utils.utils import get_file_path_relative
from utils.variables import path_dict, visualizations_folder, age_key, sex_key, week_key, covid_deaths_key

def to_categorical(input: pd.Series) -> List[Any]:
    """
    returns the mapping of int to categorical value, and the categorized pandas series
    """
    le = LabelEncoder()
    output: np.ndarray =  le.fit_transform(input)
    le_name_mapping: Tuple[int, str] = tuple(zip(le.transform(le.classes_), le.classes_))
    
    return [le_name_mapping, pd.Series(output)]

def get_rows(data: pd.DataFrame, column_key: str, column_values: List[Any], includes: bool = True) -> pd.DataFrame:
    """
    input a dataframe, a column key, a list of column values, and a bool for includes (true by default,
    true to return values that match the column_values and false to return values that exclude column_values)

    returns a data frame
    """
    if (not isinstance(column_values, list)):
        column_values = [column_values]

    if includes:
        return data[data[column_key].isin(column_values)]
    else:
        return data[~data[column_key].isin(column_values)]

def plot_col_v_col(data: pd.DataFrame, x_key: str, y_key: str, title: str, to_disk=True) -> None:
    """
    Plot a graph with title = title,
    x = data[x_key]
    y = data[y_key]
    x label = x_key
    y label = y_key
    path = join(get_file_path_relative(visualizations_folder), "title.png")
    """
    fig, ax = plt.subplots()
    ax.set_xlabel(x_key)
    ax.set_ylabel(y_key)
    ax.plot(data[x_key], data[y_key])
    ax.scatter(data[x_key], data[y_key], c="orange")
    ax.text(-0.1, 1.07, f'Cumulative: {data[y_key].sum()}', style='italic',
        bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10},
        transform=ax.transAxes)
    ax.set_title(title)
    
    if to_disk:
        plt.savefig(join(get_file_path_relative(visualizations_folder), f"{title}.png"))
    else:
        plt.show()

@logger.catch
def main():
    datapath: str = path_dict[DatasetName.sex_age_week]
    
    logger.info(f"Reading data from {datapath}")
    raw: pd.DataFrame = pd.read_csv(datapath)
    
    buf: StringIO = StringIO()
    raw.info(verbose=True, buf=buf)
    logger.info(f"Dataset Length: {len(raw)}")
    logger.info(f"Dataset Summary: {buf.getvalue()}")

    both_sexes: pd.DataFrame = get_rows(raw, sex_key, Sexes.both_sexes.value, includes=True)
    
    data_by_age: Dict[AgeGroup, pd.DataFrame] = {}

    for age_group in AgeGroup:
        data_by_age[age_group] = get_rows(both_sexes, age_key, age_group.value)

    for key, frame in data_by_age.items():
        plot_col_v_col(frame, week_key, covid_deaths_key, title=key.value, to_disk=True)
    



if __name__ == "__main__":
    main()
