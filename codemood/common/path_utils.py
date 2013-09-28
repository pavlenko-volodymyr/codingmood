from hashlib import md5
from os.path import splitext
from uuid import uuid4

get_md5 = lambda text: md5(text).hexdigest()
get_file_extension = lambda path: splitext(path)[1][1:]


def generate_filename(
        base_folder,
        filename,
        with_path=True,
        get_name=False,
        easy=None):
    """
    Generate unique filename with folder path.
    `with_path` - need folders in new path or no
    `get_name` - get only path or list which contents name, extension and
    dir_name of new file.
    """
    name = get_md5(str(uuid4()))

    extension = get_file_extension(filename)

    extension = extension.lower()

    if with_path:
        if easy is None:
            target = "{0}/{1}/{2}/{name}.{extension}".format(
                name[0], name[1], name[2], name=name, extension=extension)

        elif easy is False:
            target = "{0}/{1}/{name}.{extension}".format(
                name[0], name[1], name=name, extension=extension)
        else:
            target = "{0}/{name}.{extension}".format(
                name[0], name=name, extension=extension,)

        path = "{0}/{1}".format(base_folder.rstrip("/"), target)
    else:
        path = "{0}/{name}.{extension}".format(
            base_folder.rstrip("/"), name=name, extension=extension)

    return path if not get_name else (path, name, extension)


def make_upload_path(instance, filename):
    """
    Generates upload path for FileField
    """
    return generate_filename(instance.UPLOAD_DIR, filename)