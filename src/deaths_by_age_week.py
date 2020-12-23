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
from matplotlib.patches import Patch
from loguru import logger
from typing import Dict, List, Tuple, Any, Union, Optional

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

def get_cdf(data: List[int]) -> pd.Series:
    return np.cumsum(data)

def plot_col_v_col(data: pd.DataFrame, x_key: str, y_key: str, title: str, to_disk: bool = True) -> None:
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

def plot_barplot(data: pd.DataFrame, x_key: str, rot: int, title: str, round_val: Optional[int] = None) -> None:
    fig, ax = plt.subplots()
    ax = data[x_key].plot.bar(rot=-15, fontsize=6, title=title)

    for p in ax.patches:
        label = round(p.get_height(), round_val)
        ax.annotate(str(label), (p.get_x() * 1.01, p.get_height() * 1.01))
   
    ax.set_ylabel(x_key)
    plt.xticks(range(0, len(data.index)), data.index)
    plt.savefig(join(get_file_path_relative(visualizations_folder), f"{title}.png"))

def plot_line(data: np.ndarray, xticks: List[str], ylabel: str, title: str, secondary_data: Optional[pd.Series] = None, secondary_title: Optional[str] = None, round_val: Optional[int] = None) -> None:
    fig, ax = plt.subplots()
    
    legend_handles = [Patch(facecolor='orange', edgecolor='r',
                        label=title)]

    if secondary_data is not None:
        ax.bar(xticks, secondary_data)
        legend_handles.append(Patch(facecolor='blue', edgecolor='black',
                         label=secondary_title))

    for x, y in zip(xticks, data):
        label = "{:.2f}".format(y)
        plt.annotate(label, # this is the text
                    (x,y), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0,10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    ax.scatter(xticks, data, c="orange")
    plt.legend(handles=legend_handles)
    plt.ylabel(ylabel)
    plt.xticks(range(0, len(xticks)), xticks, rotation=-15, fontsize=6)
    plt.title(title)
    plt.savefig(join(get_file_path_relative(visualizations_folder), f"{title}.png"))

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
    totals: List[int] = []
    index: List[str] = []
    for age_group in AgeGroup:
        data_by_age[age_group] = get_rows(both_sexes, age_key, age_group.value)
        if age_group != AgeGroup.all_ages:
            totals.append(data_by_age[age_group][covid_deaths_key].sum())
            index.append(age_group.value)

    totals_by_age: pd.DataFrame = pd.DataFrame({"totals": totals, "percentage": [num/sum(totals) for num in totals]}, index=index)
    print(totals_by_age)
    for key, frame in data_by_age.items():
        plot_col_v_col(frame, week_key, covid_deaths_key, title=key.value, to_disk=True)
    
    cdf_totals_by_age = get_cdf(totals_by_age.percentage.values)

    plot_barplot(totals_by_age, "totals", -15, "total_deaths_by_age")
    plot_barplot(totals_by_age, "percentage", -15, "percentage_deaths_by_age", 3) 
    plot_line(cdf_totals_by_age, totals_by_age.index.values, "percentage", "CDF Deaths By Age", totals_by_age.percentage.values, "percentages")

if __name__ == "__main__":
    main()
