# Listening-monster

Web server for uploading mp3 files for translation.

## Installation

To run the server you can manually setup using the requirements.txt. However, for a better experience use [Poetry](https://python-poetry.org/). Poetry will use the `poetry.lock` file to download deps and will make sure the project works on my machine and yours too.

### Tips for configuring poetry

Poetry automatically creates the `virtualenv` for you in `{cache-dir}/virtualenvs/+`. For windows users, this is in `%LOCALAPPDATA%`. If you want your `virtualenv` in this project, remember to execute `poetry config virtualenvs.in-project true`. This is especially good for vscode debuggers. For you peeps, there's configs in `.vscode/launch.json` ready for you.
