from os import listdir, makedirs
from os.path import join, dirname
from uuid import uuid1
import mimetypes

from pypremis.lib import PremisRecord

from ...core.lib.bash_cmd import BashCommand
from .abc.converter import Converter
from .presformmaterialsuite import PresformMaterialSuite
from .ldritemoperations import copy
from .ldrpath import LDRPath


class OfficeToPDFConverter(Converter):

    libre_office_path = "/Applications/LibreOffice.app/Contents/MacOS/soffice"

    _claimed_mimes = [
        'text/plain',
        'text/csv',
        'application/rtf',
        'application/pdf',
        'application/msword',
        'application/vnd.ms-powerpoint',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ]

    _claimed_extensions = [
        '.doc',
        '.docx',
        '.odt',
        '.fodt',
        '.xls',
        '.xlsx',
        '.ods',
        '.fods',
        '.ppt',
        '.pptx',
        '.odp',
        '.fodp',
        '.odf',
        '.odg',
        '.pdf',
        '.txt',
        '.rtf'
    ]

    mimetypes.init()
    for x in _claimed_extensions:
        try:
            _claimed_mimes.append(mimetypes.types_map[x])
        except KeyError:
            pass

    _claimed_mimes = list(set(_claimed_mimes))

    def __init__(self, input_materialsuite, working_dir=None,
                 timeout=None):
        super().__init__(input_materialsuite,
                         working_dir=working_dir, timeout=timeout)

    def convert(self):
        initd_premis_file = join(self.working_dir, str(uuid1()))
        outdir = join(self.working_dir, str(uuid1()))
        makedirs(outdir)
        copy(self.source_materialsuite.premis, LDRPath(initd_premis_file))
        orig_premis = PremisRecord(frompath=initd_premis_file)
        orig_name = orig_premis.get_object_list()[0].get_originalName()
        target_containing_dir = join(self.working_dir, str(uuid1()))
        target_path = join(target_containing_dir, orig_name)
        makedirs(dirname(target_path), exist_ok=True)
        copy(self.source_materialsuite.content, LDRPath(target_path))

        cmd_out = []
        convert_cmd_args = [self.libre_office_path, '--headless',
                            '--convert-to', 'pdf', '--outdir', outdir,
                            target_path]
        convert_cmd = BashCommand(convert_cmd_args)
        convert_cmd.set_timeout(self.timeout)
        convert_cmd.run_command()
        cmd_out.append(convert_cmd.get_data())
        try:
            where_it_is = join(outdir, listdir(outdir)[0])
        except:
            where_it_is = None
        if where_it_is is not None:
            presform_ldrpath = LDRPath(where_it_is)
            presform_ms = PresformMaterialSuite()
            presform_ms.set_extension(".pdf")
            presform_ms.set_content(presform_ldrpath)
            self.get_source_materialsuite().add_presform(presform_ms)
