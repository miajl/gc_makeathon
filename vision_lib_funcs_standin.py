


class AprilDetector():
    def __init__(self, camera_address, key_fname, box_loc_fname):
        self.item_dict = {"Cheese": 0, "Chorizo": 1, "Beer": 2, "Mango Juice": 3, "Eggs": 4, "Tequila": 5}
        return

    def get_item_loc_by_key(self, desired_item):
        # ret val zero or greater is box location
        # -1: found the item, but it is not in any box location
        # -2: Did not find the item
        # -3: desired item does not match any in the key dictionary
        if desired_item in self.item_dict.keys():
           return self.item_dict[desired_item]
        return -1
    def clean(self):
       return
    
             
         