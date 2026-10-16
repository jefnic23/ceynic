import { PUBLIC_API_URL } from '$env/static/public';
import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

interface UserOut {
	email: string;
	firstName: string | null;
	lastName: string | null;
}

export const load: PageServerLoad = async ({ fetch, cookies }) => {
	const response = await fetch(`${PUBLIC_API_URL}/users`, {
		headers: { Authorization: `Bearer ${cookies.get('access')}` }
	});

	if (!response.ok) error(502, 'Unable to load account information.');

	const user: UserOut = await response.json();
	return { user };
};
