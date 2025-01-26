import { PUBLIC_API_URL } from '$env/static/public';
import type { Location } from '$lib/interfaces/location.js';

export const load = async ({ fetch, params }) => {
    const fetchProduct = async (productId: string) => {
        const response = await fetch(`${PUBLIC_API_URL}/products/${productId}`);

        if (response.status !== 200) {
            console.log("Error retrieving product.");
        }
    
        const responseData = await response.json();

        return responseData;
    }

    const fetchShippingLocation = async () => {
        // todo: fetch this on any page load and store to avoid multiple calls
        const response = await fetch(`${PUBLIC_API_URL}/storefronts/location`);

        if (!response.ok) {
            console.log("Error retrieving shipping location.");
        }

        const responseData: Location = await response.json();

        return responseData;
    }

    return {
        product: fetchProduct(params.productId),
        location: fetchShippingLocation()
    }
}