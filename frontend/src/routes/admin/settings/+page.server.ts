import { PUBLIC_API_URL } from '$env/static/public';
import type { SiteSettings } from '$lib/interfaces/SiteSettings';
import { error, fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

const endpoint = `${PUBLIC_API_URL}/settings/siteSettings`;

export const load: PageServerLoad = async ({ fetch, cookies }) => {
	const response = await fetch(endpoint, {
		headers: { Authorization: `Bearer ${cookies.get('access')}` }
	});

	if (!response.ok) error(502, 'Unable to load site settings.');

	const settings: SiteSettings = await response.json();
	if (typeof settings.pinterestEnabled !== 'boolean' || typeof settings.sortAndFilterEnabled !== 'boolean') {
		error(502, 'Invalid site settings response.');
	}

	return { pinterestEnabled: settings.pinterestEnabled, sortAndFilterEnabled: settings.sortAndFilterEnabled };
};

export const actions: Actions = {
	default: async ({ request, fetch, cookies }) => {
		const formData = await request.formData();
		const pinterestEnabled = formData.has('pinterestEnabled');
		const sortAndFilterEnabled = formData.has('sortAndFilterEnabled');

		try {
			const response = await fetch(endpoint, {
				method: 'PUT',
				headers: {
					Authorization: `Bearer ${cookies.get('access')}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ pinterestEnabled, sortAndFilterEnabled })
			});

			if (!response.ok) {
				return fail(502, { message: 'Unable to save site settings.', pinterestEnabled, sortAndFilterEnabled });
			}
		} catch {
			return fail(502, { message: 'Unable to save site settings.', pinterestEnabled, sortAndFilterEnabled });
		}

		return { success: true };
	}
};
