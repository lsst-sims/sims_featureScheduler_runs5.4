# This file is part of ts_fbs_utils.
#
# Developed for the Vera C. Rubin Observatory Telescope and Site Systems.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

__all__ = ("gen_too_surveys",)

from copy import deepcopy

import numpy as np
import numpy.typing as npt
import rubin_scheduler.scheduler.basis_functions as bf
import rubin_scheduler.scheduler.detailers as detailers
from rubin_scheduler.scheduler.detailers import (
    BandPickToODetailer,
    BandSubstituteDetailer,
)
from rubin_scheduler.scheduler.surveys import ToOScriptedSurvey
from rubin_scheduler.utils import DEFAULT_NSIDE

from lsst_surveys import (
    EXPTIME,
    SCIENCE_PROGRAM,
)

ToO_Dither_detailer = detailers.DitherDetailer(per_night=False, max_dither=0.01)

def gen_too_surveys(
    nside: int = DEFAULT_NSIDE,
    detailer_list: list[detailers.BaseDetailer] | None = None,
    too_footprint: npt.NDArray | None = None,
    masks: list[bf.BaseBasisFunction] | None = None,
    science_program: str = SCIENCE_PROGRAM,
    for_simulation: bool = False,
) -> list[ToOScriptedSurvey]:
    """Generate a list of ToO surveys to follow up
    events passed in Conditions.

    Parameters
    ----------
    nside : `int`
        The HEALpix nside to use. Default to DEFAULT_NSIDE.
    detailer_list : `list` of `detailers.BaseDetailer`
        List of survey detailers.
    too_footprint : `np.ndarray` or None
        Footprint to contain ToOs within (such as the lsst footprint).
    masks : `list` of `bf.BaseBasisFunction` or None
        A list of masks to apply to the ToO surveys.
        The masks themselves are passed instead of the standard_mask_params
        so that cloud avoidance can be added.
    science_program : `str`
        Metadata to identify the science program for the visit.
    for simulation : `bool`
        Are we running a sim, then set Solar System to update mjd.

    Returns
    -------
    too_surveys : `list` [ `ToOScriptedSurvey` ]
        A list of ToO surveys configured to trigger a pre-specified sequence
        of visits in response to ToO events in the Conditions objects.
    """

    def add_ToO_Dither_detailer(dtList):
        thisDetailer = deepcopy(dtList)
        thisDetailer.append(ToO_Dither_detailer)
        return thisDetailer

    too_surveys = []

    if masks is None:
        masks = []

    ############
    # Generic GW followup
    ############

    # XXX---There's some extra stuff about do different things
    # if there's limited time before it sets. Let's see if this can
    # work first

    # XXX--instructions say do 4th night only 1/3 of the time.
    # Just leaving off for now

    # SPM--Maybe it would be good to have this, or some other
    # GW-based strategy as a backup in the event of a ToO advisory
    # Committee intervention. Would need further consultation.
    
    times = np.array([0, 24, 48], float)
    bands_at_times = ["ugrizy", "ugrizy", "ugrizy"]
    nvis = [3, 1, 1]
    exptimes = [120.0, 120.0, 120.0]
    too_surveys.append(
        ToOScriptedSurvey(
            masks,
            nside=nside,
            followup_footprint=too_footprint,
            times=times,
            bands_at_times=bands_at_times,
            nvis=nvis,
            exptimes=exptimes,
            detailers=add_ToO_Dither_detailer(detailer_list),
            too_types_to_follow=["GW_case_A"],
            survey_name="ToO, GW_A",
            flushtime=48.0,
            # Update target_name to match the alert event ID
            target_name_base="GW_A",
            observation_reason="too_gw_a",
            science_program=science_program,
        )
    )


    ############
    # GW - BNS gold
    ############
    
    event_detailers = [
        BandPickToODetailer(
            band_start="r",
            band_end="u",
            check_mounted=True,
            require_dark=True
        )
    ]

    times = np.array([0, 2, 4, 24, 48, 72], float)
    bands_at_times = ["griz", "griz", "griz", "giz", "giz", "giz"]
    nvis = [1, 1, 1, 3, 3, 3]
    exptimes = [30.0, 30.0, 30.0, 30.0, 30.0, 30.0]
    too_surveys.append(
        ToOScriptedSurvey(
            masks,
            nside=nside,
            followup_footprint=too_footprint,
            times=times,
            bands_at_times=bands_at_times,
            nvis=nvis,
            exptimes=exptimes,
            detailers=add_ToO_Dither_detailer(detailer_list),
            too_types_to_follow=["GW_BNS_Gold,GW_SSM_Gold"],
            survey_name="ToO, GW, BNS, Gold",
            # Update target_name to match the alert event ID
            target_name_base="GW_BNS_Gold",
            observation_reason="too_gw_bns_gold",
            science_program=science_program,
            flushtime=48,
            event_gen_detailers=event_detailers
        )
    )


    ############
    # GW - BNS silver 
    ############ 

    times = np.array([0, 2, 24, 48, 72], float)
    bands_at_times = ["gi", "gi", "gi", "gi", "gi"]
    nvis = [1, 1, 3, 3, 3]
    exptimes = [30.0, 30.0, 30.0, 30.0, 30.0]
    too_surveys.append(
        ToOScriptedSurvey(
            masks,
            nside=nside,
            followup_footprint=too_footprint,
            times=times,
            bands_at_times=bands_at_times,
            nvis=nvis,
            exptimes=exptimes,
            detailers=add_ToO_Dither_detailer(detailer_list),
            too_types_to_follow=["GW_BNS_Silver,GW_SSM_Silver"],
            survey_name="ToO, GW, BNS, Silver",
            # Update target_name to match the alert event ID
            target_name_base="GW_BNS_Silver",
            observation_reason="too_gw_bns_silver",
            science_program=science_program,
            flushtime=48,
        )
    )


    ############
    # GW - BNS bronze 
    ############ 

    times = np.array([0, 24, 48, 72], float)
    bands_at_times = ["gi", "gi", "gi", "gi"]
    nvis = [1, 1, 1, 1]
    exptimes = [30.0, 30.0, 30.0, 30.0]
    too_surveys.append(
        ToOScriptedSurvey(
            masks,
            nside=nside,
            followup_footprint=too_footprint,
            times=times,
            bands_at_times=bands_at_times,
            nvis=nvis,
            exptimes=exptimes,
            detailers=add_ToO_Dither_detailer(detailer_list),
            too_types_to_follow=["GW_BNS_Bronze"],
            survey_name="ToO, GW, BNS, Bronze",
            # Update target_name to match the alert event ID
            target_name_base="GW_BNS_Bronze",
            observation_reason="too_gw_bns_bronze",
            science_program=science_program,
            flushtime=48,
        )
    )



    ############
    # GW - NSBH gold
    ############ 

    times = np.array([0, 2, 4, 24, 48, 72, 168], float)
    bands_at_times = ["griz", "griz", "griz", "giz", "giz", "giz", "giz]
    nvis = [1, 1, 1, 3, 3, 3, 3]
    exptimes = [30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0]
    too_surveys.append(
        ToOScriptedSurvey(
            masks,
            nside=nside,
            followup_footprint=too_footprint,
            times=times,
            bands_at_times=bands_at_times,
            nvis=nvis,
            exptimes=exptimes,
            detailers=add_ToO_Dither_detailer(detailer_list),
            too_types_to_follow=["GW_NSBH_Gold"],
            survey_name="ToO, GW, NSBH, Gold",
            # Update target_name to match the alert event ID
            target_name_base="GW_NSBH_Gold",
            observation_reason="too_gw_nsbh_gold",
            science_program=science_program,
            flushtime=48,
        )
    )


    ############
    # GW - NSBH silver 
    ############ 

    times = np.array([0, 2, 24, 48, 72, 168], float)
    bands_at_times = ["gz", "gz", "gz", "gz", "gz", "gz"]
    nvis = [1, 1, 3, 3, 3]
    exptimes = [30.0, 30.0, 30.0, 30.0, 30.0, 30.0]
    too_surveys.append(
        ToOScriptedSurvey(
            masks,
            nside=nside,
            followup_footprint=too_footprint,
            times=times,
            bands_at_times=bands_at_times,
            nvis=nvis,
            exptimes=exptimes,
            detailers=add_ToO_Dither_detailer(detailer_list),
            too_types_to_follow=["GW_NSBH_Silver"],
            survey_name="ToO, GW, NSBH, Silver",
            # Update target_name to match the alert event ID
            target_name_base="GW_NSBH_Silver",
            observation_reason="too_gw_nsbh_silver",
            science_program=science_program,
            flushtime=48,
        )
    )


    ############
    # GW - NSBH bronze 
    ############ 

    times = np.array([0, 24, 48, 72], float)
    bands_at_times = ["gz", "gz", "gz", "gz"]
    nvis = [1, 1, 1, 1]
    exptimes = [30.0, 30.0, 30.0, 30.0]
    too_surveys.append(
        ToOScriptedSurvey(
            masks,
            nside=nside,
            followup_footprint=too_footprint,
            times=times,
            bands_at_times=bands_at_times,
            nvis=nvis,
            exptimes=exptimes,
            detailers=add_ToO_Dither_detailer(detailer_list),
            too_types_to_follow=["GW_NSBH_Bronze"],
            survey_name="ToO, GW, NSBH, Bronze",
            # Update target_name to match the alert event ID
            target_name_base="GW_NSBH_Bronze",
            observation_reason="too_gw_nsbh_bronze",
            science_program=science_program,
            flushtime=48,
        )
    )

    ############
    # BBH hole-black hole GW merger
    ############

    # XXX--only considering bright objects now.

    # SM-- adding support for different BBH cases. We should have
    # a discussion about how to differentiate these, and if it is
    # possible to do so through the alert stream.

    event_detailers = [
        BandPickToODetailer(
            band_start="z",
            band_end="g",
            check_mounted=True,
            require_dark=True
        )
    ]

    times = np.array([0, 3, 8, 10, 40], float) * 24
    bands_at_times = ["riz"] * times.size
    nvis = [1] * times.size
    exptimes = [EXPTIME] * times.size 

    too_surveys.append(
        ToOScriptedSurvey(
            masks,
            nside=nside,
            followup_footprint=too_footprint,
            times=times,
            bands_at_times=bands_at_times,
            nvis=nvis,
            exptimes=exptimes,
            detailers=add_ToO_Dither_detailer(detailer_list),
            too_types_to_follow=["BBH"],
            survey_name="ToO, BBH",
            # Update target_name to match the alert event ID
            target_name_base="BBH",
            observation_reason="too_bbh",
            science_program=science_program,
            flushtime=48,
            event_gen_detailers=event_detailers,
        )
    )

    ############
    # Lensed BNS
    ############

    # SM --- I'm dropping this, since the observing
    # strategy and implementation is still under discussion

    # times = np.array([1.0, 1.0, 25, 25, 49, 49], float)
    # bands_at_times = ["g", "r"] * 3
    # nvis = [1, 3] * 3
    # exptimes = [EXPTIME, EXPTIME] * 3

    # too_surveys.append(
    #     ToOScriptedSurvey(
    #         masks,
    #         nside=nside,
    #         followup_footprint=too_footprint,
    #         times=times,
    #         bands_at_times=bands_at_times,
    #         nvis=nvis,
    #         exptimes=exptimes,
    #         detailers=deepcopy(detailer_list),
    #         too_types_to_follow=["lensed_BNS_case_A"],
    #         survey_name="ToO, LensedBNS_A",
    #         # Update target_name to match the alert event ID
    #         target_name_base="LensedBNS_A",
    #         observation_reason="too_lensed_bns_a",
    #         science_program=science_program,
    #         flushtime=48.0,
    #     )
    # )

    # # This is the small skymap (15 deg^2 case)
    # times = np.array([1.0, 1.0, 25, 25, 49, 49], float)
    # bands_at_times = ["g", "r"] * 3
    # nvis = [180, 120] * 3
    # exptimes = [30] * times.size

    # too_surveys.append(
    #     ToOScriptedSurvey(
    #         masks,
    #         nside=nside,
    #         followup_footprint=too_footprint,
    #         times=times,
    #         bands_at_times=bands_at_times,
    #         nvis=nvis,
    #         exptimes=exptimes,
    #         detailers=deepcopy(detailer_list),
    #         too_types_to_follow=["lensed_BNS_case_B"],
    #         survey_name="ToO, LensedBNS_B",
    #         # Update target_name to match the alert event ID
    #         target_name_base="LensedBNS_B",
    #         observation_reason="too_lensed_bns_b",
    #         science_program=science_program,
    #         flushtime=48.0,
    #     )
    # )


    ############
    # IceCube followup - Standard
    ############

    times = np.array([0.0, 0.0, 15.0 / 60.0, 0.0, 24.0, 24.0, 48.0, 72.0, 96.0, 120.0, 144.0, 168.0, 168.0, 192.0, 216.0], float)
    bands_at_times = ["u", "g", "r", "z", "g", "r", "g", "g", "gr", "g", "g", "g", "rz", "g", "g"]
    exptimes = [
        30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30
    ]
    nvis = [1, 4, 1, 1, 4, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1]

    too_surveys.append(
        ToOScriptedSurvey(
            masks,
            nside=nside,
            followup_footprint=too_footprint,
            times=times,
            bands_at_times=bands_at_times,
            nvis=nvis,
            exptimes=exptimes,
            detailers=add_ToO_Dither_detailer(detailer_list),
            too_types_to_follow=["neutrino_standard"],
            survey_name="ToO, neutrino, standard",
            # Update target_name to match the alert event ID
            target_name_base="neutrino_standard",
            observation_reason="too_neutrino_standard",
            science_program=science_program,
            flushtime=20 * 24,
        )
    )


    ############
    # IceCube followup - Extremely-high energy 
    ############

    times = np.array([0.0, 15.0 / 60.0, 24.0, 48.0, 72.0, 96.0, 120.0, 144.0, 168.0, 192.0, 216.0], float)
    bands_at_times = ["ugz", "r", "grz", "grz", "grz", "grz", "grz", "grz", "grz", "grz", "grz"]
    exptimes = [
        30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30 
        ]
    nvis = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

    too_surveys.append(
        ToOScriptedSurvey(
            masks,
            nside=nside,
            followup_footprint=too_footprint,
            times=times,
            bands_at_times=bands_at_times,
            nvis=nvis,
            exptimes=exptimes,
            detailers=add_ToO_Dither_detailer(detailer_list),
            too_types_to_follow=["neutrino_extreme"],
            survey_name="ToO, neutrino, extreme",
            # Update target_name to match the alert event ID
            target_name_base="neutrino_extreme",
            observation_reason="too_neutrino_extreme",
            science_program=science_program,
            flushtime=20 * 24,
        )
    )

    ############
    # IceCube followup - coincident alert 
    ############

    times = np.array([0, 15/60, 2, 24], float)
    bands_at_times = ["rz","g","r","rgz"]
    exptimes = [
         30, 30, 30, 30
        ]
    nvis = [4, 4, 4, 4]

    too_surveys.append(
        ToOScriptedSurvey(
            masks,
            nside=nside,
            followup_footprint=too_footprint,
            times=times,
            bands_at_times=bands_at_times,
            nvis=nvis,
            exptimes=exptimes,
            detailers=add_ToO_Dither_detailer(detailer_list),
            too_types_to_follow=["neutrino_coinc"],
            survey_name="ToO, neutrino, coincident",
            # Update target_name to match the alert event ID
            target_name_base="neutrino_coincident",
            observation_reason="too_neutrino_coincident",
            science_program=science_program,
            flushtime=20 * 24,
        )
    )

    ############
    # Solar System
    ############
    # For the solar system objects, probably want a custom survey object,
    # but this should work for now. Want to add a detailer to add a dither
    # position.

    times = np.array([0, 33 / 60.0, 66 / 60.0], float)
    bands_at_times = ["r"] * 3
    nvis = [2] * 3
    exptimes = [EXPTIME] * 3

    too_surveys.append(
        ToOScriptedSurvey(
            masks,
            nside=nside,
            followup_footprint=too_footprint,
            times=times,
            bands_at_times=bands_at_times,
            nvis=nvis,
            exptimes=exptimes,
            detailers=add_ToO_Dither_detailer(detailer_list),
            too_types_to_follow=["SSO_night"],
            survey_name="ToO, SSO_night",
            # Update target_name to match the alert event ID
            target_name_base="SSO_night",
            observation_reason="too_sso_general",
            science_program=science_program,
            flushtime=3.0,
            update_mjd0=for_simulation,
        )
    )

    times = np.array([0, 33 / 60.0, 66 / 60.0])
    bands_at_times = ["z"] * 3
    nvis = [2] * 3
    exptimes = [15.0] * 3

    if detailer_list is not None:
        more_detailers = deepcopy(detailer_list)
    else:
        more_detailers = []

    more_detailers.append(
        BandSubstituteDetailer(band_original="z", band_replacement="i")
    )

    too_surveys.append(
        ToOScriptedSurvey(
            masks,
            nside=nside,
            followup_footprint=too_footprint,
            times=times,
            bands_at_times=bands_at_times,
            nvis=nvis,
            exptimes=exptimes,
            detailers=add_ToO_Dither_detailer(more_detailers),
            too_types_to_follow=["SSO_twilight"],
            survey_name="ToO, SSO_twi",
            # Update target_name to match the alert event ID
            target_name_base="SSO_twi",
            observation_reason="too_sso_twi",
            science_program=science_program,
            flushtime=3.0,
        )
    )

    ############
    # Galactic Supernova
    ############
    # For galactic supernovae, we want to tile continuously
    # in the region in 1s and 15s exposures for i band, until
    # a counterpart is identified

    times = np.array([0, 0, 0, 0] * 4, float)
    bands_at_times = ["i", "i", "i", "i"] * 4
    nvis = [1, 1, 1, 1] * 4
    exptimes = [1, 15, 1, 15] * 4

    too_surveys.append(
        ToOScriptedSurvey(
            masks,
            nside=nside,
            followup_footprint=too_footprint,
            times=times,
            bands_at_times=bands_at_times,
            nvis=nvis,
            exptimes=exptimes,
            detailers=add_ToO_Dither_detailer(more_detailers),
            too_types_to_follow=["SN_Galactic"],
            survey_name="ToO, galactic SN",
            # Update target_name to match the alert event ID
            target_name_base="SN_Galactic",
            observation_reason="too_sn_galactic",
            science_program=science_program,
            flushtime=48.0,
        )
    )

    return too_surveys
