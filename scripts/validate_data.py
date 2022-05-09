""" Python script to validate data

Run as:

    python3 scripts/validata_data.py data
"""

import os
import sys
import hashlib


def file_hash(filename):
    """ Get byte contents of file `filename`, return SHA1 hash

    Parameters
    ----------
    filename : str
        Name of file to read

    Returns
    -------
    hash : str
        SHA1 hexadecimal hash string for contents of `filename`.
    """
    fobj = open(filename, 'rb')  # 'rb' means Read Bytes.
    byte_contents = fobj.read()
    fobj.close()
    hash = hashlib.sha1(byte_contents).hexdigest()
    return hash


def validate_data(data_directory):
    """ Read ``hash_list.txt`` file in ``data_directory``, check hashes
    
    An example file ``data_hashes.txt`` is found in the baseline version
    of the repository template for your reference.

    Parameters
    ----------
    data_directory : str
        Directory containing data and ``hash_list.txt`` file.

    Returns
    -------
    None
    Raises
    ------
    ValueError:
        If hash value for any file is different from hash value recorded in
        ``hash_list.txt`` file.
    """
    hash_list = os.path.join(data_directory, 'group-00', 'hash_list.txt')
    with open(hash_list, "r") as fobj:
        hash_lines = fobj.readlines()
    
    for line in hash_lines:
        hash, file_path = line.split(' ')
        file_path = os.path.join(data_directory, file_path)
        if '\n' in file_path:
            file_path = file_path.replace('\n', '')
        assert hash == file_hash(file_path)


def main():
    # This function (main) called when this file run as a script.
    #
    # Get the data directory from the command line arguments
    if len(sys.argv) < 2:
        raise RuntimeError("Please give data directory on "
                           "command line")
    data_directory = sys.argv[1]
    # Call function to validate data in data directory
    validate_data(data_directory)


if __name__ == '__main__':
    # Python is running this file as a script, not importing it.
    main()
