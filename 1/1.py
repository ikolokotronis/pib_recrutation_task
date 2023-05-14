def group_by(elements, field):
    result = []
    groups = {}

    for element in elements:
        category = element[field]
        item = {key: value for key, value in element.items() if key != field}

        if category in groups:
            groups[category].append(item)
        else:
            groups[category] = [item]

    for category, items in groups.items():
        result.append({"category": category, "items": items})

    return result


print(
    group_by(
        elements=[
            {"name": "Pierogi", "category": "główne", "value": 21},
            {"name": "Rosół", "category": "zupa", "value": 16},
            {"name": "Ogórkowa", "category": "zupa", "value": 17},
            {"name": "Mascarpone", "category": "deser", "value": 10},
            {"name": "Lody", "category": "deser", "value": 6},
        ],
        field="category",
    )
)
