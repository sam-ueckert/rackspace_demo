import random
import string
import json
from datetime import date

data_centers = ["east", "west", "south", "north"]
demo_data = []

for data_center in data_centers:
    data_center_dict = {"data_center_name": data_center, "zones": {}}
    num_zones = random.randint(5, 20)
    for i in range(num_zones):
        zone_letter = string.ascii_uppercase[i]
        data_center_dict["zones"][zone_letter] = []
        num_pa1410s = random.randint(0, 10)
        for j in range(num_pa1410s):
            pa1410_name = f"{data_center}-zone{zone_letter}-pa1410-{j}"
            pa1410_data = {"name": pa1410_name, "vsys": []}
            num_vsys = random.randint(0, 4)
            for k in range(1, num_vsys + 1):
                vsys_name = f"vsys{k}"
                pa1410_data["vsys"].append({"name": vsys_name})
            data_center_dict["zones"][zone_letter].append(pa1410_data)
    demo_data.append(data_center_dict)

print(demo_data)
# filename = f"demo_data_{date.today()}.json"
filename = "demo_data.json"

with open(filename, 'w') as f:
    json.dump(demo_data, f)