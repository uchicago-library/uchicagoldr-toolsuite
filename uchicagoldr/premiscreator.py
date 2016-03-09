from os.path import split, getsize, isdir, join
from os import makedirs
from hashlib import md5, sha256
from magic import from_file
from mimetypes import guess_type
from re import sub
from uuid import uuid1
from uchicagoldr.tree import FileProcessor
from pypremis.lib import PremisRecord
from pypremis.nodes import *


class PremisCreator(FileProcessor):
    def __init__(self, directory, source_root, irrelevant_part=None):
        if not isdir(join(directory, 'data')):
            raise ValueError("The specified directory does not have " +
                             "a data subdir")
        self.data_root = join(directory, 'data')
        self.admin_root = join(directory, 'admin')
        FileProcessor.__init__(self, self.data_root, source_root, irrelevant_part)
        for x in self.find_all_files():
            file_path = x.identifier
            record = self.make_record(file_path)
            record_file_path = self.determine_record_location(file_path)
            self.write_record_to_disk(record, record_file_path)

    def make_record(self, file_path):
        obj = self._make_object(file_path)
        return PremisRecord(objects=[obj])

    def determine_record_location(self, file_path):
        origin_path = sub('^'+self.data_root+"/", '', file_path)
        prefix = origin_path.split("/")[0]
        origin_path = sub('^'+prefix+"/", '', origin_path)
        path = join(self.admin_root, prefix, 'PREMIS', origin_path+'.premis.xml')
        return path

    def write_record_to_disk(self, record, file_path):
        if not isdir (split(file_path)[0]):
            makedirs(split(file_path)[0])
        record.write_to_file(file_path)

    def _detect_mime(self, file_path):
        try:
            magic_num = from_file(file_path, mime=True).decode()
        except:
            magic_num = None
        try:
            guess = guess_type(file_path)[0]
        except:
            guess = None
        return magic_num, guess

    def _sane_hash(self, hasher, file_path, block_size=65536):
        hash_result = hasher()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(block_size)
                if not data:
                    break
                hash_result.update(data)
        return str(hash_result.hexdigest())

    def _make_object(self, file_path):
        objectIdentifier = self._make_objectIdentifier()
        objectCategory = 'file'
        objectCharacteristics = self._make_objectCharacteristics(file_path)
        originalName = split(file_path)[1]
        storage = self._make_Storage(file_path)
        obj = Object(objectIdentifier, objectCategory, objectCharacteristics)
        obj.set_originalName(originalName)
        obj.set_storage(storage)
        return obj

    def _make_objectIdentifier(self):
        """
        uses uuid1 to generate DOIs. uuid1 should keep us unique by
        hardware mac and time down to whatever accuracy time.time() has
        plus some entropy. There's really fancy sounding posts on stack
        overflow about why this should be fine
        """
        return ObjectIdentifier("DOI", str(uuid1()))

    def _make_objectCharacteristics(self, file_path):
        fixity1, fixity2 = self._make_fixity(file_path)
        size = str(getsize(file_path))
        formats = self._make_format(file_path)
        objChar = ObjectCharacteristics(formats[0])
        if len(formats) > 1:
            for x in formats[1:]:
                objChar.add_format(x)
        objChar.set_fixity(fixity1)
        objChar.add_fixity(fixity2)
        objChar.set_size(size)
        return objChar

    def _make_Storage(self, file_path):
        contentLocation = self._make_contentLocation(file_path)
        stor = Storage()
        stor.set_contentLocation(contentLocation)
        return stor

    def _make_fixity(self, file_path):
        md5_fixity = Fixity('md5', self._sane_hash(md5, file_path))
        md5_fixity.set_messageDigestOriginator('python3 hashlib.md5')
        sha256_fixity = Fixity('sha256', self._sane_hash(sha256, file_path))
        sha256_fixity.set_messageDigestOriginator('python3 hashlib.sha256')
        return md5_fixity, sha256_fixity

    def _make_format(self, file_path):
        magic_num, guess  = self._detect_mime(file_path)
        formats = []
        if magic_num:
            premis_magic_format_desig = FormatDesignation(magic_num)
            premis_magic_format = Format(formatDesignation=premis_magic_format_desig)
            premis_magic_format.set_formatNote('from magic number (python3 magic.from_file)')
            formats.append(premis_magic_format)
        if guess:
            premis_guess_format_desig = FormatDesignation(guess)
            premis_guess_format = Format(formatDesignation=premis_guess_format_desig)
            premis_guess_format.set_formatNote('from file extension (python3 mimetypes.guess_type)')
            formats.append(premis_guess_format)
        if len(formats) == 0:
            premis_unknown_format_desig = FormatDesignation('undetected')
            premis_unknown_format = Format(formatDesignation=premis_unknown_format_desig)
            premis_unknown_format.set_formatNote('format detection failed by python3 magic.from_file and mimetypes.guess_type')
            formats.append(premis_unknown_format)
        else:
            return formats

        return formatDesignation

    def _make_contentLocation(self, file_path):
        return ContentLocation("Unix File Path", file_path)
