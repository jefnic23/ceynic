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

    const fetchSiteSettings = async (): Promise<SiteSettings> => {
        const response = await fetch(`${PUBLIC_API_URL}/settings/siteSettings`);

        if (!response.ok) {
            console.log('Error retrieving site settings.');
            return { pinterestEnabled: false, sortAndFilterEnabled: true };
        }

        return await response.json();
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

    const siteSettings = fetchSiteSettings();

    return {
        url: url.pathname,
        name: fetchName(),
        socialMediaLinks: fetchSocialMediaLinks(),
        pinterestEnabled: siteSettings.then(settings => settings.pinterestEnabled === true),
        sortAndFilterEnabled: siteSettings.then(settings => settings.sortAndFilterEnabled !== false),
        paymentProcessor: await fetchPaymentProcessor()
    }
}
