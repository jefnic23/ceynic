import type { Actions } from "@sveltejs/kit";
import { PUBLIC_API_URL } from "$env/static/public";
import type { ProductOut } from "$lib/interfaces/ProductOut";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ url, fetch }) => {
    const productId = url.searchParams.get('productId');
    if (!productId || !/^[1-9]\d*$/.test(productId) || !Number.isSafeInteger(Number(productId))) {
        return { inquiry: null };
    }

    try {
        const response = await fetch(`${PUBLIC_API_URL}/products/${productId}`);
        if (!response.ok) return { inquiry: null };

        const product: ProductOut = await response.json();
        const imageIndex = Number(url.searchParams.get('imageIndex') ?? 0);
        const image = Number.isSafeInteger(imageIndex) && imageIndex >= 0
            ? product.images?.[imageIndex] ?? product.images?.[0]
            : product.images?.[0];

        return { inquiry: { productId: product.id, title: product.title, imageUrl: image?.url ?? null } };
    } catch {
        return { inquiry: null };
    }
};

export const actions = {
    default: async ({ request }) => {
        const formData = await request.formData();

        const response = await fetch(`${PUBLIC_API_URL}/contact`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            console.log("Error submitting form.");
        }

        return { success: true }
    }
} satisfies Actions;
