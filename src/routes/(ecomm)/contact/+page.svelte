<script lang="ts">
	import { PUBLIC_RECAPTCHA_SITE_KEY } from '$env/static/public';
	import type { ActionData, PageData } from './$types';
	import { page } from '$app/state';
	import PageContainer from '$lib/components/shared/PageContainer.svelte';
	import ProductImage from '$lib/components/ProductImage.svelte';
	import ContactForm from '$lib/components/ecomm/ContactForm.svelte';

	let { form, data }: { form: ActionData; data: PageData } = $props();
</script>

<svelte:head>
	<script src="https://www.google.com/recaptcha/api.js?render={PUBLIC_RECAPTCHA_SITE_KEY}"></script>
</svelte:head>

<PageContainer max="100%">
	<div class="contact-page">
		<h3>{data.inquiry ? 'Interested in purchasing this work? Send me a message.' : 'Please contact me if you have any questions or comments'}</h3>
		{#if data.inquiry?.imageUrl}
			<div class="inquiry-image">
				<ProductImage url={data.inquiry.imageUrl} alt={data.inquiry.title} data-pin-no-hover="true" data-pin-nopin="true" />
			</div>
		{/if}
		<ContactForm success={form?.success} message={page.url.searchParams.get('message') ?? ''} />
	</div>
</PageContainer>

<style>
	.contact-page { display: flex; flex-direction: column; align-items: center; gap: 1rem; inline-size: 100%; }
	.inquiry-image { display: flex; justify-content: center; inline-size: 100%; max-inline-size: 320px; max-block-size: 320px; }
	.inquiry-image :global(img) { max-block-size: 320px; object-fit: contain; }
</style>
