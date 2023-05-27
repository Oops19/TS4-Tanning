#
# License: https://creativecommons.org/licenses/by/4.0/ https://creativecommons.org/licenses/by/4.0/legalcode
# © 2022 https://github.com/Oops19
#


from sims.suntan.suntan_tuning import TanLevel

from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput

from sims4communitylib.utils.common_log_registry import CommonLogRegistry, CommonLog

from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from tanning.modinfo import ModInfo


log: CommonLog = CommonLogRegistry.get().register_log(f"{ModInfo.get_identity().name}", ModInfo.get_identity().name)
log.enable()


@CommonConsoleCommand(
    ModInfo.get_identity(),
    'o19.tanning.tan',
    "Usage: o19.tanning.tan"
)
def o19_cmd_tan(output: CommonConsoleCommandOutput):
    try:
        sim = CommonSimUtils.get_active_sim()
        # FINGERNAIL = 73 s = "16482018810904373590" > <!-- E4BBE4C87542E956 -->  (16482018810904373590, 73)
        _outfit_part_data_list = ((9223372037046442173, 2), (6977, 3), (148023, 4), (13025992306196967712, 8), (9223372036901407277, 33), (51050, 34), (10967, 35), (11877906383619433840, 36), (13551179027179487951, 43), (16581998070815190585, 56), (16178797531151470151, 57), (15215745643906387534, 64), (11136293878617509287, 69), (300325, 78), (300455, 79), (300564, 80), (320016, 81), (15933, 5), (16482018810904373590, 73))
        suntan_tracker = sim.sim_info.suntan_tracker
        if suntan_tracker:
            suntan_tracker._tan_level = TanLevel.DEEP  # NO_TAN, DEEP or SUNBURNED
            suntan_tracker._outfit_part_data_list = _outfit_part_data_list
            suntan_tracker._suntan_force_updated = True
            suntan_tracker._force_update = True
            sim.sim_info.resend_suntan_data()
        output("ok")
    except Exception as e:
        output(f"Oops: '{e}")
        log.error(f"Oops: '{e}", exception=e)