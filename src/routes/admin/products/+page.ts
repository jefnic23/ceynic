import type { ProductsOut } from '$lib/interfaces/ProductsOut';
import { PUBLIC_API_URL } from "$env/static/public";

export const load = async ({ fetch }) => {
    const fetchProducts = async (): Promise<ProductsOut[]> => {
        const response = await fetch(`${PUBLIC_API_URL}/products`);

        if (!response.ok) {
            console.log("Error retrieving products.");
            return [];
        }

        const responseData: ProductsOut[] = await response.json();

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return responseData;
    }

    return {
        products: fetchProducts()
    }
}