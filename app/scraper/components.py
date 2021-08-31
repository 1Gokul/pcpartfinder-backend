import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
}


async def vedant_computers(query):
    response = requests.get(
        f"https://www.vedantcomputers.com/index.php?route=product/search&search={query}",
        headers=headers,
    )
    soup = BeautifulSoup(response.content, "lxml")

    results = []
    for product in soup.select(".main-products.product-grid .caption"):
        results.append(
            {
                "name": product.select_one(".name a").get_text(),
                "link": product.select_one(".name a")["href"],
                "price": product.select_one(".price").get_text(strip=True),
            }
        )

    return results
