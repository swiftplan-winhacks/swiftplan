from dataclasses import dataclass
import datetime
from typing import List, NamedTuple, Tuple
import json
from copy import deepcopy
from event import Event, Location, Timeframe

from mapsy import timeDistance


@dataclass
class Task:
    id: int
    begin: datetime.datetime
    end: datetime.datetime
    dur: datetime.timedelta
    @property
    def loc_id(self):
        return self.id


class Interval(NamedTuple):
    begin: datetime.datetime
    end: datetime.datetime
    loc_id_b: Tuple
    loc_id_e: Tuple


class Planner:
    def __init__(self, events: List[Event], home_location: Location):
        self.events = events
        self.home_location = home_location
        self.rigid_tasks, self.flexible_tasks, s_date, e_date = self.parse()
        home_loc_id = -1

        if datetime.datetime.now().date() != s_date.date():
            days = [s_date + datetime.timedelta(days=i)
                    for i in range((e_date - s_date).days + 1)]
            self.freetime = [
                Interval(d + datetime.timedelta(hours=7),
                         d + datetime.timedelta(hours=23),
                         home_loc_id,
                         home_loc_id) for d in days
            ]

        else:
            today_int = Interval(
                datetime.datetime.now() + datetime.timedelta(minutes=1),
                datetime.datetime.now().replace(hour=23, minute=0),
                home_loc_id,
                home_loc_id
            )

            days = [s_date + datetime.timedelta(days=i)
                    for i in range(1, (e_date - s_date).days + 1)]

            self.freetime = [today_int] + [
                Interval(d + datetime.timedelta(hours=7),
                         d + datetime.timedelta(hours=23),
                         home_loc_id,
                         home_loc_id) for d in days
            ]

        self.placed_tasks = dict()
        self.solution_found = False
        self.distances = dict()

    def __repr__(self):
        return str(self.placed_tasks)

    def parse(self):
        dt_fmt = "%d.%m.%Y %H:%M"
        rigid_tasks = []
        flexible_tasks = []

        for i, e in enumerate(self.events):
            b_st = e.timeframe.start_date + " " + e.timeframe.start_time
            b_t = datetime.datetime.strptime(b_st, dt_fmt)

            e_st = e.timeframe.end_date + " " + e.timeframe.end_time
            e_t = datetime.datetime.strptime(e_st, dt_fmt)

            if e.timeframe.duration is not None:
                h, m = [int(e) for e in e.timeframe.duration.split(":")]
                duration = datetime.timedelta(hours=h, minutes=m)
            else:
                duration = e_t - b_t
            task = Task(i, b_t, e_t, duration)
            if e.isFixed():
                rigid_tasks.append(task)
            else:
                flexible_tasks.append(task)

        s_time = min(rigid_tasks+flexible_tasks,
                     key=lambda t: t.begin).begin.replace(hour=0, minute=0)
        e_time = max(rigid_tasks+flexible_tasks,
                     key=lambda t: t.end).end.replace(hour=0, minute=0)

        return rigid_tasks, flexible_tasks, s_time, e_time

    def dist(self, loc_id1, loc_id2, time):
        if loc_id1 == -1:  # home destination
            l1 = self.home_location
        else:
            l1 = self.events[loc_id1].location

        if loc_id2 == -1:
            l2 = self.home_location
        else:
            l2 = self.events[loc_id2].location

        if (l1.latlngtup(), l2.latlngtup(), time) in self.distances:
            return self.distances[(l1.latlngtup(), l2.latlngtup(), time)]
        else:

            #dist = datetime.timedelta(0)
            dist = timeDistance(l1, l2, time)

            self.distances[(l1.latlngtup(), l2.latlngtup(), time)] = dist
            return dist

    def place(self, t: Task, invls):
        for ivl in invls:
            s_time = max(ivl.begin, t.begin)
            e_time = min(ivl.end,   t.end)
            aval_time = e_time - s_time
            if aval_time > datetime.timedelta(0):
                tot_dur = self.dist(ivl.loc_id_b, t.loc_id, s_time) + \
                    t.dur + \
                    self.dist(t.loc_id, ivl.loc_id_e, s_time + t.dur)
                if tot_dur <= aval_time:
                    # print("Posssible", t, ivl)
                    break
        else:
            # print("Cannot allocate task")
            return False
        if ivl.begin != s_time:
            invls.append(
                Interval(ivl.begin,
                         s_time + self.dist(ivl.loc_id_b, t.loc_id, s_time),
                         ivl.loc_id_b,
                         t.loc_id)
            )

        if s_time + tot_dur < ivl.end:
            invls.append(
                Interval(s_time + self.dist(ivl.loc_id_b, t.loc_id, s_time) + t.dur,
                         ivl.end,
                         t.loc_id,
                         ivl.loc_id_e)
            )
        invls.remove(ivl)
        invls.sort()

        self.placed_tasks[t.id] = (
            s_time + self.dist(ivl.loc_id_b, t.loc_id, s_time),
            s_time + self.dist(ivl.loc_id_b, t.loc_id, s_time) + t.dur
        )

        return True

    def allocate(self, task_l, invls):
        if self.solution_found:
            return

        if len(task_l) == 0:
            self.solution_found = True
            return

        for t in task_l:
            cinvls = deepcopy(invls)
            allocated = self.place(t, cinvls)

            if not allocated:
                return

            t_tmp = deepcopy(task_l)
            t_tmp.remove(t)
            self.allocate(t_tmp, cinvls)
            if self.solution_found:
                return

    def plan(self):
        invls = self.freetime
        for t in self.rigid_tasks:
            self.place(t, invls)

        self.flexible_tasks.sort(key=lambda task: -task.dur)

        self.allocate(self.flexible_tasks, invls)

        if not self.solution_found:
            n_missing = len(self.placed_tasks) - \
                len(set(self.placed_tasks.values()))
            print(
                f"No solution found, {n_missing} tasks remains without place")

        for i, t in self.placed_tasks.items():  # task_time_start, task_time_end, task
            st = t[0].timetuple()
            et = t[1].timetuple()
            diff = t[1] - t[0]
            start_date = f"{st[2]:02d}.{st[1]:02d}.{st[0]}"
            start_time = f"{st[3]:02d}:{st[4]:02d}"
            end_date = f"{et[2]:02d}.{et[1]:02d}.{et[0]}"
            end_time = f"{et[3]:02d}:{et[4]:02d}"
            ntf = Timeframe(start_date, start_time, end_date, end_time)
            self.events[i].reschedule(ntf)


def test(n):
    HOME_LOCATION = Location(52.22977, 21.01178)  # PKIN

    print(f"------Test with n = {n}------")
    events = []
    for i in range(n):
        t = Timeframe("01.04.2020", "13:00", "02.04.2020", "13:21", "3:00")
        e = Event(f"a{i}", "nothing", "lol",
                  Location(52.237082385, 21.025083233), False, t)
        events.append(e)

    print("Before:")
    for e in events:
        print(e.timeframe.start_date, e.timeframe.start_time)
    planner = Planner(events, HOME_LOCATION)
    planner.plan()
    print("After:")
    for e in events:
        print(e.scheluded_datetime.start_date, e.scheluded_datetime.start_time)


if __name__ == "__main__":
    test(3)
    test(7)
