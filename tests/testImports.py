import unittest

class TestImports(unittest.TestCase):
    def test_bit_level_imports(self):
        from uchicagoldrtoolsuite.bit_level.lib.filesystemmaterialsuitepackager import FileSystemMaterialSuitePackager
        from uchicagoldrtoolsuite.bit_level.lib.filesystemsegmentpackager import FileSystemSegmentPackager
        from uchicagoldrtoolsuite.bit_level.lib.filesystemstagereader import FileSystemStageReader
        from uchicagoldrtoolsuite.bit_level.lib.filesystemstagewriter import FileSystemStageWriter
        from uchicagoldrtoolsuite.bit_level.lib.ldrpath import LDRPath
        from uchicagoldrtoolsuite.bit_level.lib.ldrurl import LDRURL
        from uchicagoldrtoolsuite.bit_level.lib.absolutefilepathtree import AbsoluteFilePathTree
        from uchicagoldrtoolsuite.bit_level.lib.filepathtree import FilePathTree
        from uchicagoldrtoolsuite.bit_level.lib.filewalker import FileWalker
        from uchicagoldrtoolsuite.bit_level.lib.ldritemoperations import copy
        from uchicagoldrtoolsuite.bit_level.lib.abc.materialsuitepackager import MaterialSuitePackager
        from uchicagoldrtoolsuite.bit_level.lib.abc.presformmaterialsuitepackager import PresformMaterialSuitePackager
        from uchicagoldrtoolsuite.bit_level.lib.materialsuite import MaterialSuite
        from uchicagoldrtoolsuite.bit_level.lib.presformmaterialsuite import PresformMaterialSuite
        from uchicagoldrtoolsuite.bit_level.lib.premisextensionnodes import Restriction
        from uchicagoldrtoolsuite.bit_level.lib.premisobjectrecordcreator import PremisObjectRecordCreator
        from uchicagoldrtoolsuite.bit_level.lib.rootedpath import RootedPath
        from uchicagoldrtoolsuite.bit_level.lib.stage import Stage
        from uchicagoldrtoolsuite.bit_level.lib.segment import Segment
        from uchicagoldrtoolsuite.bit_level.lib.technicalmetadatarecordcreator import TechnicalMetadataRecordCreator
        from uchicagoldrtoolsuite.bit_level.lib.externalfilesystemmaterialsuitepackager import ExternalFileSystemMaterialSuitePackager
        from uchicagoldrtoolsuite.bit_level.lib.externalfilesystemsegmentpackager import ExternalFileSystemSegmentPackager

#       from uchicagoldrtoolsuite.bit_level.lib.archivestructure import ArchiveStructure

        from uchicagoldrtoolsuite.bit_level.lib.abc.abc.packager import Packager
        from uchicagoldrtoolsuite.bit_level.lib.abc.abc.serializationreader import SerializationReader
        from uchicagoldrtoolsuite.bit_level.lib.abc.abc.serializationwriter import SerializationWriter
        from uchicagoldrtoolsuite.bit_level.lib.abc.structure import Structure
        from uchicagoldrtoolsuite.bit_level.lib.abc.ldritem import LDRItem
        from uchicagoldrtoolsuite.bit_level.lib.abc.segmentpackager import SegmentPackager
        from uchicagoldrtoolsuite.bit_level.lib.abc.stageserializationreader import StageSerializationReader
        from uchicagoldrtoolsuite.bit_level.lib.abc.stageserializationwriter import StageSerializationWriter
        from uchicagoldrtoolsuite.bit_level.lib.abc.converter import Converter
        from uchicagoldrtoolsuite.bit_level.lib.abc.technicalmetadatacreator import TechnicalMetadataCreator

        from uchicagoldrtoolsuite.bit_level.lib.genericpremiscreator import GenericPREMISCreator
        from uchicagoldrtoolsuite.bit_level.lib.genericpremisrestrictionsetter import GenericPREMISRestrictionSetter
        from uchicagoldrtoolsuite.bit_level.lib.generictechnicalmetadatacreator import GenericTechnicalMetadataCreator
        from uchicagoldrtoolsuite.bit_level.app.stager import Stager
        from uchicagoldrtoolsuite.bit_level.app.pruner import Pruner
        from uchicagoldrtoolsuite.bit_level.app.technicalmetadatacreator import TechnicalMetadataCreator
        from uchicagoldrtoolsuite.bit_level.app.accessionrecordadder import AccessionRecordAdder
        from uchicagoldrtoolsuite.bit_level.app.adminnoteadder import AdminNoteAdder
        from uchicagoldrtoolsuite.bit_level.app.legalnoteadder import LegalNoteAdder
        from uchicagoldrtoolsuite.bit_level.app.premiscreator import PremisCreator
        from uchicagoldrtoolsuite.bit_level.app.premisrestrictionsetter import PremisRestrictionSetter
        from uchicagoldrtoolsuite.bit_level.app.presformcreator import PresformCreator
        from uchicagoldrtoolsuite.bit_level.app.technicalmetadatacreator import TechnicalMetadataCreator
#        from uchicagoldrtoolsuite.bit_level.app.archiver import Archiver

        from uchicagoldrtoolsuite.bit_level.lib.converters.audioconverter import AudioConverter
        from uchicagoldrtoolsuite.bit_level.lib.converters.imageconverter import ImageConverter
        from uchicagoldrtoolsuite.bit_level.lib.converters.officetocsvconverter import OfficeToCSVConverter
        from uchicagoldrtoolsuite.bit_level.lib.converters.officetopdfconverter import OfficeToPDFConverter
        from uchicagoldrtoolsuite.bit_level.lib.converters.officetotxtconverter import OfficeToTXTConverter
        from uchicagoldrtoolsuite.bit_level.lib.converters.videoconverter import VideoConverter

        from uchicagoldrtoolsuite.bit_level.lib.techmdcreators.fitscreator import FITsCreator


    def test_core_imports(self):
        from uchicagoldrtoolsuite.core.lib.accessionrecorder import AccessionRecorder
        from uchicagoldrtoolsuite.core.lib.bash_cmd import BashCommand
        from uchicagoldrtoolsuite.core.lib.confreader import ConfReader
        from uchicagoldrtoolsuite.core.lib.convenience import \
            iso8601_dt, \
            sane_hash, \
            retrieve_resource_filepath, \
            retrieve_resource_stream, \
            retrieve_controlled_vocabulary
        from uchicagoldrtoolsuite.core.app.abc.abc.app import App
        from uchicagoldrtoolsuite.core.app.abc.cliapp import CLIApp
        from uchicagoldrtoolsuite.core.app.aru import AccessionRecordEditor
        from uchicagoldrtoolsuite.core.app.postinstall import PostInstall

    def test_conceptual_imports(self):
        from uchicagoldrtoolsuite.conceptual.lib.abc.abc.retriever import Retriever
        from uchicagoldrtoolsuite.conceptual.lib.abc.contentpointerresolver import ContentPointerResolver
        from uchicagoldrtoolsuite.conceptual.lib.abc.contentpointerretriever import ContentPointerRetriever
        from uchicagoldrtoolsuite.conceptual.lib.abc.familyretriever import FamilyRetriever
        from uchicagoldrtoolsuite.conceptual.lib.contentpointer import ContentPointer
        from uchicagoldrtoolsuite.conceptual.lib.family import Family
        from uchicagoldrtoolsuite.conceptual.lib.dbcontentpointerresolver import DatabaseContentPointerResolver
        from uchicagoldrtoolsuite.conceptual.lib.dbcontentpointerretriever import DatabaseContentPointerRetriever
        from uchicagoldrtoolsuite.conceptual.lib.dbenvmixin import DatabaseEnvironmentMixin
        from uchicagoldrtoolsuite.conceptual.lib.dbfamilyretriever import DatabaseFamilyRetriever


if __name__ == '__main__':
    unittest.main()
