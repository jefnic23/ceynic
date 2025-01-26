import { PUBLIC_API_URL } from '$env/static/public';
import { ProductFilter } from '$lib/enums/productFilter.js';
import type { MediumCount } from '$lib/interfaces/mediumCount';
import type { PriceRange } from '$lib/interfaces/priceRange.js';
import type { ProductsOut } from '$lib/interfaces/product.js';
import type { SizeRanges } from '$lib/interfaces/sizeRanges';

export const load = async ({ fetch, url }) => {
    const fetchProducts = async (sort: string = "", filters: (string | null)[][] = []) => {
        const queryParams = new URLSearchParams();

        if (sort) queryParams.append("sort", sort);

        filters.forEach((filter) => {
            if (filter[1]) queryParams.append(filter[0] as string, filter[1] as string);
        });

        const response = await fetch(`${PUBLIC_API_URL}/products?${queryParams.toString()}`);

        if (!response.ok) {
            console.log("Error retrieving products.");
            return [];
        }

        const responseData: ProductsOut[] = await response.json();

        return responseData;
    }

    const fetchPriceRange = async (): Promise<PriceRange> => {
        const response = await fetch(`${PUBLIC_API_URL}/products/priceRange`);

        if (!response.ok) {
            console.log("Error retrieving price range.");
            return { minimum: 0, maximum: 0 };
        }

        const responseData: PriceRange = await response.json();

        return responseData;
    }

    const fetchMediumCounts = async (): Promise<MediumCount[]> => {
        const response = await fetch(`${PUBLIC_API_URL}/products/mediumCounts`);

        if (!response.ok) {
            console.log("Error retrieving price range.");
            return [];
        }

        const responseData: MediumCount[] = await response.json();

        return responseData;
    }

    const fetchSizeRanges = async (): Promise<SizeRanges> => {
        const response = await fetch(`${PUBLIC_API_URL}/products/sizeRanges`);

        if (!response.ok) {
            console.log("Error retrieving price range.");
            return { widthMinimum: 0, widthMaximum: 0, heightMinimum: 0, heightMaximum: 0 };
        }

        const responseData: SizeRanges = await response.json();

        return responseData;
    }

    const sort = url.searchParams.get("sort") || "";
    const filters = Object.values(ProductFilter).map(value => [value, url.searchParams.get(value)]);

    return {
        products: fetchProducts(sort, filters),
        priceRange: fetchPriceRange(),
        mediumCounts: fetchMediumCounts(),
        sizeRanges: fetchSizeRanges()
    }
}