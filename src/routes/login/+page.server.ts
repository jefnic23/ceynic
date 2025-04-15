import { redirect, fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { handleLogin } from '$lib/server/auth';

export const load: PageServerLoad = async () => {}

export const actions: Actions = {
    default: async (event) => {
        const result = await handleLogin(event);

        if (result.success) {
            redirect(302, "/admin");
        } else {
            return fail(401, { credentials: true });
        }
    }
} 