import { redirect, fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { handleLogin } from '$lib/server/auth';
import { PUBLIC_API_URL } from '$env/static/public';

export const load: PageServerLoad = async () => {}

export const actions: Actions = {
    login: async (event) => {
        const result = await handleLogin(event);

        if (result.success) {
            redirect(302, "/admin");
        } else {
            return fail(401, { credentials: true });
        }
    },
    requestReset: async ({ request, fetch }) => {
        const formData = await request.formData();
        const email = formData.get('email');
        const isResend = formData.get('resend') === 'true';
        if (typeof email !== 'string' || !email.trim()) {
            return fail(400, { resetRequested: isResend, email: '', resetError: 'Enter your email address.' });
        }

        const resetEmail = email.trim();
        const body = new FormData();
        body.set('email', resetEmail);

        try {
            const response = await fetch(`${PUBLIC_API_URL}/reset_password`, {
                method: 'POST',
                body
            });
            if (!response.ok) return fail(502, { resetRequested: isResend, email: resetEmail, resetError: 'Unable to send the reset email. Please try again.' });
        } catch {
            return fail(502, { resetRequested: isResend, email: resetEmail, resetError: 'Unable to send the reset email. Please try again.' });
        }

        return { resetRequested: true, email: resetEmail };
    }
}
