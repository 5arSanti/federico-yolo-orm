import os, yaml
from typing import List

def create_data_yaml(path_to_classes_txt, path_to_data_yaml):
  if not os.path.exists(path_to_classes_txt):
    print(f'classes.txt file not found! Please create a classes.txt labelmap and move it to {path_to_classes_txt}')
    return
  
  with open(path_to_classes_txt, 'r') as f:
    classes = []
    for line in f.readlines():
      if len(line.strip()) == 0: continue
      classes.append(line.strip())
  
  number_of_classes = len(classes)

  data = {
      'path': 'data',
      'train': 'train/images',
      'val': 'validation/images',
      'nc': number_of_classes,
      'names': classes
  }

  with open(path_to_data_yaml, 'w') as f:
    yaml.dump(data, f, sort_keys=False)
  
  print(f'Created config file at {path_to_data_yaml}')

  return


def create_data_yaml_from_set_yaml(path_to_set_yaml: str, path_to_data_yaml: str):
  if not os.path.exists(path_to_set_yaml):
    print(f'set data.yaml not found at {path_to_set_yaml}')
    return

  with open(path_to_set_yaml, 'r') as f:
    src_yaml = yaml.safe_load(f)

  names: List[str] = src_yaml.get('names', []) or []
  if not isinstance(names, list) or len(names) == 0:
    print('Could not read class names from set data.yaml. Aborting.')
    return

  number_of_classes = int(src_yaml.get('nc', len(names)))

  data = {
      'path': 'data',
      'train': 'train/images',
      'val': 'validation/images',
      'nc': number_of_classes,
      'names': names
  }

  with open(path_to_data_yaml, 'w') as f:
    yaml.dump(data, f, sort_keys=False)

  print(f'Created config file at {path_to_data_yaml} from {path_to_set_yaml}')

  return


def create_data_yaml_from_set_and_classes(path_to_set_yaml: str, path_to_classes_txt: str, path_to_data_yaml: str):
  if not os.path.exists(path_to_set_yaml):
    print(f'set data.yaml not found at {path_to_set_yaml}')
    return None

  with open(path_to_set_yaml, 'r') as f:
    set_yaml = yaml.safe_load(f)

  set_names: List[str] = set_yaml.get('names', []) or []
  if not isinstance(set_names, list):
    print('Invalid names list in set data.yaml')
    return None

  custom_names: List[str] = []
  if os.path.exists(path_to_classes_txt):
    with open(path_to_classes_txt, 'r') as f:
      for line in f.readlines():
        line = line.strip()
        if line:
          custom_names.append(line)

  final_names: List[str] = []
  seen = set()
  for n in set_names:
    if n not in seen:
      final_names.append(n)
      seen.add(n)
  for n in custom_names:
    if n not in seen:
      final_names.append(n)
      seen.add(n)

  data = {
      'path': 'data',
      'train': 'train/images',
      'val': 'validation/images',
      'nc': len(final_names),
      'names': final_names
  }

  with open(path_to_data_yaml, 'w') as f:
    yaml.dump(data, f, sort_keys=False)

  print(f'Created config file at {path_to_data_yaml} from union of {path_to_set_yaml} and {path_to_classes_txt}')

  return final_names