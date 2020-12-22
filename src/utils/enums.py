from enum import Enum

class DatasetName(Enum):
    sex_age_state = "sex_age_state"
    sex_age_week = "sex_age_week"
    focus_ages_0_18 = "focus_ages_0_18"
    dc_inf_pneu = "dc_inf_pneu"
    conditions = "conditions"
    weekly_deaths_14_18 = "weekly_deaths_14_18"
    weekly_deaths_19_20 = "weekly_deaths_19_20"

class AgeGroup(Enum):
    all_ages = "All Ages"
    under_one_year =  "Under 1 year"
    age_1_4        =  "1-4 years"
    age_5_14       =  "5- 14 years"
    age_15_24      =  "15- 24 years"
    age_25_34      =  "25- 34 years"
    age_35_44      =  "35- 44 years"
    age_45_54      =  "45- 54 years"
    age_55_64      =  "55- 64 years"
    age_65_74      =  "65- 74 years"
    age_75_84      =  "75- 84 years"
    age_85_over    =  "85 years and over"

class Sexes(Enum):
    male       = "Male"
    female     = "Female"
    both_sexes = "All Sex"