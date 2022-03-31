import imp
import os
import shutil

importlist = os.listdir("./implementations")
counter = 0
dst_path = './runFiles'

for importfile in importlist:
    src_path = './implementations/' + importfile + '/deserialization.py'
    os.rename(src_path, "deserialization" + str(counter)+'.py')
    shutil.copyfile(src_path,dst_path)
    counter += 1
    print(src_path, dst_path)