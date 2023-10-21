import numpy as np
from box import ConfigBox
from pathlib import Path
from gymtracker import logger
from box.exceptions import BoxValueError
import yaml



def calculate_angle(a,b,c):
    a= np.array(a) # First
    b= np.array(b) # Mid
    c= np.array(c) # End
    
    
    vect_ab = a-b
    vect_bc = c-b
    
    radians= np.arccos(np.dot(vect_ab,vect_bc)/(np.linalg.norm(vect_ab)*np.linalg.norm(vect_bc)))
    
    """
        Turned the points into vector and  with the equation ab.bc = |ab||bc|cosα
        
        α = cos^-1 (ab.bc/(|ab||bc|))
        
        The result will be in radian we convert that into degree
    
    """
    
    angles= np.abs(radians*180.0/np.pi)
    
    return angles





def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns
    
    Args:
        path_to_yaml (str): path like input
    
    Raises:
        ValueError: if yamlfile is empty
        e: empty file
        
    Returns:
        ConfigBox: ConfigBox type
    """

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            # logger.info(f"yaml file: {path_to_yaml} loaded succesfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
