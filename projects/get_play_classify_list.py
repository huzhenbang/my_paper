#coding=gbk
import os
import string
import json

foreign_aid_id_ls = []
path_dir = 'G:\CBA_files\projects\img\外援'
for rt, dirs, files in os.walk(path_dir):
    for f in files:
        ind1 = string.rfind(f, '_')
        ind2 = string.rfind(f, '.')
        foreign_aid_id_ls.append(f[ind1+1:ind2])

json_str = json.dumps(foreign_aid_id_ls, indent=4)
with open('foreign_aid_id_ls.txt', 'w') as f:
    f.write(json_str)
