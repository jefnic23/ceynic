import { PUBLIC_API_URL } from '$env/static/public';
import { error, fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

interface UserOut {
	email: string;
	firstName: string | null;
	lastName: string | null;
}

interface AboutContent {
	about: string;
}

const aboutEndpoint = `${PUBLIC_API_URL}/settings/about`;

export const load: PageServerLoad = async ({ fetch, cookies }) => {
	const headers = { Authorization: `Bearer ${cookies.get('access')}` };
	const [userResponse, aboutResponse] = await Promise.all([
		fetch(`${PUBLIC_API_URL}/users`, { headers }),
		fetch(aboutEndpoint, { headers })
	]);

	if (!userResponse.ok) error(502, 'Unable to load account information.');
	if (!aboutResponse.ok) error(502, 'Unable to load About page content.');

	const user: UserOut = await userResponse.json();
	const aboutContent: AboutContent = await aboutResponse.json();
	if (typeof aboutContent.about !== 'string') error(502, 'Invalid About page content response.');
	return { user, about: aboutContent.about };
};

export const actions: Actions = {
	default: async ({ request, fetch, cookies }) => {
		const formData = await request.formData();
		const about = formData.get('about');
		if (typeof about !== 'string') {
			return fail(400, { message: 'Invalid About page content.', about: '' });
		}
		if (about.length > 50_000) {
			return fail(400, {
				message: 'About page content must be 50,000 characters or fewer.',
				about
			});
		}
		if (about.toLowerCase().includes('blob:')) {
			return fail(400, {
				message: 'Image uploads are not available. Replace blob URLs with public image URLs.',
				about
			});
		}

		try {
			const response = await fetch(aboutEndpoint, {
				method: 'PUT',
				headers: {
					Authorization: `Bearer ${cookies.get('access')}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ about })
			});

			if (!response.ok) {
				return fail(502, { message: 'Unable to save About page content.', about });
			}
		} catch {
			return fail(502, { message: 'Unable to save About page content.', about });
		}

		return { success: true };
	}
};
