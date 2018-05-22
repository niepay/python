import os
import shutil
import glob
import datetime




d = datetime.date.today()
dest_dir_name = ('%d' % d.year + "-" + '%02d' % d.month)
print(dest_dir_name)
source_dir = ("X:/DIG_SPA_FS1/alphasat-hdf5/WebcamHilmwarte")
#filename = source_dir + '/143.224.252.23_01_' + '%d' % d.year + '%02d' % d.month

for filename in glob.glob(os.path.join(source_dir + '/143.224.252.23_01_' + '%d' % d.year + '%02d' % d.month + '*')):
    shutil.r
