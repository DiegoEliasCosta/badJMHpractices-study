import os
import hashlib
from slugify import slugify


def formatFileName(df_name):

    param = df_name[-1]
    # Hashing long figure names
    if len(param) > 64:
        hash_object = hashlib.md5(param.encode())
        param = hash_object.hexdigest()

    name = '_'.join(df_name[1:-1])
    name = name + '_' + param
    name = slugify(name)
    return name


def createIfNotExist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
