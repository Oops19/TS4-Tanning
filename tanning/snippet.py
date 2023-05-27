#
# License: https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#


import ast
from typing import Dict, List, Union

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
    tuning_data: Dict[Union[str,int],Dict[Union[str,int],List[Union[int,str]]]] = dict()  # {bodytype: {cas_part: [pas_part_1, cas_part_2, ...], cp: [cp1, cp2, ...], ...}, bodytype_2: ..., ...}

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
            version: int = cls.version
            data: str = cls.data
            log.debug(f"version='{version}: {type(version)}'; data='{data.strip()}: {type(data)}'")
            data: dict = ast.literal_eval(data.strip())
            log.debug(f"version='{version}: {type(version)}'; ast.data='{data}: {type(data)}'")
            for body_type, cas_part_instances in data.items():
                current_cas_part_instances = TanningFix.tuning_data.get(body_type, dict())
                current_cas_part_instances.update(cas_part_instances)
                TanningFix.tuning_data.update({body_type: current_cas_part_instances})
            log.debug(f"TanningFix.tuning_data = '{TanningFix.tuning_data}'")
        except Exception as e:
            log.error(f"Oops '{e}'", exception=e)
