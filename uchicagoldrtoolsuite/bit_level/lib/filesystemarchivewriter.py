
from os import makedirs
from os.path import basename, dirname, exists, join, split
from sys import stderr

from uchicagoldrtoolsuite.core.lib.idbuilder import IDBuilder

from .abc.archiveserializationwriter import ArchiveSerializationWriter
from .archive import Archive
from .archivefitsmodifier import ArchiveFitsModifier
from .archivemanifestwriter import ArchiveManifestWriter
from .archivepremismodifier import ArchivePremisModifier

from .archiveauditor import ArchiveAuditor
from .ldritemoperations import copy
from .ldrpath import LDRPath
from .pairtree import Pairtree
from .premisdigestextractor import PremisDigestExtractor

__author__ = "Tyler Danstrom"
__email__ = " tdanstrom@uchicago.edu"
__company__ = "The University of Chicago Library"
__copyright__ = "Copyright University of Chicago, 2016"
__publication__ = ""
__version__ = "0.0.1dev"


class FileSystemArchiveWriter(ArchiveSerializationWriter):
    """
    writes an archive structure to the file system as a directory
    """
    def __init__(self, aStructure, archive_loc, origin_loc):
        """
        initialize the writer

        __Args__

        1. aStructure (StagingStructure): The structure to write
        2. archive_loc (str): the root directory for the archive of the ldr
        3. origin_loc (str): the root directory of the stage directory
        being archived

        """
        self.structure = aStructure
        self.pairtree = Pairtree(self.structure.identifier)
        self.audit_qualification = ArchiveAuditor(origin_loc, aStructure)
        self.origin_root = split(origin_loc)[0]
        self.identifier = IDBuilder().build('premisID')
        self.premis_modifier = ArchivePremisModifier
        self.fits_modifier = ArchiveFitsModifier
        self.file_digest_extraction = PremisDigestExtractor
        self.manifest_writer = ArchiveManifestWriter(archive_loc)
        self.archive_loc = archive_loc

    def write(self):
        """
        checks of the structure is validate and audits the contents of the
        structure for errors.

        If the structure is valid and there are no errors in the audit it
        serializes the structure to disk which includes the following steps

        1. modifies premis records in the structure to include archive
        information

        2. modifies fits technical metadata records to include archive
        information

        3. sets up archive file serialization structure and copies contents
        of the structure into the serialization structure

        4. extracts message digests for the resource files from premis records
        and appends them with the new file location to the archive manifest

        """
        print(self.audit_qualification.audit())
        # if self.structure.validate() and self.audit_qualification.audit():

        #     pairtree_path = self.pairtree.get_pairtree_path()
        #     data_dir = join(self.archive_loc, pairtree_path, 'data')
        #     admin_dir = join(self.archive_loc, pairtree_path, 'admin')
        #     makedirs(data_dir, exist_ok=True)
        #     makedirs(admin_dir, exist_ok=True)
        #     accrecord_dir = join(admin_dir, 'accessionrecord')
        #     legalnote_dir = join(admin_dir, 'legalnotes')
        #     adminnote_dir = join(admin_dir, 'adminnotes')
        #     makedirs(accrecord_dir, exist_ok=True)
        #     makedirs(legalnote_dir, exist_ok=True)
        #     makedirs(adminnote_dir, exist_ok=True)
        #     for n_acc_record in self.structure.accessionrecord_list:
        #         acc_filename = basename(n_acc_record.content.item_name)
        #         copy(n_acc_record.content, LDRPath(
        #             join(accrecord_dir,
        #                  acc_filename)))
        #     for n_legal_note in self.structure.legalnote_list:
        #         legalnote_filename = basename(n_legal_note.
        #                                       content.item_name)
        #         copy(n_legal_note.content, LDRPath(
        #             join(legalnote_dir,
        #                  legalnote_filename)))
        #     for n_adminnote in self.structure.adminnote_list:
        #         adminnote_filename = basename(n_adminnote.content.
        #                                       item_name)
        #         copy(n_adminnote.content.itemB, LDRPath(
        #             join(adminnote_dir,
        #                  adminnote_filename)))
        #     for n_segment in self.structure.segment_list:
        #         segment_id = n_segment.label+'-'+str(n_segment.run)
        #         techmd_dir = join(admin_dir, segment_id, 'TECHMD')
        #         premis_dir = join(admin_dir, segment_id, 'PREMIS')
        #         segment_data_dir = join(data_dir, segment_id)
        #         makedirs(techmd_dir, exist_ok=True)
        #         makedirs(premis_dir, exist_ok=True)
        #         makedirs(segment_data_dir, exist_ok=True)
        #         for n_msuite in n_segment.materialsuite_list:
        #             n_content_destination_fullpath = join(
        #                 data_dir, segment_id, n_msuite.content.item_name)
        #             new_premis_record = self.premis_modifier(
        #                 n_msuite.premis, n_content_destination_fullpath).\
        #                 modify_record
        #             digest_data = self.file_digest_extraction(n_msuite.premis)
        #             self.manifest_writer(
        #                 n_content_destination_fullpath, digest_data)
        #             makedirs(
        #                 join(data_dir, dirname(
        #                     n_msuite.content.item_name)), exist_ok=True)
        #             makedirs(
        #                 join(premis_dir, dirname(
        #                     n_msuite.content.item_name)), exist_ok=True)
        #             makedirs(
        #                 join(techmd_dir, dirname(
        #                     n_msuite.content.item_name)), exist_ok=True)

        #             new_premis_path = join(
        #                 premis_dir, n_msuite.premis.item_name)
        #             new_content_path = join(
        #                 data_dir, n_msuite.content.item_name)
        #             new_content_ldrpath = LDRPath(new_content_path)
        #             new_premis_record.write(new_premis_path)
        #             copy(n_msuite.content, new_content_ldrpath)

        #             for n_techmd in n_msuite.technicalmetadata_list:
        #                 new_tech_record_loc = join(
        #                     techmd_dir, n_techmd.content.item_name)
        #                 new_tech_record = self.fits_modifier(
        #                     n_techmd, new_tech_record_loc).modify_record()
        #                 new_tech_path = join(
        #                     techmd_dir, n_techmd.item_name)
        #                 new_tech_record.write(new_tech_path)

        #             for n_presform in n_msuite.presform:
        #                 n_destination_fullpath = join(
        #                     data_dir, segment_id, n_presform.content.item_name)
        #                 new_premis_record = self.premis_modifier(
        #                     n_presform.premis, n_destination_fullpath).\
        #                     modify_record()
        #                 digest_data = self.file_digest_extraction(
        #                     n_msuite.premis)
        #                 self.manifest_writer(
        #                     n_destination_fullpath, digest_data)
        #                 makedirs(
        #                     join(data_dir, dirname(
        #                         n_presform.content.item_name)), exist_ok=True)
        #                 makedirs(
        #                     join(premis_dir, dirname(
        #                         n_presform.content.item_name)), exist_ok=True)
        #                 makedirs(
        #                     join(techmd_dir, dirname(
        #                         n_presform.content.item_name)), exist_ok=True)
        #                 new_premis_path = join(
        #                     premis_dir, n_presform.premis.item_name)
        #                 new_presform_content_path = join(
        #                     data_dir, n_presform.content.item_name)
        #                 new_presform_content_ldrpath = LDRPath(
        #                     new_presform_content_path)
        #                 new_premis_record.write(new_premis_path)
        #                 copy(n_presform.content, new_presform_content_ldrpath)

        #                 for n_techmd in n_presform.technicalmetadata_list:
        #                     new_tech_record_loc = join(
        #                         techmd_dir, n_techmd.content.item_name)
        #                     new_tech_record = self.fits_modifier(
        #                         n_techmd, new_tech_record_loc).modify_record()
        #                     new_tech_path = join(
        #                         techmd_dir, n_techmd.item_name)
        #                     new_tech_record.write(new_tech_path)
        # else:
        #     stderr.write(self.structure.explain_results())
        #     stderr.write(self.audit_qualification.show_errors())

    def get_structure(self):
        return self._structure

    def set_structure(self, value):

        if isinstance(value, Archive):
            self._structure = value
        else:
            raise ValueError(
                "FileSystemArchiveWriter reqiures an Archive structure" +
                " in the structure attribute")

    def get_pairtree(self):
        return self._pairtree

    def set_pairtree(self, value):
        if isinstance(value, Pairtree):
            self._pairtree = value
        else:
            raise ValueError(
                "FileSystemArchiveWriter must take an instance of a Pairtree in the pairtree attribute")

    def get_origin_root(self):
        return self._origin_root

    def set_origin_root(self, value):
        if exists(value):
            self._origin_root = value
        else:
            raise ValueError("{} origin root does not exist.".format(value))

    def get_archive_loc(self):
        return self._archive_loc

    def set_archive_loc(self, value):
        if exists(value):
            self._archive_loc = value
        else:
            raise ValueError(
                "{} archive loc does not exist".format(value))

    def get_identifier(self):
        return self._identifier

    def set_identifier(self, value):
        self._identifier = value

    def get_premis_modifier(self):
        return self._premis_modifier

    def set_premis_modifier(self, value):
        self._premis_modifier = value

    def get_fits_modifier(self):
        return self._fits_modifier

    def set_fits_modifier(self, value):
        self._fits_modifier = value

    structure = property(get_structure, set_structure)
    pairtree = property(get_pairtree, set_pairtree)
    origin_root = property(get_origin_root, set_origin_root)
    archive_loc = property(get_archive_loc, set_archive_loc)
    fits_modifer = property(get_fits_modifier, set_fits_modifier)
    premis_modifier = property(get_premis_modifier, set_premis_modifier)
    identifier = property(get_identifier, set_identifier)
