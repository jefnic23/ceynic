import { PUBLIC_API_URL } from '$env/static/public';
import type { OrderOut } from '$lib/interfaces/OrderOut';
import type { PageServerLoad } from './$types';

interface UserOut {
	email: string;
	firstName: string | null;
	lastName: string | null;
}

function ordersByMonth(orders: OrderOut[]) {
	const now = new Date();
	const monthFormatter = new Intl.DateTimeFormat('en-US', { month: 'short', year: 'numeric', timeZone: 'UTC' });
	const months = Array.from({ length: 6 }, (_, index) => {
		const date = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() - 5 + index, 1));
		return {
			key: date.getUTCFullYear() * 12 + date.getUTCMonth(),
			label: monthFormatter.format(date),
			count: 0
		};
	});
	const monthsByKey = new Map(months.map((month) => [month.key, month]));

	for (const order of orders) {
		const created = new Date(order.createTime);
		const month = monthsByKey.get(created.getUTCFullYear() * 12 + created.getUTCMonth());
		if (month) month.count += 1;
	}

	return months.map(({ label, count }) => ({ label, count }));
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

	const fetchOrders = async (): Promise<OrderOut[]> => {
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

		return await response.json();
	};

	const orders = fetchOrders();

	return {
		user: fetchUser(),
		pendingOrders: orders.then((items) => items.filter((order) => order.status === 'PENDING')),
		monthlyOrders: orders.then(ordersByMonth)
	};
};
