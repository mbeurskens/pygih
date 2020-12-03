""" Run pylint automatically in git repositories by installing it in git hooks. """

import argparse
import os
import shutil
import datetime

hook_file_types = ['pre-commit', 'pre-push']


def _get_file_mode(arguments) -> str:
    if arguments.append:
        return "a"
    return "w"


def _check_for_hooks_dir(hook_path):
    """ Check if hook directory exists. """
    if not os.path.exists(hook_path):
        raise NotADirectoryError("Cannot find hook directory " + hook_path)


def _check_if_repo(path) -> bool:
    """ Check if the directory in 'path' is a git repository. """
    if os.path.exists(os.path.join(path, '.git')):
        return True
    return False


def _create_hook_backup(file_path, backup):
    """ Create a backup of the hook file if the backup flag is set. """
    if backup and os.path.exists(file_path):
        shutil.copy(file_path, file_path +
                    datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.copy')


def _write_hook_file(file, arguments):
    """ Write hook file based on arguments. """
    ignore_string = ''
    if arguments.ignore:
        ignore_statements = []
        for ign in arguments.ignore:
            ignore_statements.append('-path ' + ign)
        ignore_string = ' '.join(ignore_statements)
    file.write("echo 'Linting files' \n")
    if not arguments.strict:
        file.write("echo 'Pylint hook not running in strict mode."
                   " Errors are shown but no error code will be returned.' \n")
    file.write(r"FILES=$(find . -type d \( " + ignore_string +
               r" \) -prune -false -o -name '*.py')" + "\n")
    file.write(r"pylint $FILES " + "\n")
    if arguments.strict:
        file.write("if [ $? -ne 0 ]\n" +
                   "then\n" +
                   "echo 'Currently running pygih strict mode'\n" +
                   "echo 'Not all pylint tests passed, aborting...'\n" +
                   "exit 1\n" +
                   "fi\n")
    file.write("echo 'Done' \n")
    file.write("exit 0")


def _install_pylint_hook(arguments):
    hook_path = os.path.join(arguments.dir, '.git', 'hooks')
    file_path = os.path.join(hook_path, arguments.hook)
    _check_for_hooks_dir(hook_path)
    _check_if_repo(arguments.dir)
    _create_hook_backup(file_path, arguments.backup)

    with open(file_path, _get_file_mode(arguments)) as file:
        _write_hook_file(file, arguments)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add pylint to git hooks.')
    parser.add_argument('--hook', type=str, default='pre-commit',
                        help='Choose a hook type from the list of supported '
                             'hooks: ' + str(hook_file_types) + '. Uses pre-commit ')
    parser.add_argument('--strict', action='store_true', default=False,
                        help='When strict mode is enabled, an action will '
                             'be rejected until all pylint warnings are '
                             'solved.')
    parser.add_argument('--backup', action='store_true', default=False,
                        help='When a git hook file is replaced, the original'
                             'will be copied.')
    parser.add_argument('--append', action='store_true', default=False,
                        help='Append pylint hook to the git hook if a current '
                             'git hook is already in place.')
    parser.add_argument('--dir', type=str, default='.',
                        help='Target install directory. Uses the current'
                             ' directory by default.')
    parser.add_argument('--ignore', type=str, nargs='+',
                        help='List of directories and files to ignore.')
    args = parser.parse_args()

    dir_path = os.path.realpath(args.dir)
    if not _check_if_repo(dir_path):
        raise NotADirectoryError("The directory '" + dir_path + "' is not "
                                                                "a git repository")
    _install_pylint_hook(args)
