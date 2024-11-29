import type { Writable } from "svelte/store";
import { writable } from "svelte/store";
import { PUBLIC_API_URL } from "$env/static/public";

export async function getUser(accessToken: string): Promise<string | null> {
    const response = await fetch(`${PUBLIC_API_URL}/users`, {
        headers: {
            Authorization: `Bearer ${accessToken}`,
        },
    });

    if (response.status == 200) {
        const user: string = await response.json();
        return user.split("@")[0];
    } else if (response.status == 401) {
        console.log("Username or password incorrect.");
    } else {
        console.log("Error logging in.");
    }

    return null;
}

export const user: Writable<string | null> = writable(null);
