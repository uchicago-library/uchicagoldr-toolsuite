import re
from sys import stderr
from os.path import exists, join, split as dirsplit

from .abc.stageserializationreader import StageSerializationReader
from .stage import Stage
from .absolutefilepathtree import AbsoluteFilePathTree
from .ldrpath import LDRPath
from .materialsuite import MaterialSuite
from .segment import Segment


__author__ = "Brian Balsamo, Tyler Danstrom"
__email__ = "balsamo@uchicago.edu, tdanstrom@uchicago.edu"
__company__ = "The University of Chicago Library"
__copyright__ = "Copyright University of Chicago, 2016"
__publication__ = ""
__version__ = "0.0.1dev"


class FileSystemStageReader(StageSerializationReader):
    """
    Repackages files written to disk as a Staging Structure
    """
    def __init__(self, staging_directory):
        super().__init__()
        self.set_implementation('file system')
        self.stage_id = staging_directory.split('/')[-1]
        self.structureType = "staging"
        self.serialized_location = staging_directory

    def read(self):
        if exists(self.serialized_location):
            tree = AbsoluteFilePathTree(self.serialized_location)
            just_files = tree.get_files()
            data_node_identifier = join(self.serialized_location, 'data')
            data_node_depth = tree.find_depth_of_a_path(data_node_identifier)
            data_node = tree.find_tag_at_depth('data', data_node_depth)[0]
            data_node_subdirs = data_node.fpointer
            stagingstructure = Stage(self.serialized_location.split('/')[-1])
            for n in data_node_subdirs:
                a_past_segment_node_depth = tree.find_depth_of_a_path(n)
                if a_past_segment_node_depth > 0:
                    label = dirsplit(n)[1]
                    valid_pattern = re.compile('(\w{1,})-(\d{1,})')
                    label_matching = valid_pattern.match(label)
                    if label_matching:
                        prefix, number = label_matching.group(1), \
                                         label_matching.group(2)
                        a_new_segment = Segment(prefix, int(number))
                        stagingstructure.segment.append(a_new_segment)
            for n_thing in just_files:
                segment_id = join(self.serialized_location, 'data/')
                if segment_id in n_thing:
                    split_from_segment_id = n_thing.split(segment_id)
                    if len(split_from_segment_id) == 2:
                        file_run = split_from_segment_id[1].split('/')[0]
                        matching_segment = [x for x in stagingstructure.segment
                                            if x.identifier == file_run]
                        if len(matching_segment) == 1:
                            a_file = LDRPath(n_thing)
                            msuite = MaterialSuite(a_file.item_name)
                            msuite.original.append(a_file)
                            matching_segment[0].materialsuite.append(msuite)
                        else:
                            stderr.write("There are more than one segments in" +
                                         " the staging structure with id {}\n".
                                         format(file_run))
                    else:
                        stderr.write("the path for {} is wrong.\n".format(
                            n_thing))

        else:
            stagingstructure = Stage(self.stage_id)
        return stagingstructure

    def set_structure(self, aStructure):
        self.structure = aStructure

    def get_stage_id(self):
        return self._stage_id

    def set_stage_id(self, value):
        self._stage_id = value

    stage_id = property(get_stage_id, set_stage_id)