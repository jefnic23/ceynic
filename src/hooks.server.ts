import { redirect, type Handle } from '@sveltejs/kit';
import { handleLogout, handleRefresh, isExpired } from '$lib/server/auth';

export const handle: Handle = async ({ event, resolve }) => {
	if (event.url.pathname.startsWith('/admin')) {
		const accessToken = event.cookies.get("access");
		const refreshToken = event.cookies.get("refresh");

		if (!refreshToken || isExpired(refreshToken)) {
			handleLogout(event.cookies);
			throw redirect(303, '/login');
		}

		if (!accessToken || isExpired(accessToken)) {
			let refreshed = false;
			try {
				refreshed = (await handleRefresh(event.cookies)).success;
			} catch {
				// Treat an unavailable refresh endpoint as a failed session refresh.
			}
			if (!refreshed) {
				handleLogout(event.cookies);
				throw redirect(303, '/login');
			}
		}

		event.locals.user = 'me';
	}

	return await resolve(event);
};
