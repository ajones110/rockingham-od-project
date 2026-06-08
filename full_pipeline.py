# Destination information
destination_id = row["PERSISTENT_ID"]
destination_name = row["LOCATION_NAME"]

for origin, trips in cbg_dict.items():

    records.append({
        "origin": str(origin),
        "destination_id": str(destination_id),
        "destination_name": str(destination_name),
        "trips": float(trips)
    })

