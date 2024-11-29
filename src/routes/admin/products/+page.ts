import type { ProductsOut } from '$lib/interfaces/product';
import { PUBLIC_API_URL } from "$env/static/public";

export const load = async ({ fetch }) => {
    const fetchProducts = async (): Promise<ProductsOut[]> => {
        const response = await fetch(`${PUBLIC_API_URL}/products`);

        if (!response.ok) {
            console.log("Error retrieving products.");
            return [];
        }

        const responseData = await response.json();

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return responseData.map((item: any): ProductsOut => ({
            id: item.id,
            title: item.title,
            price: item.price,
            height: item.height,
            width: item.width, 
            medium: item.mediumId === 1 ? "Painting" : "Print",
            thumbnail: item.thumbnail,
            imageUrl: item.imageUrl
        }));
    }

    return {
        products: fetchProducts()
    }
}