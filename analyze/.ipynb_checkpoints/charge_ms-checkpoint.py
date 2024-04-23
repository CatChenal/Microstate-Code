import numpy as np
import operator
from typing import Union
import zlib



class Charge_Microstate:
    """
    For usage symmetry with Microstate class, Charge_Microstate.E = Charge_Microstate.average_E,
    So querying for the energy can be done using Charge_Microstate.E, bearing in mind that
    the energy is an average for a charge microstate.
    Sortable class.
    The Charge_Microstate.crg_stateid is implemented as compressed bytes as in the ms_analysis.py
    Microstate class in Junjun Mao's demo.
    """

    def __init__(self, crg_state:list, total_E:float, count:int):
        self.crg_stateid = zlib.compress(" ".join([str(x) for x in crg_state]).encode())
        self.average_E = self.E = 0  # .E -> average E
        self.total_E = total_E
        self.count = count

    def state(self):
        return [int(i) for i in zlib.decompress(self.crg_stateid).decode().split()]

    def __str__(self):
        return f"Charge_Microstate(\n\tcount = {self.count:,},\n\tE = {self.E:,.2f},\n\tstate = {self.state()}\n)"

    def _check_operand(self, other):
        """Fails on missing attribute."""

        if not (
            hasattr(other, "crg_stateid")
            and hasattr(other, "E")
            and hasattr(other, "count")
        ):
            return NotImplemented("Comparison with non Charge_Microstate object.")
        return

    def __eq__(self, other):
        self._check_operand(other)
        return (self.crg_stateid, self.E, self.count) == (
            other.crg_stateid,
            other.E,
            other.count,
        )

    def __lt__(self, other):
        self._check_operand(other)
        return (self.crg_stateid, self.E, self.count) < (
            other.crg_stateid,
            other.E,
            other.count,
        )


def ms_to_charge_ms(microstates:Union[dict, list], conformers:list) -> list:
    """
    Refactored from jmao's MC class method: convert_to_charge_ms
    """

    if isinstance(microstates, dict):
        microstates = list(microstates.values())

    charge_microstates = []

    # populate dict charge_ms_by_id:
    charge_ms_by_id = {}

    for ms in microstates:
        current_crg_state = [round(conformers[ic].crg) for ic in ms.state]
        crg_ms = Charge_Microstate(current_crg_state, ms.E * ms.count, ms.count)
        crg_id = crg_ms.crg_stateid  # compressed bytes
        if crg_id in charge_ms_by_id.keys():
            charge_ms_by_id[crg_id].count += crg_ms.count
            charge_ms_by_id[crg_id].total_E += crg_ms.total_E
        else:
            charge_ms_by_id[crg_id] = crg_ms

    for k in charge_ms_by_id.keys():
        crg_ms = charge_ms_by_id[k]
        crg_ms.average_E = crg_ms.E = crg_ms.total_E / crg_ms.count
        charge_microstates.append(crg_ms)

    return charge_microstates


def sort_charge_microstates(charge_microstates:list,
                            sort_by:str = "count",
                            sort_reverse:bool = True) -> Union[list, None]:
    """Return the list of charge_microstates sorted by one of these attributes: ["count", "E", "total_E"],
    and in reverse order (descending) if sort_reverse is True.
    Args:
    charge_microstates (list): list of Charge_Microstate instances;
    sort_by (str, "count"): Attribute as sort key;
    sort_reverse (bool, True): Sort order: descending if True (default), else ascending.
    Return None if 'sort_by' is not recognized.
    """

    if sort_by not in ["count", "E", "total_E"]:
        print("'sort_by' must be a valid charge_microstate attribute; choices: ['count', 'E', 'total_E']")
        return None

    return sorted(charge_microstates,
                  key=operator.attrgetter(sort_by),
                  reverse=sort_reverse)


def topN_charge_microstates(charge_microstates:list,
                            N:int = 1,
                            sort_by:str = "count",
                            sort_reverse:bool = True) -> Union[list, None]:
    """Return the top N entries from the list of charge_microstates sorted by one of these attributes:
       ["count", "E", "total_E"], and in reverse order (descending) if sort_reverse is True.
       Note: The 'topN' in this context means the most frequent if sort_by is 'count', or the most
       favorable (lowest) energy otherwise. Thus, the expected sort args are ('count', sort_reverse=
       True), or (["E" | "total_E"], sort_reverse=False). A warning is displayed for any other combination
       and None is returned.
       Args:
       charge_microstates (list): list of Charge_Microstate instances;
       N (int, 1): Number of entries to return;
       sort_by (str, "count"): Attribute as sort key;
       sort_reverse (bool, True): Sort order: descending if True (default), else ascending.
       Return:
       A list of N Charge_Microstate instances.
    """

    # validate sort args:
    if sort_by == "count" and not sort_reverse:
        print("WARNING: Returning the most frequent charge microstates by count calls for sorting descendingly: sort_reverse must be True.")
        return None
    elif sort_by.endswith("E") and sort_reverse:
        print("WARNING: Returning the most favorable charge microstates by energy calls for sorting ascendingly: sort_reverse must be False.")
        return None

    sorted_charge_ms = sort_charge_microstates(charge_microstates, sort_by, sort_reverse)

    return sorted_charge_ms[:N]
