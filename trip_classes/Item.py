class Item:
    def __init__(self, item_type: str, jsn):
        self.item_type = item_type
        self.item_id = jsn['id']
        self.coordinate = jsn['coordinate']
        self.rate = jsn['guestrating']

    def __repr__(self):
        return '- Type: %s, ID: %s, Rate: %s, Coordinates: %s' % (
            self.item_type, self.item_id, self.rate, self.coordinate)
        # return self.item_type
