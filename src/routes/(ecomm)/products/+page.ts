import { PUBLIC_API_URL } from '$env/static/public';

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

        const responseData = await response.json();

        return responseData;
    }

    const sort = url.searchParams.get("sort") || "";

    return {
        products: fetchProducts(sort)
    }
}