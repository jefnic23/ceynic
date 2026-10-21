import { PUBLIC_API_URL } from '$env/static/public';
import { PaymentProcessor } from '$lib/enums/paymentProcessor';
import { error, fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

const selectionEndpoint = `${PUBLIC_API_URL}/settings/paymentProcessor`;
const configuredEndpoint = `${PUBLIC_API_URL}/settings/paymentProcessorSettings`;
const paypalEndpoint = `${configuredEndpoint}/${encodeURIComponent(PaymentProcessor.PAYPAL)}`;

export const load: PageServerLoad = async ({ fetch, cookies }) => {
	const headers = { Authorization: `Bearer ${cookies.get('access')}` };
	const [selectionResponse, configuredResponse] = await Promise.all([
		fetch(selectionEndpoint, { headers }),
		fetch(configuredEndpoint, { headers })
	]);

	if (!selectionResponse.ok || !configuredResponse.ok) {
		error(502, 'Unable to load payment settings.');
	}

	const processor: unknown = await selectionResponse.json();
	const configured: unknown = await configuredResponse.json();
	if (
		(processor !== null && processor !== PaymentProcessor.PAYPAL) ||
		typeof configured !== 'object' ||
		configured === null ||
		!('processors' in configured) ||
		!Array.isArray(configured.processors)
	) {
		error(502, 'Invalid payment settings response.');
	}

	return {
		processor,
		paypalConfigured: configured.processors.includes(PaymentProcessor.PAYPAL)
	};
};

export const actions: Actions = {
	default: async ({ request, fetch, cookies }) => {
		const formData = await request.formData();
		const processor = formData.get('processor');
		if (processor !== 'None' && processor !== PaymentProcessor.PAYPAL) {
			return fail(400, { message: 'Select a valid payment processor.' });
		}

		const clientId = formData.get('client_id') ?? '';
		const clientSecret = formData.get('client_secret') ?? '';
		if (typeof clientId !== 'string' || typeof clientSecret !== 'string') {
			return fail(400, { message: 'Invalid PayPal credentials.', processor });
		}

		const id = clientId.trim();
		const secret = clientSecret.trim();
		const headers = {
			Authorization: `Bearer ${cookies.get('access')}`,
			'Content-Type': 'application/json'
		};

		let credentialsSaved = false;
		try {
			if (processor === PaymentProcessor.PAYPAL) {
				const configuredResponse = await fetch(configuredEndpoint, { headers });
				if (!configuredResponse.ok) {
					return fail(502, { message: 'Unable to check PayPal settings.', processor, clientId });
				}

				const configured = await configuredResponse.json();
				if (!Array.isArray(configured?.processors)) {
					return fail(502, { message: 'Invalid PayPal settings response.', processor, clientId });
				}
				const paypalConfigured = configured.processors.includes(PaymentProcessor.PAYPAL);
				if (!paypalConfigured || id || secret) {
					if (!id || !secret) {
						return fail(400, {
							message: 'Enter both PayPal client ID and client secret.',
							processor,
							clientId
						});
					}

					const credentialsResponse = await fetch(paypalEndpoint, {
						method: 'PUT',
						headers,
						body: JSON.stringify({ client_id: id, client_secret: secret })
					});
					if (!credentialsResponse.ok) {
						return fail(502, { message: 'Unable to save PayPal credentials.', processor, clientId });
					}
					credentialsSaved = true;
				}
			}

			const response = await fetch(selectionEndpoint, {
				method: 'PUT',
				headers,
				body: JSON.stringify({ processor: processor === 'None' ? null : processor })
			});
			if (!response.ok) {
				return fail(502, {
					message: credentialsSaved
						? 'PayPal credentials were saved, but the payment processor could not be selected.'
						: 'Unable to select payment processor.',
					processor,
					clientId
				});
			}
		} catch {
			return fail(502, {
				message: credentialsSaved
					? 'PayPal credentials were saved, but the payment processor could not be selected.'
					: 'Unable to save payment settings.',
				processor,
				clientId
			});
		}

		return { success: true };
	}
};
