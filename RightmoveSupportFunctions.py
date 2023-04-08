import math

from RightmoveDictionary import AREA_CODES, COUNTIES, REGIONS, TOWNS


def locationSearch(location : str):
    while True:
        test  = [k for k in AREA_CODES.items() if k == location.upper()]
        new_location = location
        if len(test) > 0:
            nums = [v for k,v in AREA_CODES.items() if k in test]
            break
        test  = [k for k, v in TOWNS.items() if location.title() in v]
        if len(test) > 0:
            nums = [v for k,v in AREA_CODES.items() if k in test]
            break
        test  = [k for k, v in COUNTIES.items() if location.title() in v]
        if len(test) > 0:
            nums = [v for k,v in AREA_CODES.items() if k in test]
            break
        test  = [k for k, v in REGIONS.items() if location.title() in v]
        if len(test) > 0:
            nums = [v for k,v in AREA_CODES.items() if k in test]
            break
        SEARCH = location.title()
        print(f"Wasn't able to locate {location}, were you searching for an Area Code/Town/County/Region?")
        while True:
            reply = input().lower()
            TEST = 'area code'
            if reply == TEST:
                FIND = [k for k in AREA_CODES.keys() if k.startswith(SEARCH[0])]
                if len(FIND) == 0:
                    print('No matches, can only search for Area Code/Town/County/Region')
                    nums = []
                    new_location = ''
                    break
                print(f'These are the closest matchs: \n {FIND} \n Which were you looking for?')
                while True:
                    answer = input()
                    if answer.upper() in FIND:
                        test  = [k for k in AREA_CODES.items() if k == answer.upper()]
                        nums = [v for k,v in AREA_CODES.items() if k in test]
                        new_location = answer.upper()
                        break
                break
            TEST = 'town'
            if reply == TEST:
                MATCHES = [v for v in TOWNS.values() if v.startswith(SEARCH[0]) and v.endswith(SEARCH[-1])]
                FIND = list(set([town for town in MATCHES if math.isclose(sum([ord(l) for l in town]), sum([ord(s) for s in SEARCH]), abs_tol=100)]))
                if len(FIND) == 0:
                    print('No matches, can only search for Area Code/Town/County/Region')
                    nums = []
                    new_location = ''
                    break
                print(f'These are the closest matchs: \n {FIND} \n Which were you looking for?')
                while True:
                    answer = input()
                    if answer.title() in FIND:
                        test  = [k for k, v in TOWNS.items() if answer.title() in v]
                        nums = [v for k,v in AREA_CODES.items() if k in test]
                        new_location = answer.title()
                        break
                break
            TEST = 'county'
            if reply == TEST:
                MATCHES = [v for v in COUNTIES.values() if v.startswith(SEARCH[0]) and v.endswith(SEARCH[-1])]
                FIND = list(set([town for town in MATCHES if math.isclose(sum([ord(l) for l in town]), sum([ord(s) for s in SEARCH]), abs_tol=100)]))
                if len(FIND) == 0:
                    print('No matches, can only search for Area Code/Town/County/Region')
                    nums = []
                    new_location = ''
                    break
                print(f'These are the closest matchs: \n {FIND} \n Which were you looking for?')
                while True:
                    answer = input()
                    if answer.title() in FIND:
                        test  = [k for k, v in COUNTIES.items() if answer.title() in v]
                        nums = [v for k,v in AREA_CODES.items() if k in test]
                        new_location = answer.title()
                        break
                break
            TEST = 'region'
            if reply == TEST:
                MATCHES = [v for v in REGIONS.values() if v.startswith(SEARCH[0]) and v.endswith(SEARCH[-1])]
                FIND = list(set([town for town in MATCHES if math.isclose(sum([ord(l) for l in town]), sum([ord(s) for s in SEARCH]), abs_tol=100)]))
                if len(FIND) == 0:
                    print('No matches, can only search for Area Code/Town/County/Region')
                    nums = []
                    new_location = ''
                    break
                print(f'These are the closest matchs: \n {FIND} \n Which were you looking for?')
                while True:
                    answer = input()
                    if answer.title() in FIND:
                        test  = [k for k, v in REGIONS.items() if answer.title() in v]
                        nums = [v for k,v in AREA_CODES.items() if k in test]
                        new_location = answer.title()
                        print(nums)
                        break
                break
            else:
                print('Please answer with Area Code/Town/County/Region')
        break             
    return(nums, new_location)