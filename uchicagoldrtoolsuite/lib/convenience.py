def get_valid_types():
    from uchicagoldrtoolsuite.configuration import LDRConfiguration
    config = LDRConfiguration()
    types = config.get_a_config_data_value('outputinformation', 'valid_types')
    a_list = types.split(',')
    return a_list


def sane_hash(hash_algo, file_path, block_size=65536):
    """
    compute a hash hexdigest without loading giant things into RAM

    __Args__

    1. hash_algo (str): an algo with an implementation hooked
        - md5
        - sha256
    2. file_path (str): the abspath to the file

    __KWArgs__

    * block_size (int): How many bytes to load into RAM at once

    __Returns__

    * (str): The hexdigest of the specified hashing algo on the file
    """
    from hashlib import md5, sha256
    if hash_algo == 'md5':
        hasher = md5
    elif hash_algo == 'sha256':
        hasher = sha256
    else:
        raise NotImplemented('Hashing algos supported are md5 and sha256')

    hash_result = hasher()
    with open(file_path, 'rb') as f:
        while True:
           try:
              data = f.read(block_size)
           except OSError as e:
              stderr.write("{} could not be read\n".format(file_path))
              stderr.write(e)
              Stderr.write("\n")
           if not data:
              break
           hash_result.update(data)
    return str(hash_result.hexdigest())


def retrieve_resource_filepath(resource_path, pkg_name=None):
    """
    retrieves the filepath of some package resource, extracting it if need be

    __Args__

    1. resource_path (str): The path to the resource in the package

    __KWArgs__

    * pkg_name (str): The name of a package. Defaults to the project name

    __Returns__

    * (str): The filepath to the resource
    """
    from pkg_resources import Requirement, resource_filename
    if pkg_name is None:
        pkg_name = 'uchicagoldr'
    return resource_filename(Requirement.parse(pkg_name), resource_path)


def retrieve_resource_string(resource_path, pkg_name=None):
    """
    retrieves the string contents of some package resource

    __Args__

    1. resource_path (str): The path to the resource in the package

    __KWArgs__

    * pkg_name (str): The name of a package. Defaults to the project name

    __Returns__

    * (str): the resource contents
    """
    from pkg_resources import Requirement, resource_string
    if pkg_name is None:
        pkg_name = 'uchicagoldr'
    return resource_string(Requirement.parse(pkg_name), resource_path)


def retrieve_resource_stream(resource_path, pkg_name=None):
    """
    retrieves a stream of the contents of some package resource

    __Args__

    1. resource_path (str): The path to the resource in the package

    __KWArgs__

    * pkg_name (str): The name of a package. Defaults to the project name

    __Returns__

    * (io): an io stream
    """
    from pkg_resources import Requirement, resource_stream
    if pkg_name is None:
        pkg_name = 'uchicagoldr'
    return resource_stream(Requirement.parse(pkg_name), resource_path)


def retrieve_controlled_vocabulary(vocab_name, built=True):
    """
    retrieves a controlled vocabulary from the package resources

    __Args__

    1. vocab_name (str): The name of some cv in controlledvocabs/ sans .json

    __KWArgs__

    * built (bool): Whether or not to build the FromJson object. Defaults
    to true. (This is not the same as building the cv itself)

    __Returns__

    * if built==True: An unbuilt controlled vocabulary
    * if built==False: An unbuilt ControlledVocabularyFromSource object
    """
    from controlledvocab.lib import ControlledVocabFromJson
    fname = retrieve_resource_filepath('controlledvocabs/'+vocab_name+'.json')
    cv = ControlledVocabFromJson(fname)
    if built:
        cv = cv.build()
    return cv
