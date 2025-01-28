import { PUBLIC_API_URL } from '$env/static/public';

export const load = async ({ fetch }) => {
    const fetchAbout = async () => {
        const response = await fetch(`${PUBLIC_API_URL}/storefronts/about`);

        if (response.status !== 200) {
            console.log("Error retrieving about content.");
        }
    
        const responseData = await response.json();

        return responseData;
    }

    return {
        about: fetchAbout()
    }
}