from os.path import join
from typing import Dict

from .utils import get_file_path_relative
from .enums import DatasetName

data_folder: str = 'data'

path_dict: Dict[DatasetName, str] = {
    DatasetName.sex_age_week : join(get_file_path_relative(data_folder), "Provisional_COVID-19_Death_Counts_by_Sex__Age__and_Week.csv"),
    DatasetName.focus_ages_0_18 : join(get_file_path_relative(data_folder), "Provisional_COVID-19_Deaths_Focus_on_Ages_0-18_Years.csv"),
    DatasetName.sex_age_state : join(get_file_path_relative(data_folder), "Provisional_COVID-19_Death_Counts_by_Sex__Age__and_State.csv"),
    DatasetName.dc_inf_pneu : join(get_file_path_relative(data_folder), "Provisional_Death_Counts_for_Influenza__Pneumonia__and_COVID-19.csv"),
    DatasetName.conditions : join(get_file_path_relative(data_folder), "Conditions_contributing_to_deaths_involving_coronavirus_disease_2019__COVID-19__by_age_group_and_state__United_States.csv"),
    DatasetName.weekly_deaths_14_18 : join(get_file_path_relative(data_folder), "Weekly_Counts_of_Deaths_by_State_and_Select_Causes__2014-2018.csv"),
    DatasetName.weekly_deaths_19_20 : join(get_file_path_relative(data_folder), "Weekly_Counts_of_Deaths_by_State_and_Select_Causes__2019-2020.csv"),
}

# Keys for Provisional_COVID-19_Death_Counts_by_Sex__Age__and_Week.csv
week_key: str = "MMWR Week"
sex_key: str = "Sex"
age_key: str = "Age Group"
total_deaths_key: str = "Total Deaths"
covid_deaths_key: str = "COVID-19 Deaths"
state_key: str = "State"
data_as_of_key: str = "Data as of"
end_week_key: str = "End Week"
start_week_key: str = "Start Week"

