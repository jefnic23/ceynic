import { PUBLIC_API_URL } from '$env/static/public';
import type { ProductOut, MediumOut } from '$lib/interfaces/ProductOut';

export const load = async ({ fetch }) => {
    const fetchProducts = async () => {
        const response = await fetch(`${PUBLIC_API_URL}/products`);

        if (!response.ok) {
            console.log("Error retrieving products.");
        }

        const responseData: ProductOut[] = await response.json();

        return responseData.filter((product: ProductOut) => (product.medium as MediumOut).name === "Painting");
    }

    return {
        products: fetchProducts()
    }
}