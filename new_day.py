import re
import shutil
from pathlib import Path

# TODO: rewrite this to .bat script

print(' Creating new advent day '.center(50, '-'))

temp_dir = Path('day00').absolute()

# find number of last day
last_day = sorted(
    folder.name
    for folder in Path('.').iterdir()
    if folder.is_dir() and folder.name.startswith('day')
    )[-1]

print(f'Last day is {last_day}.')

# prepare the paths
last_day_num = int(re.findall(r'\d+', last_day)[0])
new_day_num = last_day_num + 1
new_day_folder_name = f'day{new_day_num:02}'
new_path = Path(new_day_folder_name).absolute()

# copy folder
print(f"Creating folder '{new_day_folder_name}'.")
shutil.copytree(temp_dir, new_path)

# edit run configurations
print('Editing run configuration.')
for file in Path('.run').iterdir():
    print(f' - editing {file}')
    with open(file, 'r') as f:
        contents = f.read()
        new_contents = re.sub(
            fr'{last_day}', fr'{new_day_folder_name}', contents
            )
    with open(file, 'w') as f:
        f.write(new_contents)

print(' Finished '.center(50, '-'))
