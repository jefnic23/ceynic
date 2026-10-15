import { PUBLIC_API_URL } from '$env/static/public';
import type { OrderDetails } from '$lib/interfaces/OrderDetails';
import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params }) => {
	const response = await fetch(`${PUBLIC_API_URL}/orders/${encodeURIComponent(params.orderId)}`);

	if (response.status === 404) error(404, 'Order not found.');
	if (!response.ok) error(502, 'Unable to load order details.');

	return { order: (await response.json()) as OrderDetails };
};
