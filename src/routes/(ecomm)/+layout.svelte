<script lang="ts">
	import { PUBLIC_MEASUREMENT_ID } from "$env/static/public";
	import { page } from '$app/state';
	import type { PageData } from './$types';
	import Footer from '$lib/components/Footer.svelte';
	import { onNavigate } from '$app/navigation';
	import EcommHeader from '$lib/components/ecomm/EcommHeader.svelte';
	import GoogleAnalytics from '$lib/components/GoogleAnalytics.svelte';
	import type { SocialMediaLink } from "$lib/interfaces/socialMediaLink";

	onNavigate((navigation) => {
		if (!document.startViewTransition) return;

		return new Promise((resolve) => {
			document.startViewTransition(async () => {
				resolve();
				await navigation.complete;
			});
		});
	});

	interface Props {
		data: PageData;
		children?: import('svelte').Snippet;
	}

	let { data, children }: Props = $props();

	let namePromise: Promise<string> = data.name;
	let name: string = $state("");

	$effect(() => {
		if (namePromise) {
			namePromise.then((value) => {
				name = value;
			});
		}
	});

	let socialMediaLinkPromise: Promise<SocialMediaLink[]> = data.socialMediaLinks;
	let socialMediaLinks: SocialMediaLink[] = $state([]);

	$effect(() => {
		if (socialMediaLinkPromise) {
			socialMediaLinkPromise.then((value) => {
				socialMediaLinks = value;
			});
		}
	});
</script>

<GoogleAnalytics measurementId={PUBLIC_MEASUREMENT_ID} />

<div class="wrapper">
	<EcommHeader url={page.url} name={name} />

	{#key data.url}
		<main>
			{@render children?.()}
		</main>
	{/key}

	<Footer copyright={name} socialMediaLinks={socialMediaLinks} />
</div>

<style>
	main {
		position: relative;
		display: flex;
		justify-content: center;
		flex: 1;
		padding: 2rem;
	}

	.wrapper {
		min-height: 100svh;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}
</style>
