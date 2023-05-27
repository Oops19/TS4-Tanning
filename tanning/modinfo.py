from sims4communitylib.mod_support.common_mod_info import CommonModInfo


class ModInfo(CommonModInfo):
    _FILE_PATH: str = str(__file__)

    @property
    def _name(self) -> str:
        return 'IL_Tanning'

    @property
    def _author(self) -> str:
        return 'o19'

    @property
    def _base_namespace(self) -> str:
        return 'tanning'

    @property
    def _file_path(self) -> str:
        return ModInfo._FILE_PATH

    @property
    def _version(self) -> str:
        return '0.0.8'


'''
v0.0.8
    Import fixes
    Using Ts4Lib for CommonEnum
v0.0.7
    Update README and compile.sh
v0.0.6
    Update README and compile.sh
v0.0.5
    Fixed logging of BodyType
v0.0.4
    Bugfix merging multiple snippet
v0.0.3
    Integrated GUIDs support
v0.0.2
    Support for simple XML Tuning Snippets
v0.0.1
    Initial version
'''
