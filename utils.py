def get_spn(toponym):
    envelope = toponym.get("boundedBy", {}).get("Envelope", {})

    if not envelope:
        return "0.005,0.005"

    lower_corner = envelope["lowerCorner"].split()
    upper_corner = envelope["upperCorner"].split()

    width = abs(float(upper_corner[0]) - float(lower_corner[0]))
    height = abs(float(upper_corner[1]) - float(lower_corner[1]))

    return f"{width},{height}"