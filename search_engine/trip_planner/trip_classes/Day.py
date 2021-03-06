from search_engine.trip_planner.trip_classes.Item import Item
from copy import deepcopy


class Day:
    def __init__(self, idx: int, activities: list):
        self.day_index = idx
        self.items = activities

    def add_item(self, item):
        self.items.append(item)

    def insert_item(self, item, index):
        self.items.insert(index, item)

    def remove_item(self, item_id):
        for item in self.items:
            if item.item_id == item_id:
                self.items.remove(item)

    def swap_items(self, item1_ind, item2_ind):
        self.items[item1_ind], self.items[item2_ind] = self.items[item2_ind], self.items[item1_ind]

    def set_index(self, idx: int):
        self.day_index = idx

    def __repr__(self):
        return '- day%s:%s' % (self.day_index, '\n'.join(str(self.items).split('- ')))
