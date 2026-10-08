import { error, fail } from '@sveltejs/kit';
import type { RequestEvent } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { PUBLIC_API_URL } from '$env/static/public';
import * as z from 'zod';
import * as ProductForCreate from '$lib/schemas/ProductForCreate.json';
import * as ProductForUpdate from '$lib/schemas/ProductForUpdate.json';

const ProductToCreate = z.fromJSONSchema(
	ProductForCreate as z.core.JSONSchema.JSONSchema
);
const ProductToUpdate = z.fromJSONSchema(
	ProductForUpdate as z.core.JSONSchema.JSONSchema
);

export const load: PageServerLoad = async () => {};

async function submitProduct({ request, cookies }: RequestEvent, method: 'POST' | 'PUT') {
	const productData = await request.formData();
	const product = {
		title: productData.get('title'),
		description: productData.get('description') || null,
		price: productData.get('price'),
		mediumId: Number(productData.get('medium_id')),
		height: Number(productData.get('height')),
		width: Number(productData.get('width')),
		enabled: productData.has('enabled'),
		images: productData
			.getAll('images')
			.filter((image): image is File => image instanceof File)
			.map((image) => image.name)
	};
	const validationResult =
		method === 'POST'
			? ProductToCreate.safeParse(product)
			: ProductToUpdate.safeParse({ id: Number(productData.get('id')), ...product });

	if (!validationResult.success) {
		return fail(400, { errors: z.treeifyError(validationResult.error) });
	}

	if (productData.get('filesChanged') !== 'true') productData.delete('images');

	productData.delete('filesChanged');

	const endpoint =
		method === 'POST'
			? `${PUBLIC_API_URL}/products`
			: `${PUBLIC_API_URL}/products/${productData.get('id')}`;

	const response = await fetch(endpoint, {
		method,
		headers: {
			Authorization: `Bearer ${cookies.get('access')}`
		},
		body: productData
	});

	if (!response.ok) {
		const details = await response.text();
		console.error('Product API error:', response.status, details);
		error(500, `Error ${method === 'POST' ? 'creating' : 'updating'} product.`);
	}

	return { success: true };
}

export const actions: Actions = {
	create: (event) => submitProduct(event, 'POST'),
	update: (event) => submitProduct(event, 'PUT')
};
