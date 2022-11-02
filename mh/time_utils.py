#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Monster Hunter time utils module.

    Monster Hunter 3 Server Project
    Copyright (C) 2021  Sepalani

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import datetime
import time


EPOCH = datetime.datetime(1970, 1, 1)
TICKS_PER_CYCLE = 23040  # 6.4 hours per cycle, 3.2 hours per daytime/nighttime

SECONDS_PER_DAY = 24*60*60
JHEN_EVENT_OFFSET = 14  # Cycle of 14 (real) days
FOG_START = 0
JHEN_START = 1  # 1 (real) day of fog
JHEN_END = 3  # Followed by 2 (real) days of sandstorm


def datetime_to_int(dt):
    return int((dt - EPOCH).total_seconds())


def current_tick():
    """
    This product of this function is based on the assumption that
    any decreasing integer value is sufficient for tracking the
    passage of time in Monster Hunter Tri.

    Debugging has shown that the internal time value (initialized
    via a request to the server which responds using this function)
    continuously decreases by one per second, and an internal modulus
    is used to turn the ever-decreasing value into a point in the
    day/night cycle (with a cycle length specified by the server).

    It is also suspected that, should this value ever reach zero, an
    integer underflow happens, which disrupts the day/night cycle.

    As a result, to ensure that the underflow never happens, the current
    implementation uses a reversed epoch time that counts down from
    UINT_MAX (the game's internal maximum for this value) as the seconds
    pass. This also has the effect of time "passing" even when the
    server is shut down.
    """
    return 0xFFFFFFFF - datetime_to_int(datetime.datetime.now())


def current_server_time():
    return datetime_to_int(datetime.datetime.now())


def get_jhen_event_times():
    """
    If the first int is less than the gametime at server login:
      If the second int is greater than the gametime at server login, fog
      Otherwise, if the third int is greater than the gametime at server login,
      sandstorm
    FIRST INT: Start of fog (epoch seconds)
    SECOND INT: Start of Jhen event (epoch seconds)
    THIRD INT: End of Jhen event (epoch seconds)
    """
    current_day = int(current_server_time()//SECONDS_PER_DAY)
    day_in_cycle = current_day % JHEN_EVENT_OFFSET
    if day_in_cycle < JHEN_END:  # Current period
        cycle_start = (current_day - day_in_cycle) * SECONDS_PER_DAY
    else:  # Upcoming period
        cycle_start = (current_day - day_in_cycle + JHEN_EVENT_OFFSET) * \
                      SECONDS_PER_DAY
    return (int(cycle_start + FOG_START*SECONDS_PER_DAY),  # fog start
            int(cycle_start + JHEN_START*SECONDS_PER_DAY),  # sandstorm start
            int(cycle_start + JHEN_END*SECONDS_PER_DAY))  # sandstorm end


class Timer(object):
    def __init__(self):
        self.__start = time.time()

    def elapsed(self):
        """Elapsed seconds since start"""
        return time.time() - self.__start

    def restart(self):
        """Reset timer and start again"""
        self.__start = time.time()
