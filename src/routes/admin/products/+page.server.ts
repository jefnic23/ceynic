import { error } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { PUBLIC_API_URL } from '$env/static/public';

export const load: PageServerLoad = async () => {}

export const actions: Actions = {
    default: async ({ request, cookies }) => {
        const productData = await request.formData();
        
        if (productData.get("filesChanged") !== "true") productData.delete("images");

        productData.delete("filesChanged");

        const response = await fetch(`${PUBLIC_API_URL}/products/${productData.get("id")}`, {
            method: "PUT",
            headers: {
                "Authorization": `Bearer ${cookies.get("access")}`,
            },
            body: productData
        });

        if (response.status !== 200) {
            error(500, "Error updating product.");
        }

        return ({success: true});
    }
} 