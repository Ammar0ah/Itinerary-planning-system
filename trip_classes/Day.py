from trip_classes.Item import Item


class Day:
    def __init__(self, idx: int, items: list):
        self.idx = idx
        self.items = items

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item_id):
        for item in self.items:
            if item.item_id == item_id:
                self.items.remove(item)

    def set_index(self, idx: int):
        self.idx = idx

    def __repr__(self):
        return '- day%s:%s' % (self.idx, '\n'.join(str(self.items).split('- ')))
