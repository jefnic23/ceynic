import type { ProductOut } from '$lib/interfaces/ProductOut';
import { PUBLIC_API_URL } from "$env/static/public";

export const load = async ({ fetch }) => {
    const fetchProducts = async (): Promise<ProductOut[]> => {
        const response = await fetch(`${PUBLIC_API_URL}/products`);

        if (!response.ok) {
            console.log("Error retrieving products.");
            return [];
        }

        const responseData: ProductOut[] = await response.json();

        return responseData;
    }

    return {
        products: fetchProducts()
    }
}