from json import dumps, dump
from os import makedirs
from os.path import exists, join, dirname
from tempfile import TemporaryDirectory
from uuid import uuid4

from pypremis.lib import PremisRecord

from pypairtree.utils import identifier_to_path
from pypairtree.pairtree import PairTree
from pypairtree.pairtreeobject import PairTreeObject
from pypairtree.intraobjectbytestream import IntraObjectByteStream

from uchicagoldrtoolsuite.core.lib.masterlog import spawn_logger
from .abc.archiveserializationwriter import ArchiveSerializationWriter
from ..ldritems.ldrpath import LDRPath
from ..ldritems.ldritemcopier import LDRItemCopier

__author__ = "Brian Balsamo"
__email__ = "balsamo@uchicago.edu"
__company = "The University of Chicago Library"
__publication__ = ""
__version__ = "0.0.1dev"


log = spawn_logger(__name__)


class SegmentedPairTreeObject(PairTreeObject):

    _seg_id = None

    def get_seg_id(self):
        return self._seg_id

    def set_seg_id(self, x):
        self._seg_id = x

    seg_id = property(get_seg_id, set_seg_id)


class FileSystemArchiveWriter(ArchiveSerializationWriter):
    """
    Writes an archive structure to disk utilizing PairTrees as a series
    of directories and files.
    """
    def __init__(self, anArchive, aRoot, eq_detect="bytes"):
        """
        spawn a writer

        """
        super().__init__(anArchive)
        self.lts_env_path = aRoot
        self.eq_detect = eq_detect
        log.debug("FileSystemArchiveWriter spawned: {}".format(str(self)))

    def __repr__(self):
        attr_dict = {
            'lts_env_path': self.lts_env_path,
            'eq_detect': self.eq_detect,
            'struct': str(self.get_struct())
        }
        return "<FileSystemArchiveWriter {}>".format(dumps(attr_dict,
                                                           sort_keys=True))

    def _write_ark_dir(self, clobber=False):
        ark_path = join(
            str(identifier_to_path(self.get_struct().identifier,
                                   root=self.lts_env_path)),
            "arf"
        )
        if exists(ark_path) and not clobber:
            err_text = "The Ark path ({}) ".format(ark_path) + \
                "already exists in the long term storage environment. " + \
                "Aborting."
            log.critical(err_text)
            raise OSError(err_text)
        else:
            makedirs(ark_path, exist_ok=True)
        return ark_path

    def _write_dirs_skeleton(self, ark_path):
        admin_dir_path = join(ark_path, "admin")
        pairtree_root = join(ark_path, "pairtree_root")
        accession_records_dir_path = join(admin_dir_path, "accession_records")
        adminnotes_dir_path = join(admin_dir_path, "adminnotes")
        legalnotes_dir_path = join(admin_dir_path, "legalnotes")

        for x in [admin_dir_path, pairtree_root, accession_records_dir_path,
                  adminnotes_dir_path, legalnotes_dir_path]:
            makedirs(x, exist_ok=True)
        return admin_dir_path, pairtree_root, accession_records_dir_path, \
            adminnotes_dir_path, legalnotes_dir_path

    def _put_materialsuite_into_pairtree(self, materialsuite,
                                         seg_id, pair_tree):
        obj_id = self._get_premis_obj_id(materialsuite.premis)
        o = SegmentedPairTreeObject(identifier=obj_id, encapsulation="arf")
        o.seg_id = seg_id
        content = IntraObjectByteStream(
            materialsuite.content,
            intraobjectaddress="content.file"
        )
        premis = IntraObjectByteStream(
            materialsuite.premis,
            intraobjectaddress="premis.xml"
        )
        if len(materialsuite.technicalmetadata_list) > 1:
            raise NotImplementedError(
                "The Archive serializer currently only supports " +
                "serializing a single FITs record as technical metadata."
            )
        fits = IntraObjectByteStream(
            materialsuite.technicalmetadata_list[0],
            intraobjectaddress="fits.xml"
        )
        o.add_bytestream(content)
        o.add_bytestream(premis)
        o.add_bytestream(fits)
        pair_tree.add_object(o)
        if materialsuite.presform_list:
            for x in materialsuite.presform_list:
                self._put_materialsuite_into_pairtree(x, seg_id, pair_tree)

    def _get_premis_obj_id(self, premis_ldritem):
        with TemporaryDirectory() as tmp_dir:
            premis_path = join(tmp_dir, uuid4().hex)
            tmp_item = LDRPath(premis_path)
            LDRItemCopier(premis_ldritem, tmp_item).copy()
            premis = PremisRecord(frompath=premis_path)
            return premis.get_object_list()[0].get_objectIdentifier()[0].get_objectIdentifierValue()

    def _pack_archive_into_pairtree(self, pair_tree):
        for seg in self.get_struct().segment_list:
            seg_id = seg.identifier
            for materialsuite in seg.materialsuite_list:
                self._put_materialsuite_into_pairtree(materialsuite, seg_id,
                                                      pair_tree)

    def _write_data(self, pair_tree, ark_path, data_manifest):
        for obj in pair_tree.objects:
            for bytestream in obj.bytestreams:
                path = join(ark_path,
                            pair_tree.root_dir_name,
                            str(identifier_to_path(obj.identifier)),
                            obj.encapsulation,
                            bytestream.intraobjectaddress)
                makedirs(dirname(path), exist_ok=True)
                dst_item = LDRPath(path)
                cr = LDRItemCopier(bytestream.openable, dst_item).copy()
                if not cr['src_eqs_dst']:
                    raise ValueError()
                manifest_dict = {
                    'origin': bytestream.openable.item_name,
                    'identifier': obj.identifier,
                    'copy_report': cr,
                    'origin_seg': obj.seg_id,
                    'acc_id': self.get_struct().identifier
                }
                data_manifest.append(manifest_dict)

    def _write_data_manifest(self, data_manifest, admin_dir_path):
        with open(join(admin_dir_path, "data_manifest.json"), 'w') as f:
            dump(data_manifest, f, indent=4, sort_keys=True)

    def write(self):
        log.debug("Writing Archive")

        ark_path = self._write_ark_dir()
        admin_dir_path, pairtree_root, accession_records_dir_path, \
            adminnotes_dir_path, legalnotes_dir_path = \
            self._write_dirs_skeleton(ark_path)

        data_manifest = []

        pair_tree = PairTree(containing_dir=ark_path)
        self._pack_archive_into_pairtree(pair_tree)
        self._write_data(pair_tree, ark_path, data_manifest)
        self._write_data_manifest(data_manifest, admin_dir_path)
