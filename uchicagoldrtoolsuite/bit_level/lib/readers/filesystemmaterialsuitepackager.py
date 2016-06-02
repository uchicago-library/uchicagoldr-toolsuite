from os import listdir
from os.path import join, dirname, basename, isfile, splitext
from re import compile as re_compile

from .abc.materialsuitepackager import MaterialSuitePackager
from .filesystempresformmaterialsuitepackager import \
    FileSystemPresformMaterialSuitePackager
from ..ldritems.ldrpath import LDRPath


__author__ = "Brian Balsamo, Tyler Danstrom"
__email__ = "balsamo@uchicago.edu, tdanstrom@uchicago.edu"
__company__ = "The University of Chicago Library"
__copyright__ = "Copyright University of Chicago, 2016"
__publication__ = ""
__version__ = "0.0.1dev"


class FileSystemMaterialSuitePackager(MaterialSuitePackager):
    """
    Reads a file system MaterialSuite serialization and knows how to package
    material suites from the contents for inclusion in segment structures
    """
    def __init__(self, stage_env_path, stage_id, label_text, label_number,
                 rel_content_path):
        """
        spawn a packager

        __Args__

        1. stage_env_path (str): The file system path to the staging environment
        2. stage_id (str): The stage identifier for the stage on disk
        3. label_text (str): The text that makes up the first part of the
            segment identifier
        4. label_number (int): The number that makes up the second part of
            the segment identifier
        5. rel_content_path (str): The **relative** path to the content in
            the segment which should have some of the parts of a MaterialSuite
        """
        super().__init__()
        self.stage_env_path = stage_env_path
        self.stage_id = stage_id
        self.label_text = label_text
        self.label_number = label_number
        self.set_implementation('file system')
        self.rel_content_path = rel_content_path
        stage_fullpath = join(stage_env_path, stage_id)
        self.data_fullpath = join(stage_fullpath, 'data',
                                  label_text + "-" + str(label_number))
        self.file_fullpath = join(self.data_fullpath, self.rel_content_path)
        self.file_name = basename(self.rel_content_path)
        self.admin_fullpath = join(stage_fullpath, 'admin',
                                   label_text + "-" + str(label_number))

    def get_content(self):
        return LDRPath(self.file_fullpath,
                       root=self.data_fullpath)

    def get_techmd_list(self):
        fits_path = join(self.admin_fullpath,
                         "TECHMD",
                         self.rel_content_path+".fits.xml")
        if isfile(fits_path):
            return [
                LDRPath(
                    fits_path, root=join(self.admin_fullpath, "TECHMD")
                )
            ]
        return None

    def get_presform_list(self):
        presforms = []
        presform_filename_pattern = re_compile(
            "^{}\.presform(\.[a-zA-Z0-9]*)?$".format(
                self.file_name
            )
        )
        containing_folder_path = join(self.data_fullpath,
                                      dirname(self.rel_content_path))
        siblings = [x for x in listdir(containing_folder_path)]
        for x in siblings:
            if presform_filename_pattern.match(x):
                presform_extension = splitext(x)[1]
                presforms.append(
                    FileSystemPresformMaterialSuitePackager(
                        self.stage_env_path,
                        self.stage_id,
                        self.label_text,
                        self.label_number,
                        self.rel_content_path+".presform"+presform_extension
                    ).package()
                )
        if len(presforms) > 0:
            return presforms
        return None

    def get_premis(self):
        premis_path = join(self.admin_fullpath,
                           "PREMIS",
                           self.rel_content_path+".premis.xml")
        if isfile(premis_path):
            return LDRPath(premis_path,
                           root=join(self.admin_fullpath, "PREMIS"))
        return None
