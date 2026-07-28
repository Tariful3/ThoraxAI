import os
import json
import joblib
import yaml
import base64

from pathlib import Path
from typing import Any

from box.exceptions import BoxValueError
from box import ConfigBox
from ensure import ensure_annotations

from chestDiseaseClassifier import logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads yaml file and returns ConfigBox object
    """

    try:
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)

            logger.info(f"YAML file loaded successfully: {path_to_yaml}")

            return ConfigBox(content)

    except BoxValueError:
        raise ValueError("YAML file is empty")

    except Exception as e:
        raise e



@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Create list of directories
    """

    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)

        if verbose:
            logger.info(f"Created directory: {path}")



@ensure_annotations
def save_json(path: Path, data: dict):
    """
    Save json data into file
    """

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"JSON file saved at: {path}")



@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Load json file
    """

    with open(path, "r") as f:
        content = json.load(f)

    logger.info(f"JSON file loaded from: {path}")

    return ConfigBox(content)



@ensure_annotations
def save_bin(data: Any, path: Path):
    """
    Save binary file using joblib
    """

    joblib.dump(data, path)

    logger.info(f"Binary file saved at: {path}")



@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Load binary file using joblib
    """

    data = joblib.load(path)

    logger.info(f"Binary file loaded from: {path}")

    return data



@ensure_annotations
def get_size(path: Path) -> str:
    """
    Get file size in KB/MB/GB
    """

    size = os.path.getsize(path)

    if size < 1024:
        return f"{size} Bytes"

    elif size < 1024**2:
        return f"{round(size/1024,2)} KB"

    elif size < 1024**3:
        return f"{round(size/(1024**2),2)} MB"

    else:
        return f"{round(size/(1024**3),2)} GB"



@ensure_annotations
def encode_image(image_path: Path) -> str:
    """
    Convert image into base64 string
    """

    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(
            image_file.read()
        )

    return encoded_string.decode("utf-8")



@ensure_annotations
def decode_image(encoded_string: str, file_name: Path):
    """
    Decode base64 string and save image
    """

    image_data = base64.b64decode(encoded_string)

    with open(file_name, "wb") as f:
        f.write(image_data)

    logger.info(f"Image decoded and saved: {file_name}")