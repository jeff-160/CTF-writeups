from collections import defaultdict

coords = defaultdict(list)

with open("gps.txt") as f:
    current_file = None
    lat = lon = None

    for line in f:
        if line.startswith("========"):
            current_file = line.split("/")[-1].strip()
        elif "GPS Latitude" in line:
            lat = float(line.split(":")[1])
        elif "GPS Longitude" in line:
            lon = float(line.split(":")[1])
            coords[(lat, lon)].append(current_file)

for (lat, lon), files in coords.items():
    if len(files) == 1:
        print(lat, lon)