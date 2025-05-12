import { PUBLIC_API_URL } from '$env/static/public'
import type { SocialMediaLink } from '$lib/interfaces/socialMediaLink.js';

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

    const fetchSocialMediaLinks = async (): Promise<SocialMediaLink[]> => {
        const response = await fetch(`${PUBLIC_API_URL}/socialMediaLinks`);

        if (!response.ok) {
            console.log("Error retrieving social media links.");
            return [];
        }

        const responseData: SocialMediaLink[] = await response.json();

        return responseData;
    }

    return {
        url: url.pathname,
        name: fetchName(),
        socialMediaLinks: fetchSocialMediaLinks()
    }
}
