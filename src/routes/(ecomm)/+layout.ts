import { PUBLIC_API_URL } from '$env/static/public'
import type { SocialMediaLinkOut } from '$lib/interfaces/SocialMediaLinkOut';
import type { SiteSettings } from '$lib/interfaces/SiteSettings';

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

    return {
        url: url.pathname,
        name: fetchName(),
        socialMediaLinks: fetchSocialMediaLinks(),
        pinterestEnabled: fetchPinterestEnabled()
    }
}
