import { PUBLIC_API_URL } from '$env/static/public';
import type { OrderOut } from '$lib/interfaces/OrderOut';
import type { PageServerLoad } from './$types';

interface UserOut {
	email: string;
	firstName: string | null;
	lastName: string | null;
}

export const load: PageServerLoad = async ({ fetch, cookies }) => {
	const fetchUser = async (): Promise<UserOut | null> => {
		const response = await fetch(`${PUBLIC_API_URL}/users`, {
			headers: {
				Authorization: `Bearer ${cookies.get('access')}`
			}
		});

		if (!response.ok) {
			console.log('Error retrieving user.');
			return null;
		}

		return await response.json();
	};

	const fetchPendingOrders = async (): Promise<OrderOut[]> => {
		const response = await fetch(`${PUBLIC_API_URL}/orders`, {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${cookies.get('access')}`
			}
		});

		if (!response.ok) {
			console.log('Error retrieving orders.');
			return [];
		}

		const orders: OrderOut[] = await response.json();
		return orders.filter((order) => order.status === 'PENDING');
	};

	return {
		user: fetchUser(),
		pendingOrders: fetchPendingOrders()
	};
};
