import { PUBLIC_API_URL } from '$env/static/public';

export const load = async ({ fetch, params }) => {
    const fetchProduct = async (productId: string) => {
        const response = await fetch(`${PUBLIC_API_URL}/products/${productId}`);

        if (response.status !== 200) {
            console.log("Error retrieving product.");
        }
    
        const responseData = await response.json();

        return responseData;
    }

    return {
        product: fetchProduct(params.productId)
    }
}