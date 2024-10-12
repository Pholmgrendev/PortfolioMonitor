import os
import yaml

def load_env_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)
    
    # load the API configuration
    for key, value in config['api'].items():
        env_var = f"API_{key.upper().replace('-', '_')}"
        os.environ[env_var] = str(value)
