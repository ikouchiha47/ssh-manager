import ntpath
import os

class FileWriter:
    def __init__(self, filepath):
        self.full_filepath = os.path.expanduser(filepath)
        (self.repo, self.is_new_repo) = self.__get_repo()

    def __generate_backup_file_name(self):
        # bad idea
        # use git
        full_filename = ntpath.basename(self.full_filepath)
        dirname = ntpath.dirname(self.full_filename)
        filename, extension = os.path.splitext(full_filename)

        for i in range(1, 30):
            for file in os.listdir(dirname):
                new_file_name = "%s.%d.%s" % (filename, i, extension)
                if ntpath.basename(file) !=  new_file_name:
                    return new_file_name

        # after 30 backups. its time to recycle it.
        # assuming the 1.bkp is the last valid one, we recycle from .2.bkp
        return "%s.2.%s" % (filename, extension)

    def __get_repo(self):
        repo = None
        is_new_repo = False
        dirname = ntpath.dirname(self.full_filepath)

        try:
            repo = git.Repo(dirname)
        except git.exc.InvalidGitRepositoryError:
            repo = git.Repo.init(dirname)
            is_new_repo = True

        return (repo, is_new_repo)

    def __changed_files(self, full_filename):
        files = []
        if self.is_new_repo:
            if len(self.repo.untracked_files) and full_filename in self.repo.untracked_files:
                files.append(full_filename)
        else:
            for (path, stage), entry in self.repo.index.entries.items():
                if path == full_filename:
                    files.append(full_filename)

        return files

    def write(self, text):
        with open(self.full_filepath, "w+") as f:
            f.write(text)

        # os.chmod(self.full_filepath, 755)
        return self

    def commit(self):
        full_filename = ntpath.basename(self.full_filepath)
        files = self.__changed_files(full_filename)

        if len(files):
            self.repo.index.add(files)
            self.repo.index.commit("Changed ssh config")

        return True
