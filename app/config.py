DB_TABLE_NAME = "crawler_data"

SCRAPY_ITEM_KEYS = ["name", "price", "url", "store"]

STORES = [
    "Vedant_Computers",
    "MD_Computers",
    "Prime_ABGB",
    "IT_Depot",
    "PC_Shop",
    "PC_Studio",
    "Elite_Hubs",
    "National_PC",
    "Tech_Booze",
]

# Used to categorize the scraped items
DB_CATEGORIES = {
    **dict.fromkeys(
        [
            "graphics-cards",
            "graphic-cards",
            "graphics-card",
            "graphic-card",
            "graphic-cards-gpu",
            "Graphic+Cards",
        ],
        "GPU",
    )
}
