import { PUBLIC_API_URL } from '$env/static/public';
import type { ProductsOut } from '$lib/interfaces/product.js';

export const load = async ({ fetch }) => {
    const fetchProducts = async () => {
        const response = await fetch(`${PUBLIC_API_URL}/products`);

        if (!response.ok) {
            console.log("Error retrieving products.");
        }

        const responseData: ProductsOut[] = await response.json();

        return responseData;
    }

    return {
        products: fetchProducts()
    }
}