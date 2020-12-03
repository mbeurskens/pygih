# Pylint Git Hook Installer
Do you want your Python codebase to be readable and understandable?
Have you ever thought about including [pylint](https://github.com/PyCQA/pylint)
as part of your local workflow automatically? Then _pygih_ (pronounced "piggy") is the tool for you!

Automatically connect _pylint_ to [a git hook](https://git-scm.com/book/en/v1/Customizing-Git-Git-Hooks)
to automatically run it on git events like _pre-commit_ and _pre-push_. Take the hastle out of
setting up pylint for your personal workflow. _Pygih_ is a simple command line tool to
quickly add _pylint_ to your git hooks. 

~Mickey

## Setup and Quickstart
First install _pylint_ using your favourite method such as conda or pip.

`pip install pylint`

_Pygih_ can be run from the command line. This setup assumes that you start a command prompt
from the root of the _pygih_ repository. Run the following from the command line to install 
the git hook with _pylint_:

`python pygih.py --dir /path/to/target/repository`

This will install a _pre-commit_ git hook to run pylint on all python files in that repository.
The git hook will be configured such that it only generates warnings. It does not
block commits when pylint returns warnings or errors.

__The current version of pygih will overwrite an existing git hook configuration.__
As safety, you can set a flag to copy an existing hook to a similarly named file with a time
stamp. It can be found in `.git/hooks`. For a full list of options you can use the `--help` flag.

`python pygih.py --help`

Try to commit some code a check the results.

## Custom Usage
_Pygih_ supports a number of command line arguments that can be used to
alter the git hook settings. Some common settings are featured here. 

First consider you would like to make sure that a git action aborts when
_pylint_ returns errors or warnings. That can be done by using the `--strict` flag.

`python pygih.py --dir path/to/target/repository --strict`

If you would like to append _pygih_ settings to an existing hook file, 
use the `--append` flag. 

`python pygih.py --dir path/to/target/repository --append`

In order to make a backup of the current hook file before editing or replacing,
you can use `--backup`. It will be placed in `repo/.git/hooks`.

`python pygih.py --dir path/to/target/repository --backup`

Now a combination: You can run _pygih_ in strict mode, make a backup of the current
hook file and install _pylint_ in addition to other settings in the _pre-push_ hook instead of the _pre-commit_ hook.
You'd also like to ignore some folder that you have to use, but will not fix yourself.

`python pygih.py --dir path/to/target/repository --strict --append --backup --hook pre-push --ignore somedir 
stuff/subdir`

Have a look at `python pygih.py --help` for more details. Happy coding!