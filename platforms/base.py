# platforms/base.py
from abc import ABC, abstractmethod
from utils.cmd import run_cmd

class BasePlatform(ABC):
    def __init__(self, title, version, tv=None, debug=False, app=None, profile=None, release=False): #build_only=False,
        self.title = title
        self.version = version
        self.tv = tv
        self.debug = debug
        self.app = app
        self.profile = profile
        self.release = release

    @abstractmethod
    def deploy(self):
        pass

    @abstractmethod
    def package(self):
        pass

    def get_app_folder(self):
        return f"build.{self.platform}/{'' if not self.app else self.app[1:]}"
