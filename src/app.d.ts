// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		interface Locals {
			user: string | null
		}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
	
	interface Window {
		dataLayer: IArguments[];
		grecaptcha: {
			ready: (callback: () => void) => void;
			execute: (siteKey: string, options: { action: string }) => Promise<string>;
		};
		gtag?: (...args: unknown[]) => void;
	}
}

export {};
