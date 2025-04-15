import { redirect, type Handle } from '@sveltejs/kit';
import { handleRefresh } from '$lib/server/auth';

export const handle: Handle = async ({ event, resolve }) => {
	if (event.url.pathname.startsWith('/admin')) {
		const accessToken = event.cookies.get("access");
		const refreshToken = event.cookies.get("refresh");

		if (!accessToken && !refreshToken) {
			throw redirect(303, '/login');
		}

		// If access token is missing, attempt a refresh if refresh token is available
		if (!accessToken && refreshToken) {
			const attemptRefresh = await handleRefresh(event.cookies);
			if (attemptRefresh) {
				event.locals.user = "me";
			} else {
				throw redirect(303, '/login');
			}
		}

		// Either access token exists or refresh was successful
		// return await resolve(event);
	}

	return await resolve(event);
};