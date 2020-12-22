import os

from os.path import join
from enum import Enum
from typing import Dict 

from utils.utils import get_file_path_relative

class DatasetName(Enum):
    sex_age_state = "sex_age_state"
    sex_age_week = "sex_age_week"
    focus_ages_0_18 = "focus_ages_0_18"
    dc_inf_pneu = "dc_inf_pneu"

data_folder: str = 'data'

path_dict: Dict[DatasetName, str] = {
    DatasetName.sex_age_week : join(get_file_path_relative(data_folder), "Provisional_COVID-19_Death_Counts_by_Sex__Age__and_Week.csv"),
    DatasetName.focus_ages_0_18 : join(get_file_path_relative(data_folder), "Provisional_COVID-19_Deaths_Focus_on_Ages_0-18_Years.csv")
}

def main():
    print("Below is the current working directory:")
    print(os.getcwd())

    print("Below is where the data is:")
    print(join(get_file_path_relative(data_folder), "Provisional_COVID-19_Death_Counts_by_Sex__Age__and_Week.csv"))

    print("This is the call we have to make after all of this heavy lifting")
    print(path_dict[DatasetName.sex_age_week])

    print("This is an enum value")
    print(DatasetName.sex_age_week.value)

if __name__ == "__main__":
    main()