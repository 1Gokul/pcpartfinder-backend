import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"
}


def get_soup(link):
    response = requests.get(
        link,
        headers=headers,
    )
    return BeautifulSoup(response.content, "lxml")


async def vedant_computers(query):
    soup = get_soup(
        f"https://www.vedantcomputers.com/index.php?route=product/search&search={query}"
    )

    results = []
    for product in soup.select(".main-products.product-grid .caption"):
        results.append(
            {
                "store": "vedant",
                "name": product.select_one(".name a").get_text(),
                "link": product.select_one(".name a")["href"].split("?", 1)[0],
                "price": f"₹{product.select_one('.price').get_text(strip=True).split('₹')[-1]}",
            }
        )

    return results


async def md_computers(query):
    search_query = query.replace(" ", "+")
    soup = get_soup(
        f"https://mdcomputers.in/index.php?search={search_query}&submit_search=&route=product%2Fsearch"
    )

    results = []
    for product in soup.select(".product-item-container .right-block.right-b"):
        results.append(
            {
                "store": "md",
                "name": product.select_one("h4 a").get_text(),
                "link": product.select_one("h4 a")["href"].split("?", 1)[0],
                "price": f"₹{product.select_one('.price').get_text(strip=True).split('₹')[-1]}",
            }
        )

    return results


async def prime_abgb(query):
    search_query = query.replace(" ", "+")
    soup = get_soup(
        f"https://www.primeabgb.com/?post_type=product&taxonomy=product_cat&product_cat=0&s={search_query}"
    )

    results = []
    for product in soup.select(".products .product-innfo"):
        results.append(
            {
                "store": "primeabgb",
                "name": product.select_one(".product-name a").get_text(),
                "link": product.select_one(".product-name a")["href"],
                "price": f"₹{product.select_one('.woocommerce-Price-amount').get_text(strip=True).split('₹')[-1]}"
            }
        )

    return results


async def rp_tech(query):
    search_query = query.replace(" ", "+")
    soup = get_soup(
        f"https://rptechindia.in/catalogsearch/result/index/?q={search_query}&stock_filter=258"
    )

    results = []
    for product in soup.select(".products-row .product-box"):
        results.append(
            {
                "store": "rptech",
                "name": product.select_one(".product-title a").get_text(strip=True),
                "link": product.select_one(".product-title a")["href"],
                "price": f"₹{product.select_one('.price-tag').get_text(strip=True).split('₹')[-1]}",
            }
        )

    return results