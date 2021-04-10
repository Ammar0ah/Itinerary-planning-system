class Item: 
    def __init__(self, item_type : str, item_id : str, item_info : dict):
        self.item_type = item_type
        self.item_id = item_id
        self.item_info = item_info 
        
    def __repr__(self):
        return '- Type: %s , ID: %s, Info: %s' %(self.item_type, self.item_id, self.item_info)    