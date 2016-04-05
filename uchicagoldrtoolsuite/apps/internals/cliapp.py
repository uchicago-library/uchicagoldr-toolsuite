from argparse import ArgumentParser
from sys import stdout, stderr
from os.path import isabs, join, isdir, isfile, exists, split
from os import makedirs
from uchicagoldrtoolsuite.apps.internals.app import App
from uchicagoldrtoolsuite.configuration.confreader import ConfReader


class CLIApp(App):
    """
    The base class for CLI applications, from which specific
    applications should be derived.

    __Provided Methods__

    * spawn_parser (ArgumentParser): Creates the parser boilerplate,
    with the command line flags that all applications set."
    * Prompts
        * prompt (*): Prompt the user for an arbitrary something (usually a str)
        and get their response. The most general user interaction method.
        * bool_prompt (bool/None): Prompt the user for a boolean answer and
        get their response
        * choose_from_prompt (*): Ask the user to choose an element from a list
        * path_prompt (str): Ask the user for a path, get one
    * Prints
        * stdoutp: Print something to standard output
        * stderrp: Print something to standard error
    * Utility
        * create_path: Makes a file or a dir at some path
    """
    def __init__(self, __author__=None, __email__=None, __company__=None,
                 __copyright__=None, __publication__=None, __version__=None):
        App.__init__(
            self,
            __author__=__author__,
            __email__=__email__,
            __company__=__company__,
            __copyright__=__copyright__,
            __publication__=__publication__,
            __version__=__version__
        )

    def spawn_parser(self, **kwargs):
        parser = ArgumentParser(**kwargs)

        # Always allow the user to specify an alternate conf dir
        parser.add_argument(
            '--conf-dir',
            default=None,
            help="Specify a custom configuration directory to be parsed "
            "with precedence over the default and builtin configs."
        )
        # Always allow the user to specify an alternate conf file
        parser.add_argument(
            '--conf-file',
            default=None,
            help="Specify a custom configuration filename, if required."
        )
        # Always allow the user to specify verbosity
        parser.add_argument(
            '-v',
            '--verbose',
            action='count',
            default=0,
            help="Cause the program to output verbosely."
        )
        self.parser = parser

    def prompt(self, prompt, default=None, disp_default=None, closing=None):
        if not disp_default:
            disp_default = str(default)
        if not default:
            disp_prompt = "{}: ".format(prompt)
        else:
            disp_prompt = "{} ({}): ".format(prompt, disp_default)
        answer = input(disp_prompt)
        if answer == '':
            answer = default
        if closing:
            stdout.write("{}\n".format(closing))

        return answer

    def bool_prompt(self, prompt, default=None, closing=None):
        pos_in = ['t', 'true', 'y', 'yes', '1', 1, True]
        neg_in = ['f', 'false', 'n', 'no', '0', 0, False]
        if default not in pos_in + neg_in and default is not None:
            raise AssertionError('bool_input is for getting bools.')
        answer = self.prompt(prompt, default=default, closing=closing)
        if answer in pos_in:
            return True
        elif answer in neg_in:
            return False
        elif answer is None:
            return None
        else:
            return IOError()

    def choose_from_prompt(self, prompt, choices, choice_str_list=None,
                           default=None, closing=None):
        if choice_str_list is None:
            choice_str_list = []
            for i, x in enumerate(choices):
                choice_str_list.append("{}) {}".format(str(i), str(x)))
            choice_str = "\n".join(choice_str_list)
        else:
            for i, x in enumerate(choice_str_list):
                choice_str_list[i] = "{}) {}".format(str(i), x)
            choice_str = "\n".join(choice_str_list)
        prompt = "{}\n{}\n".format(prompt, choice_str) + \
            "Selection"
        answer = self.prompt(prompt, default=default, closing=closing)
        if isinstance(answer, str):
            for x in answer:
                if x not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    answer = None
                break
            if answer is not None:
                answer = int(answer)
        if answer is None:
            return None
        else:
            return choices[answer]

    def path_prompt(self, prompt, default=None, closing=None,
                    disp_default=None, must_exist=False, must_be_absolute=False,
                    must_be_relative=False, root=None, must_be_file=False,
                    must_be_dir=False):
        prompt = "{}\nPath".format(prompt)
        answer = self.prompt(prompt, default=default, disp_default=disp_default,
                             closing=closing)
        if must_be_absolute:
            if not isabs(answer):
                return False
        if must_be_relative:
            if isabs(answer):
                return False
        if root:
            testpath = join(root, answer)
        else:
            testpath = answer
        if must_exist:
            if not exists(testpath):
                return False
        if must_be_file:
            if not isfile(testpath):
                return False
        if must_be_dir:
            if not isdir(testpath):
                return False
        return answer

    def create_path(self, file_or_dir, path=None):
        if file_or_dir != 'dir' and file_or_dir != 'file':
            raise AssertionError('Specify either \'file\' or \'dir\'')
        if path is None:
            if file_or_dir == 'dir':
                diropt = True
                fileopt = False
            else:
                fileopt = True
                diropt = False
            path = self.path_prompt("Please specify a path to create",
                                    must_be_absolute=True,
                                    must_be_file=fileopt,
                                    must_be_dir=diropt)
            if not path:
                return False
        if file_or_dir == 'file':
            cdir = split(path)[0]
            if not exists(cdir):
                makedirs(cdir)
            if not exists(path):
                open(path, 'w').close()
            return True
        if file_or_dir == 'dir':
            if not exists(path):
                makedirs(path)
            return True

    def stdoutp(self, message, end='\n', sanitize=True):
        if sanitize:
            message = str(message)
            end = str(end)
        stdout.write(message+end)

    def stderrp(self, message, end='\n', sanitize=True):
        if sanitize:
            message = str(message)
            end = str(end)
        stderr.write(message+end)

    def get_config(self, config_directory=None, config_file=None):
        return ConfReader(config_directory=config_directory,
                          config_file=config_file,)