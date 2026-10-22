import { PUBLIC_API_URL } from "$env/static/public";
import type { OrderDetails } from "$lib/interfaces/OrderDetails";
import { error } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ fetch, cookies, params }) => {
    const fetchOrder = async (orderId: string): Promise<OrderDetails> => {
        const response = await fetch(`${PUBLIC_API_URL}/admin/orders/${encodeURIComponent(orderId)}`, {
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
    default: async ({ request, cookies }) => {
        const data = await request.formData();
        const action = data.get("action");
        const recordId = data.get("recordId");

        if (
            typeof recordId !== 'string' ||
            !/^\d+$/.test(recordId) ||
            typeof action !== 'string' ||
            !['capture', 'void', 'refund', 'payment/refresh'].includes(action)
        ) {
            error(400, 'Invalid order action.');
        }

        const response = await fetch(`${PUBLIC_API_URL}/orders/${recordId}/${action}`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${cookies.get("access")}`,
            }
        });

		if (!response.ok) {
			const result = await response.json().catch(() => null);
			const message = typeof result?.detail === 'string'
				? result.detail
				: 'Unable to update payment. Check the order state before retrying.';
			error(response.status, message);
		}

		const responseData = await response.json();

        return responseData;
    }
} 
