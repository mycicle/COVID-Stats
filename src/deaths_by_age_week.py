import pandas as pd
import numpy as np

from io import StringIO
from sklearn.preprocessing import LabelEncoder
from loguru import logger
from typing import Dict, List, Tuple, Any

from utils.enums import DatasetName
from utils.variables import path_dict, age_key

def to_categorical(input: pd.Series) -> List[Any]:
    """
    returns the mapping of int to categorical value, and the categorized pandas series
    """
    le = LabelEncoder()
    output: np.ndarray =  le.fit_transform(input)
    le_name_mapping: Tuple[int, str] = tuple(zip(le.transform(le.classes_), le.classes_))
    
    return [le_name_mapping, pd.Series(output)]

def main():
    datapath: str = path_dict[DatasetName.sex_age_week]
    
    logger.info(f"Reading data from {datapath}")
    raw: pd.DataFrame = pd.read_csv(datapath)
    
    buf: StringIO = StringIO()
    raw.info(verbose=True, buf=buf)
    logger.info(f"Dataset Length: {len(raw)}")
    logger.info(f"Dataset Summary: {buf.getvalue()}")

    logger.info(f"Categorizing column: {age_key}")
    [age_categorical_mapping, raw[age_key]] = to_categorical(raw[age_key])

    logger.info(f"Categorical Mappings for column: {age_key}\n{age_categorical_mapping}")


if __name__ == "__main__":
    main()
