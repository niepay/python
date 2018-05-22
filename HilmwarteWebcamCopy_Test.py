import os
import shutil
import glob


def copy_files_Webcam( source_path, destination_path, override=False ):

    files_count = 0
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)
    items = glob.glob(source_path + '/143.224.252.23*')

    print (items)
    for item in items:
        if os.path.isdir(item):
            path = os.path.join(destination_path, item.split('/')[-1])
            files_count += recursive_copy_files(source_path=item, destination_path=path, override=override)
        else:
            file = os.path.join(destination_path, item.split('/')[-1])
            print (file)
            print (item)
            print (destination_path)
            if not os.path.exists(file) or override:
                shutil.copyfile(item, file)
                files_count += 1
    return files_count


copy_files_Webcam( "C:\\Users\\nip\\Documents\\copyfrom", "C:\\Users\\nip\\Documents\\copyto", True )
