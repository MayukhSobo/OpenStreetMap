
def testing(*args):
    for each in args[0]:
        print(each)


a = [
    (
        {'amenity': 'place_to_worship'},
        {'operation': 'add_field'},
        {'fieldName': 'religion'},
        {'condition': 'false'},
        {'on': 'religion'}
    ),

    (
        {'name': '*'},
        {'operation': 'remove_entry'},
        {'condition': 'false'},
        {'on': 'name'}
    ),

    (
        {'amenity': 'atm'},
        {'operation': 'extract'},
        {'from': 'amenity > bank'}
    ),

    (
        {'addr:country': 'IN'},
        {'operation': 'replace'},
        {'IN': 'India'},
        {'on': 'addr:country'}
    ),

    (
        {'addr:postcode': '*'},
        {'operation': 'fix'},
        {'country': 'India'},
        {'on': 'addr:postcode'}
    ),

    (
        {'amenity': 'marketplace'},
        {'operation': 'remove_entry'},
        {'condition': 'irrelevant'},
        {'on': 'name'}
    ),

    (
        {'amenity': 'bar'},
        {'operation': 'merge'},
        {'into': 'amenity > pub'}
    ),

    (
        {'amenity': 'restaurants'},
        {'operation': 'fix'},
        {'on': 'name'}
    ),

    (
        {'way': 'ref'},
        {'operation': 'change_field'},
        {'fieldName': 'type'},
        {'condition': 'ref[0] == ref[-1]'},
        {'on': 'type'}
    ),
]
testing(a)
