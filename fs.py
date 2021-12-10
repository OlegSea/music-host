import os

def scanDir(path):
  if path.endswith('/'):
    path = path[0:-2]
  directory = []
  for file in os.scandir(path):
    if file.is_dir:
      directory.append(scanDir(f'{path}/{file.name.replace(" ", "\ ")}'))
    else:
      directory.append(file.name)
    return directory

print(scanDir('/home/olegsea/Music'))