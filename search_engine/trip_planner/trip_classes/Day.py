from Item import Item
from copy import deepcopy


class Day:
    def __init__(self, idx: int, items: list):
        self.idx = idx
        self.items = items

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
        self.idx = idx

    def __repr__(self):
        return '- day%s:%s' % (self.idx, '\n'.join(str(self.items).split('- ')))
