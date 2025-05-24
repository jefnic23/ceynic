import { PUBLIC_API_URL } from '$env/static/public';
import type { ProductMetadata } from '$lib/interfaces/ProductMetadata';
import type { ProductsOut } from '$lib/interfaces/ProductsOut';

export const load = async ({ fetch, url }) => {
    const fetchProducts = async () => {
        const response = await fetch(`${PUBLIC_API_URL}/products?${url.searchParams}`);

        if (!response.ok) {
            console.log("Error retrieving products.");
            return [];
        }

        const responseData: ProductsOut[] = await response.json();

        return responseData;
    }

    const fetchMetadata = async (): Promise<ProductMetadata | null> => {
        const response = await fetch(`${PUBLIC_API_URL}/products/metadata`);

        if (!response.ok) {
            console.log("Error retrieving metadata.");
            return null;
        }

        const responseData: ProductMetadata = await response.json();

        return responseData;
    }

    return {
        products: fetchProducts(),
        metadata: fetchMetadata(),
    }
}