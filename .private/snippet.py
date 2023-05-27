import services

from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import HasTunableReference, Tunable
from sims4communitylib.utils.common_log_registry import CommonLog, CommonLogRegistry
from tanning.modinfo import ModInfo

log: CommonLog = CommonLogRegistry.get().register_log(f"{ModInfo.get_identity().name}", ModInfo.get_identity().name)
log.enable()


class TanningFix(
    # <I c="TanningTool" i="snippet" m="tanning.snippet" n="author_whatever" s="fnv64(author_whatever)"> <!-- 0x fnv64(author_whatever) -->
    HasTunableReference,
    metaclass=HashedTunedInstanceMetaclass,
    manager=services.get_instance_manager(Types.SNIPPET)
):
    INSTANCE_TUNABLES = {
        # <T n="version">1</T>
        'version': Tunable(
            description='Tanning Snippet version.',
            tunable_type=int,
            default=1
        ),

        # <T n="data">{...}</T>
        'data': Tunable(
            description='The Python dict data',
            tunable_type=str,
            default=""
        ),
    }

    @classmethod
    def _tuning_loaded_callback(cls):
        log.info(f'Processing {cls}')
        try:
            version = cls.version
            data = cls.data
            log.debug(f"version='{version}'; data='{data}'")
        except:
            pass



