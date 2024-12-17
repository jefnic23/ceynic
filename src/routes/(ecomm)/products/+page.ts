import { PUBLIC_API_URL } from '$env/static/public';
import type { PriceRange } from '$lib/interfaces/priceRange.js';
import type { ProductsOut } from '$lib/interfaces/product.js';

export const load = async ({ fetch, url }) => {
    const fetchProducts = async (sort: string = "") => {
        const queryParams = new URLSearchParams();

        if (sort) {
            queryParams.append("sort", sort);
        }

        const response = await fetch(`${PUBLIC_API_URL}/products?${queryParams.toString()}`);

        if (!response.ok) {
            console.log("Error retrieving products.");
            return [];
        }

        const responseData: ProductsOut[] = await response.json();

        return responseData;
    }

    const fetchPriceRange = async () => {
        const response = await fetch(`${PUBLIC_API_URL}/products/priceRange`);

        if (!response.ok) {
            console.log("Error retrieving price range.");
            return;
        }

        const responseData: PriceRange = await response.json();

        return responseData;
    }

    const sort = url.searchParams.get("sort") || "";

    return {
        products: fetchProducts(sort),
        priceRange: fetchPriceRange()
    }
}