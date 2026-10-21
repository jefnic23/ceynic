import { PUBLIC_API_URL } from "$env/static/public";
import type { OrderDetails } from "$lib/interfaces/OrderDetails";
import { error } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ fetch, cookies, params }) => {
    const fetchOrder = async (orderId: string): Promise<OrderDetails> => {
        const response = await fetch(`${PUBLIC_API_URL}/orders/${orderId}`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${cookies.get("access")}`,
            }
        });

        if (!response.ok) {
            console.log("Error retrieving order.");
            error(500, "Error retrieving order.");
        }

        const responseData: OrderDetails = await response.json();

        return responseData;
    }

    return {
        order: fetchOrder(params.orderId)
    }
}

export const actions: Actions = {
    default: async ({ request, params, cookies }) => {
        const data = await request.formData();
        const action = data.get("action");

        const response = await fetch(`${PUBLIC_API_URL}/orders/${params.orderId}/${action}`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${cookies.get("access")}`,
            }
        });

		if (response.status !== 200) {
			console.log('Error capturing payment.');
			error(500, "Error capturing payment.");
		}

		const responseData = await response.json();

        return responseData;
    }
} 
