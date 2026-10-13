<script lang="ts">
	import { PUBLIC_RECAPTCHA_SITE_KEY } from '$env/static/public';
	import type { ActionResult } from '@sveltejs/kit';
	import type { ActionData, PageData } from './$types';
	import { applyAction, deserialize } from '$app/forms';
	import { invalidateAll } from '$app/navigation';
	import { page } from '$app/state';
	import Button from '$lib/components/shared/Button.svelte';
	import ProductImage from '$lib/components/ProductImage.svelte';
	import { tick } from 'svelte';

	interface Props {
		form: ActionData;
		data: PageData;
	}

	let { form, data }: Props = $props();

	$effect(() => {
		if (data.inquiry?.imageUrl) tick().then(() => window.PinUtils?.build());
	});

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		window.grecaptcha.ready(async () => {
			const token = await window.grecaptcha.execute(PUBLIC_RECAPTCHA_SITE_KEY, {
				action: 'submit'
			});

			const data = new FormData(event.target as HTMLFormElement);

			data.append('token', token);

			const response = await fetch((event.target as HTMLFormElement).action, {
				method: (event.target as HTMLFormElement).method,
				body: data
			});

			const result: ActionResult = deserialize(await response.text());

			if (result.type === 'success') {
				await invalidateAll();
			}

			applyAction(result);
		});
	}
</script>

<svelte:head>
	<script src="https://www.google.com/recaptcha/api.js?render={PUBLIC_RECAPTCHA_SITE_KEY}"></script>
</svelte:head>

<div class="wrapper">
	<h3>
		{data.inquiry
			? 'Interested in purchasing this work? Send me a message.'
			: 'Please contact me if you have any questions or comments'}
	</h3>
	{#if data.inquiry?.imageUrl}
		<div class="inquiry-image">
			<ProductImage
				url={data.inquiry.imageUrl}
				alt={data.inquiry.title}
				data-pin-media={new URL(data.inquiry.imageUrl, page.url).href}
				data-pin-url={new URL(`/products/${data.inquiry.productId}`, page.url).href}
				data-pin-description={data.inquiry.title}
			/>
		</div>
	{/if}
	<form class="wrapper form" method="POST" onsubmit={handleSubmit}>
		{#if form?.success}
			<div>Thank you for your message!</div>
		{:else}
			<div class="form-element">
				<label class="form-label" for="name">Name</label>
				<input
					class="form-control"
					id="name"
					name="name"
					type="text"
					value=""
					placeholder="Your name..."
					required
				/>
			</div>
			<div class="form-element">
				<label class="form-label" for="email">Email</label>
				<input
					class="form-control"
					id="email"
					name="email"
					type="text"
					value=""
					placeholder="Your email..."
					required
				/>
			</div>
			<div class="form-element">
				<label class="form-label" for="message">Message</label>
				<textarea
					class="form-control"
					id="message"
					name="message"
					placeholder="Write something..."
					value={page.url.searchParams.get('message') ?? ''}
					required
				></textarea>
			</div>
			<div class="recaptcha">
				This site is protected by reCAPTCHA and the Google
				<a href="https://policies.google.com/privacy" target="_blank">Privacy Policy</a> and
				<a href="https://policies.google.com/terms" target="_blank">Terms of Service</a> apply.
			</div>
			<Button>Send</Button>
		{/if}
	</form>
</div>

<style>
	.wrapper {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 100%;
		gap: 1rem;
	}

	.form {
		max-width: 500px;
	}

	.inquiry-image {
		display: flex;
		justify-content: center;
		width: 100%;
		max-width: 320px;
		max-height: 320px;
	}

	.inquiry-image :global(img) {
		max-height: 320px;
		object-fit: contain;
	}

	.form-element {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		width: 100%;
	}

	.form-control {
		width: 100%;
		border: 2px solid #666;
		border-radius: 0.34rem;
	}

	.recaptcha {
		font-size: 11px;
	}

	input,
	textarea {
		font-family: inherit;
		font-size: 100%;
		padding: 0.5rem;
	}

	textarea {
		resize: vertical;
		height: 144px;
	}

	:global(.grecaptcha-badge) {
		visibility: hidden;
	}
</style>
