<script lang="ts">
	import { PUBLIC_RECAPTCHA_SITE_KEY } from '$env/static/public';
	import type { ActionResult } from '@sveltejs/kit';
	import { applyAction, deserialize } from '$app/forms';
	import { invalidateAll } from '$app/navigation';
	import Button from '$lib/components/shared/Button.svelte';

	let { success, message }: { success?: boolean; message: string } = $props();

	async function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		window.grecaptcha.ready(async () => {
			const token = await window.grecaptcha.execute(PUBLIC_RECAPTCHA_SITE_KEY, { action: 'submit' });
			const form = event.target as HTMLFormElement;
			const data = new FormData(form);
			data.append('token', token);
			const response = await fetch(form.action, { method: form.method, body: data });
			const result: ActionResult = deserialize(await response.text());
			if (result.type === 'success') await invalidateAll();
			applyAction(result);
		});
	}
</script>

<form class="form-stack" method="POST" onsubmit={handleSubmit}>
	{#if success}
		<div>Thank you for your message!</div>
	{:else}
		<div class="form-element"><label for="name">Name</label><input id="name" name="name" type="text" value="" placeholder="Your name..." required /></div>
		<div class="form-element"><label for="email">Email</label><input id="email" name="email" type="email" value="" placeholder="Your email..." required /></div>
		<div class="form-element"><label for="message">Message</label><textarea id="message" name="message" placeholder="Write something..." value={message} required></textarea></div>
		<div class="recaptcha">This site is protected by reCAPTCHA and the Google <a href="https://policies.google.com/privacy" target="_blank">Privacy Policy</a> and <a href="https://policies.google.com/terms" target="_blank">Terms of Service</a> apply.</div>
		<Button type="submit">Send</Button>
	{/if}
</form>

<style>
	form { max-inline-size: 500px; align-items: center; }
	.form-element { display: flex; flex-direction: column; align-items: flex-start; inline-size: 100%; }
	:is(input, textarea) { inline-size: 100%; padding: 0.5rem; border: 2px solid var(--ink-muted); border-radius: 0.34rem; font: inherit; }
	textarea { resize: vertical; block-size: 144px; }
	.recaptcha { font-size: 11px; }
	:global(.grecaptcha-badge) { visibility: hidden; }
</style>
