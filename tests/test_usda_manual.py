from app.services.nutrition.usda_provider import USDAProvider


provider = USDAProvider()

foods = provider.search_food(
    query="chicken breast",
)

print("Found foods:", len(foods))

for food in foods[:3]:
    print(
        food.get("fdcId"),
        "-",
        food.get("description"),
    )

if foods:
    fdc_id = foods[0]["fdcId"]

    food = provider.get_food(fdc_id)

    print("\nFood details:")
    print("FDC ID:", food.get("fdcId"))
    print("Description:", food.get("description"))
    print("Nutrients:", len(food.get("foodNutrients", [])))