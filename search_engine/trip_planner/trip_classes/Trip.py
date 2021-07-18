from search_engine.trip_planner.trip_classes.Day import Day
import json


class Trip:
    def __init__(self, days: list):
        self.days = days

    def add_day(self, idx: int, items: list):
        self.days.insert(idx, Day(idx, items))
        self.update_days()

    def remove_day(self, day_id):
        for day in self.days:
            if day.day == day_id:
                self.days.remove(day)

    def add_bulk_days(self, days):
        self.days.extend(days)

    def get_trip_plan(self):
        return self.days

    def switch_2days(self, first_day: int, second_day: int):
        self.days[first_day], self.days[second_day] = self.days[first_day], self.days[second_day]

    def update_days(self):
        for idx, day in enumerate(self.days):
            day.set_index(idx + 1)

    def __repr__(self):
        return 'Trip Plan:%s' % ('\n'.join(str(self.days).split('- ')))

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
