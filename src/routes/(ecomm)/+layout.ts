import { PUBLIC_API_URL } from '$env/static/public'
import { PaymentProcessor } from '$lib/enums/paymentProcessor';
import type { SocialMediaLinkOut } from '$lib/interfaces/SocialMediaLinkOut';
import type { SiteSettings } from '$lib/interfaces/SiteSettings';
import { error } from '@sveltejs/kit';

export const load = async ({ url, fetch }) => {
    const fetchName = async (): Promise<string> => {
        const response = await fetch(`${PUBLIC_API_URL}/storefronts/name`);

        if (!response.ok) {
            console.log("Error retrieving storefront name.");
            return "";
        }

        const responseData: string = await response.json();

        return responseData;
    }

    const fetchSocialMediaLinks = async (): Promise<SocialMediaLinkOut[]> => {
        const response = await fetch(`${PUBLIC_API_URL}/socialMediaLinks`);

        if (!response.ok) {
            console.log("Error retrieving social media links.");
            return [];
        }

        const responseData: SocialMediaLinkOut[] = await response.json();

        return responseData;
    }

    const fetchPinterestEnabled = async (): Promise<boolean> => {
        const response = await fetch(`${PUBLIC_API_URL}/settings/siteSettings`);

        if (!response.ok) {
            console.log('Error retrieving site settings.');
            return false;
        }

        const settings: SiteSettings = await response.json();
        return settings.pinterestEnabled === true;
    }

    const fetchPaymentProcessor = async (): Promise<PaymentProcessor | null> => {
        const response = await fetch(`${PUBLIC_API_URL}/settings/paymentProcessor`);

        if (!response.ok) error(502, 'Unable to load payment processor.');

        const processor: unknown = await response.json();
        if (processor !== null && !Object.values(PaymentProcessor).includes(processor as PaymentProcessor)) {
            error(502, 'Invalid payment processor response.');
        }

        return processor as PaymentProcessor | null;
    }

    return {
        url: url.pathname,
        name: fetchName(),
        socialMediaLinks: fetchSocialMediaLinks(),
        pinterestEnabled: fetchPinterestEnabled(),
        paymentProcessor: await fetchPaymentProcessor()
    }
}
