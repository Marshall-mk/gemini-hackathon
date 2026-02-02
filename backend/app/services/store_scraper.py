import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import urllib.parse


class StoreScraper:
    def __init__(self):
        self.stores = {
            "amazon": {
                "name": "Amazon Fresh",
                "search_url": "https://www.amazon.com/s?k=",
                "enabled": True
            }
        }

    def find_ingredient_stores(self, ingredient_name: str) -> List[Dict[str, str]]:
        """
        Find stores where ingredient can be purchased
        Returns list of store links
        """
        stores_list = []

        # Clean ingredient name for search
        clean_name = self._clean_ingredient_name(ingredient_name)

        for store_key, store_info in self.stores.items():
            if not store_info["enabled"]:
                continue

            try:
                search_url = store_info["search_url"] + urllib.parse.quote(clean_name)
                stores_list.append({
                    "store_name": store_info["name"],
                    "search_url": search_url,
                    "ingredient": ingredient_name
                })
            except Exception as e:
                print(f"Error creating link for {store_info['name']}: {str(e)}")

        return stores_list

    def _clean_ingredient_name(self, ingredient: str) -> str:
        """Clean ingredient name for search"""
        # Remove common measurement words
        words_to_remove = ['fresh', 'dried', 'frozen', 'canned', 'chopped', 'diced',
                          'sliced', 'whole', 'ground', 'minced', 'grated']

        words = ingredient.lower().split()
        cleaned_words = [w for w in words if w not in words_to_remove]

        return ' '.join(cleaned_words) if cleaned_words else ingredient

    def get_grocery_cart_link(self, ingredients: List[str], store: str = "amazon") -> str:
        """
        Generate a grocery list link for Amazon Fresh
        This creates a search URL with multiple ingredients
        """
        if store not in self.stores:
            store = "amazon"

        store_info = self.stores[store]

        # Create a comprehensive search URL for all ingredients
        all_ingredients = ", ".join(ingredients)
        search_url = store_info["search_url"] + urllib.parse.quote(all_ingredients)

        return search_url

    def create_shopping_list(self, ingredients: List[Dict]) -> Dict:
        """
        Create a comprehensive shopping list with store links for each ingredient
        """
        shopping_list = {
            "total_items": len(ingredients),
            "items": []
        }

        for ingredient in ingredients:
            ingredient_name = ingredient.get("name", "")
            quantity = ingredient.get("quantity", "")
            unit = ingredient.get("unit", "")

            stores = self.find_ingredient_stores(ingredient_name)

            shopping_list["items"].append({
                "ingredient": ingredient_name,
                "quantity": f"{quantity} {unit}".strip(),
                "stores": stores
            })

        # Add bulk shopping link for Amazon Fresh
        ingredient_names = [ing.get("name", "") for ing in ingredients]
        shopping_list["bulk_shopping_link"] = self.get_grocery_cart_link(ingredient_names, "amazon")

        return shopping_list
