import type { LayoutServerLoad } from "./$types"
import { getTokenExpiry } from '$lib/server/auth';

export const load: LayoutServerLoad = async ({ url, locals, cookies }) => {
	return {
		url: url.pathname,
		user: locals.user,
		refreshExpiresAt: getTokenExpiry(cookies.get('refresh')),
	}
}
