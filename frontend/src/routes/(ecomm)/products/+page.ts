import { PUBLIC_API_URL } from '$env/static/public';
import type { ProductMetadata } from '$lib/interfaces/ProductMetadata';
import type { ProductOut } from '$lib/interfaces/ProductOut';
import { ProductFilter } from '$lib/enums/productFilter';

export const load = async ({ fetch, url, parent }) => {
    const { sortAndFilterEnabled: enabled } = await parent();
    const sortAndFilterEnabled = await enabled;

    const fetchProducts = async () => {
        const searchParams = new URLSearchParams(url.searchParams);
        if (!sortAndFilterEnabled) {
            for (const param of ['sort', ...Object.values(ProductFilter)]) {
                searchParams.delete(param);
            }
        }

        const response = await fetch(`${PUBLIC_API_URL}/products${searchParams.size ? `?${searchParams}` : ''}`);

        if (!response.ok) {
            console.log("Error retrieving products.");
            return [];
        }

        const responseData: ProductOut[] = await response.json();

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
        metadata: sortAndFilterEnabled ? fetchMetadata() : Promise.resolve(null),
        sortAndFilterEnabled,
    }
}
