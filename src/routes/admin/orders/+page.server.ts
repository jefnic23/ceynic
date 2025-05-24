import { PUBLIC_API_URL } from "$env/static/public";
import type { OrdersOut } from "$lib/interfaces/OrdersOut";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ fetch, cookies }) => {
    const fetchOrders = async (): Promise<OrdersOut[]> => {
        const response = await fetch(`${PUBLIC_API_URL}/orders`, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${cookies.get("access")}`,
            }
        });

        if (!response.ok) {
            console.log("Error retrieving orders.");
            return [];
        }

        const responseData: OrdersOut[] = await response.json();

        return responseData;
    }

    return {
        orders: fetchOrders()
    }
}