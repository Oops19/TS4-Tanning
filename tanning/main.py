#
# License: https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#


from typing import Dict, List, Union, Set

from sims.suntan.suntan_tracker import SuntanTracker
from sims4.common import Pack

from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.common_log_registry import CommonLogRegistry, CommonLog
from sims4communitylib.utils.resources.common_game_pack_utils import CommonGamePackUtils
from tanning.modinfo import ModInfo


log: CommonLog = CommonLogRegistry.get().register_log(f"{ModInfo.get_identity().name}", ModInfo.get_identity().name)
log.enable()


class TanningFix:
    pass


class Tanning:
    replace_dict: Dict[Union[str,int],Dict[Union[str,int],List[Union[int,str]]]] = dict()  # {bodytype: {cas_part: [pas_part_1, cas_part_2, ...], cp: [cp1, cp2, ...], ...}, bodytype_2: ..., ...}
    initialized = False
    quick_lookup: Dict[int, List] = dict()  # {bodytype: [cas_part_1, cas_part_2, cp1, cp2, ...]}

    def __init__(self):
        if Tanning.initialized:
            return

        if not CommonGamePackUtils.has_game_pack_available(Pack.EP07):
            Tanning.initialized = True
            log.debug("EP07 is currently unavailable.")
            return

        Tanning.replace_dict = self._parse_tuning_data(TanningFix.tuning_data)
        log.debug(f"Tanning.replace_dict: {Tanning.replace_dict}")

        # parse the configuration
        for body_type, cas_part_instances in Tanning.replace_dict.items():
            for cas_part_target, cas_part_sources in cas_part_instances.items():
                instances = Tanning.quick_lookup.get(body_type, [])
                instances += cas_part_sources
                Tanning.quick_lookup.update({body_type: instances})

        log.debug(f"Tanning.quick_lookup {Tanning.quick_lookup}")

        @CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), SuntanTracker, SuntanTracker.set_tan_level.__name__)
        def set_tan_level(original, self, *args, **kwargs):
            # def set_tan_level(self, tan_level=None, force_update=False):
            log.debug(f"SuntanTracker.set_tan_level(self={self}: {type(self)}, {args}, {kwargs})")
            rv = original(self, *args, **kwargs)
            if self._outfit_part_data_list:
                replace_parts = dict()

                # Gather all matching parts
                for _outfit_part_data_list in self._outfit_part_data_list:
                    body_type = _outfit_part_data_list[1]
                    if body_type in Tanning.quick_lookup.keys():
                        log.debug(f"1) body_type: {body_type}")
                        instance_ids = Tanning.quick_lookup.get(body_type, [])
                        cas_part_instance = _outfit_part_data_list[0]
                        if cas_part_instance in instance_ids:
                            log.debug(f"2) cas_part_instance: {cas_part_instance}")
                            cas_part_instances = Tanning.replace_dict.get(body_type)
                            for new_cas_part_instance_id, replace_cas_part_instance_ids in cas_part_instances.items():
                                if cas_part_instance in replace_cas_part_instance_ids:
                                    log.debug(f"3) cas_part_instance: {cas_part_instance} - {new_cas_part_instance_id} - {replace_cas_part_instance_ids}")
                                    if new_cas_part_instance_id != 0:
                                        replace_parts.update({_outfit_part_data_list: (new_cas_part_instance_id, body_type)})
                                    else:
                                        replace_parts.update({_outfit_part_data_list: None})

                # Replace all matching parts
                log.debug(f"replace_parts: {replace_parts}")
                if replace_parts:
                    for remove_part, new_part in replace_parts.items():
                        pos = self._outfit_part_data_list.index(remove_part)
                        if new_part:
                            self._outfit_part_data_list = self._outfit_part_data_list[:pos] + self._outfit_part_data_list[pos + 1:] + (new_part, )
                        else:
                            self._outfit_part_data_list = self._outfit_part_data_list[:pos] + self._outfit_part_data_list[pos + 1:]
                    self._suntan_force_updated = True
                    self._force_update = True
                    self._sim_info.resend_suntan_data()

        Tanning.initialized = True
        log.debug("Tanning.initialized = True")

    def _parse_tuning_data(self, tuning_data: Dict[Union[str,int],Dict[Union[str,int],List[Union[int,str]]]]) -> Dict[int,Dict[int,Set[int]]]:

        try:
            from guids.api.common_packages import CommonPackages
            cp = CommonPackages()
            _rv = cp.search(name="yfBody_*", limit=5)
            if len(_rv) < 3:
                log.warn("CommonPackages().search() failed. Can't convert names to instance IDs. Re-initialize or install GUIDs.")
        except:
            log.warn("Importing CommonPackages() from GUIDs failed. Can't convert names to instance IDs. Update or install GUIDs.")
            cp = None

        def _get_body_type(_body_type: Union[str,int]) -> BodyType:
            """ Return the BodyType or BodyType.NONE """
            _rv = BodyType.NONE
            try:
                if isinstance(_body_type, int):
                    _rv = BodyType(_body_type)
                elif isinstance(_body_type, str) and _body_type.startswith('BodyType.'):
                    _rv = BodyType[_body_type.split('.', 1)[1]]
            except:
                log.warn(f"Could not parse BodyType '{_body_type}'")

            log.debug(f"_get_body_type({_body_type}) -> '{_rv}'")
            return _rv

        def _get_int_cas_part_ids(_cas_part: str) -> Set[int]:
            _rv = {0}
            try:
                if isinstance(_cas_part, int):
                    _rv = {_cas_part}
                elif cp and isinstance(_cas_part, str):
                    _rv = set(cp.search(name=_cas_part, limit=20))
            except:
                log.warn(f"Could not parse CAS Part '{_cas_part}'")

            log.debug(f"_get_int_cas_part_ids({_cas_part}) -> '{_rv}'")
            return _rv

        rv: Dict[int,Dict[int,Set[int]]] = dict()
        for body_type, cas_part_instances in tuning_data.items():
            int_bodytype: int = _get_body_type(body_type).value
            if not int_bodytype:
                log.warn(f"Could not parse: '{body_type}: {cas_part_instances}")
                continue
            current_cas_part_instances = rv.get(int_bodytype, dict())
            for cas_part_target, cas_part_sources in cas_part_instances.items():
                int_cas_part_target: int = _get_int_cas_part_ids(cas_part_target).pop()  # There's only one ID
                int_cas_part_sources: Set = set()
                for cas_part_source in cas_part_sources:
                    int_cas_part_sources.update(_get_int_cas_part_ids(cas_part_source))
                current_cas_part_instances.update({int_cas_part_target: int_cas_part_sources})
            rv.update({int_bodytype: current_cas_part_instances})
        return rv


@CommonEventRegistry.handle_events(ModInfo.get_identity().name)
def handle_event(event_data: S4CLZoneLateLoadEvent):
    log.debug("Tanning ...")
    Tanning()
