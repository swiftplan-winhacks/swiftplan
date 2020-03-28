from dataclasses import dataclass
import datetime
from typing import List, NamedTuple, Tuple
import json
from copy import deepcopy


@dataclass
class Task:
    id: int
    type: str
    loc: Tuple
    begin: datetime.datetime
    end: datetime.datetime
    dur: datetime.timedelta


class Interval(NamedTuple):
    begin: datetime.datetime
    end: datetime.datetime
    loc_b: Tuple
    loc_e: Tuple


class Planner:
    def __init__(self):
        self.rigid_tasks, self.flexible_tasks, s_date, e_date = self.parse("gg.json")  # json received from application 
        days = [s_date + datetime.timedelta(days=i) for i in range((e_date - s_date).days + 1)]
        home_loc = (13, 37)
        
        self.freetime = [
            Interval(d + datetime.timedelta(hours=7), 
                     d + datetime.timedelta(hours=23), 
                     home_loc, 
                     home_loc) for d in days
        ]
        self.placed_tasks = []
        self.solution_found = False
        self.distances = {}

    def __repr__(self):
        return str(self.placed_tasks)

    def parse(self, file_loc):
        with open(file_loc) as f:
            file = json.load(f)
        
        def strip1(k):
            s = file['events'][k]['time_frame']['start_date'] + \
                " "+file['events'][k]['time_frame']['start_time']
            fmt = "%d.%m.%Y %H:%M"
            return datetime.datetime.strptime(s, fmt)

        def strip2(k):
            s = file['events'][k]['time_frame']['end_date'] + \
                " "+file['events'][k]['time_frame']['end_time']
            fmt = "%d.%m.%Y %H:%M"
            return datetime.datetime.strptime(s, fmt)

        rigid = []
        smooth = []
        for i in range(len(file['events'])):
            k = Task(file['events'][i]['id'],
                    file['events'][i]['type'],
                    (file['events'][i]['location']['lat'],
                    file['events'][i]['location']['lng']),
                    strip1(i),
                    strip2(i),
                    file['events'][i]['time_frame']['duration'])

            if file['events'][i]['fixed'] == True:
                k.dur = k.end - k.begin
                rigid.append(k)
            else:
                h, m = [int(e) for e in k.dur.split(":")]
                k.dur = datetime.timedelta(hours = h, minutes = m)
                smooth.append(k)

        s_time=datetime.datetime.strptime(file['global_time_frame']['start'], "%d.%m.%Y")
        e_time=datetime.datetime.strptime(file['global_time_frame']['end'], "%d.%m.%Y")
        return rigid, smooth, s_time, e_time

    def dist(self, loc1, loc2, time):
        if (loc1, loc2, time) in self.distances:
            return self.distances[(loc1, loc2, time)]
        else:
            # zapytać API
            dist = datetime.timedelta(0)  # z API
            self.distances[(loc1, loc2, time)] = dist
            return dist

    def place(self, t: Task, invls):
        for ivl in invls:
            s_time = max(ivl.begin, t.begin)
            e_time = min(ivl.end,   t.end)
            aval_time = e_time - s_time
            if aval_time > datetime.timedelta(0):
                tot_dur = self.dist(ivl.loc_b, t.loc, s_time) + \
                    t.dur + \
                    self.dist(t.loc, ivl.end, s_time + t.dur)
                if tot_dur <= aval_time:
                    # print("Posssible", t, ivl)
                    break
        else:
            print("Cannot allocate task")
            return False
        if ivl.begin != s_time:
            invls.append(
                Interval(ivl.begin,
                         s_time + self.dist(ivl.loc_b, t.loc, s_time),
                         ivl.loc_b,
                         t.loc)
            )

        if s_time + tot_dur < ivl.end:
            invls.append(
                Interval(s_time + self.dist(ivl.loc_b, t.loc, s_time) + t.dur,
                         ivl.end,
                         t.loc,
                         ivl.loc_e)
            )
        invls.remove(ivl)
        invls.sort()

        self.placed_tasks.append((
            s_time + self.dist(ivl.loc_b, t.loc, s_time),
            s_time + self.dist(ivl.loc_b, t.loc, s_time) + t.dur,
            t))
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

    def plan(self):
        invls = self.freetime
        for t in self.rigid_tasks:
            self.place(t, invls)

        self.flexible_tasks.sort(key=lambda task: -task.dur)

        self.allocate(self.flexible_tasks, invls)
        print("Happy end")
        for e in self.placed_tasks:  # task_time_start, task_time_end, task 
            print(e)


planner = Planner()
planner.plan()
