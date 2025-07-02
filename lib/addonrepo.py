# standard imports
import os

# third-party imports
import git

class AddonRepo:
    def __init__(self, url, branch, tgt_root):
        tgt_name = url.split("/")[-1]
        tgt_path = os.path.join(tgt_root, tgt_name)
        try:
            self.repo = git.Repo.clone_from(
                url=url, to_path=tgt_path,
                branch=branch, single_branch=True, depth=1
            )
        except git.exc.GitCommandError:
            self.repo = git.Repo(tgt_path)

        assert not self.repo.is_dirty()
        self.repo.remote().pull()

    def hash(self, length=12):
        return self.repo.rev_parse("HEAD").hexsha[:length]

    def url(self):
        return self.repo.remote().url

    def path(self):
        return self.repo.working_dir

    def branch(self):
        return self.repo.active_branch
