from typing import Any

import httpx

from app.core.config import settings


class USDAProvider:
    def __init__(self) -> None:
        self.base_url = settings.USDA_API_BASE_URL.rstrip("/")
        self.api_key = settings.USDA_API_KEY

        if not self.api_key:
            raise ValueError(
                "USDA_API_KEY is not configured"
            )

    def search_food(
        self,
        query: str,
        page_size: int = 10,
    ) -> list[dict[str, Any]]:
        url = f"{self.base_url}/foods/search"

        params = {
            "api_key": self.api_key,
        }

        payload = {
            "query": query,
            "pageSize": page_size,
        }

        response = httpx.post(
            url,
            params=params,
            json=payload,
            timeout=10.0,
        )

        response.raise_for_status()

        data = response.json()

        return data.get("foods", [])

    def get_food(
        self,
        fdc_id: int,
    ) -> dict[str, Any]:
        url = f"{self.base_url}/food/{fdc_id}"

        params = {
            "api_key": self.api_key,
        }

        response = httpx.get(
            url,
            params=params,
            timeout=10.0,
        )

        response.raise_for_status()

        return response.json()