import { PUBLIC_API_URL } from '$env/static/public';
import { fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = ({ url }) => ({ hasToken: Boolean(url.searchParams.get('token')) });

export const actions: Actions = {
	default: async ({ request, url, fetch }) => {
		const token = url.searchParams.get('token');
		if (!token) return fail(400, { resetError: 'This reset link is invalid or has expired.' });

		const formData = await request.formData();
		const password = formData.get('password');
		const confirmation = formData.get('confirmation');
		if (typeof password !== 'string' || password.length < 8 || new TextEncoder().encode(password).length > 72) {
			return fail(400, { resetError: 'Password must be at least 8 characters and no more than 72 bytes.' });
		}
		if (password !== confirmation) return fail(400, { resetError: 'Passwords do not match.' });

		const body = new FormData();
		body.set('password', password);
		try {
			const response = await fetch(`${PUBLIC_API_URL}/reset_password/${encodeURIComponent(token)}`, {
				method: 'POST',
				body
			});
			if (response.status === 401 || response.status === 404) {
				return fail(400, { resetError: 'This reset link is invalid or has expired.' });
			}
			if (!response.ok) return fail(502, { resetError: 'Unable to reset your password. Please try again.' });
		} catch {
			return fail(502, { resetError: 'Unable to reset your password. Please try again.' });
		}

		return { success: true };
	}
};
