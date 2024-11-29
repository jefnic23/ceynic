import type { Actions } from "@sveltejs/kit";
import { PUBLIC_API_URL } from "$env/static/public";

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
