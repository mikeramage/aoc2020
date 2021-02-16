import re
FILE = "day21_input.txt"
food_regex = re.compile("^(?P<ingredients>[\w\s]+)\(contains (?P<allergies>[\w\s,]+)\)\s*$")

def read_file(filename):
    foods = list()
    with open(filename, 'r') as f:
        for line in f:
            food_match = re.match(food_regex, line.strip())
            if food_match:
                ingredients = food_match.group('ingredients').strip().split(' ')
                allergies = food_match.group('allergies').strip().split(', ')
                foods.append((ingredients, allergies))
            else:
                raise Exception("Line didn't match expected pattern")
    return foods

foods = read_file(FILE)
all_ingredients = set([ingredient for food in foods for ingredient in food[0]])
all_allergens = set([allergen for food in foods for allergen in food[1]])

print(f"Foods: {foods}")
print(f"Allergens: {all_allergens}")
print(f"Ingredients: {all_ingredients}")

ingredient_allergen_map = dict()
#initially an ingredient could take any allergen - initialize dict with this
for ingredient in all_ingredients:
    ingredient_allergen_map[ingredient] = set(all_allergens)

print(f"Map: {ingredient_allergen_map}")

for food in foods:
    for ingredient in ingredient_allergen_map.keys():
        if ingredient not in food[0]:
            for allergen in food[1]:
                ingredient_allergen_map[ingredient].discard(allergen)

print(f"Map after filtering: {ingredient_allergen_map}")
non_allergic_ingredients = set()
count = 0
for ingredient in ingredient_allergen_map.keys():
    if len(ingredient_allergen_map[ingredient]) == 0:
        non_allergic_ingredients.add(ingredient)
        for food in foods:
            if ingredient in food[0]:
                count += 1

print(f"Total count of appearances of ingredients with no allergens: {count}")

#Filter map again to pin down exact mapping, but reverse map to get answer more
#easily

for ingredient in non_allergic_ingredients:
    del ingredient_allergen_map[ingredient]

print(f"Huh? {ingredient_allergen_map}")

allergen_ingredient_map = dict()

still_unreduced = True

while still_unreduced:
    still_unreduced = False
    for ingredient in ingredient_allergen_map.keys():
        for allergen, x in allergen_ingredient_map.items():
            if x != ingredient:
                ingredient_allergen_map[ingredient].discard(allergen)
        if len(ingredient_allergen_map[ingredient]) > 1:
            still_unreduced = True
    for ingredient, allergens in ingredient_allergen_map.items():
        if len(allergens) == 1:
            allergen_ingredient_map[list(allergens)[0]] = ingredient


    print(f"{allergen_ingredient_map}")

dangerous_ingredients = [allergen_ingredient_map[allergen] for allergen in sorted(all_allergens)]

part2 = ','.join(dangerous_ingredients)

print(f"{part2}")



