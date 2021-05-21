from trip_classes.Day import Day
from trip_classes.Item import Item


class Trip:
    def __init__(self, user_name, days: list):
        self.user_name = user_name
        self.days = days

    def add_day(self, idx: int, items: list):
        self.days.insert(idx, Day(idx, items))
        self.update_days()

    def remove_day(self, day_id):
        for day in self.days:
            if day.day == day_id:
                self.days.remove(day)

    def get_trip_plan(self):
        return self.days

    def switch_2days(self, first_day: int, second_day: int):
        self.days[first_day], self.days[second_day] = self.days[first_day], self.days[second_day]

    def update_days(self):
        for idx, day in enumerate(self.days):
            day.set_index(idx + 1)

    def __repr__(self):
        return 'User Name: %s \nTrip Plan:%s' % (self.user_name, '\n'.join(str(self.days).split('- ')))
