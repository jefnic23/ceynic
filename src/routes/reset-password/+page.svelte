<script lang="ts">
	import { enhance } from '$app/forms';
	import Button from '$lib/components/shared/Button.svelte';
	import AuthLayout from '$lib/components/shared/AuthLayout.svelte';
	import Input from '$lib/components/shared/Input.svelte';
	import type { ActionData, PageData } from './$types';

	let { data, form }: { data: PageData; form: ActionData } = $props();
</script>

<svelte:head>
	<title>Reset password</title>
	<meta name="referrer" content="no-referrer" />
</svelte:head>

<AuthLayout>
			<h2>Reset password</h2>
			{#if form?.success}
				<p>Your password has been reset.</p>
				<a href="/login">Log in</a>
			{:else if !data.hasToken}
				<p>This reset link is invalid or has expired.</p>
				<a href="/login">Request another link</a>
			{:else}
				<p>Enter a new password for your account.</p>
				<form class="form-stack auth-form" method="POST" use:enhance>
					<Input id="password" label="New password" type="password" value="" autocomplete="new-password" required />
					<Input id="confirmation" label="Confirm password" type="password" value="" autocomplete="new-password" required />
					{#if form?.resetError}
						<p class="error">{form.resetError}</p>
						{#if form.resetError.includes('invalid or has expired')}
							<a href="/login">Request another link</a>
						{/if}
					{/if}
					<Button type="submit">Reset password</Button>
				</form>
			{/if}
</AuthLayout>

<style>
	h2 {
		margin-block: 0;
	}

	.error {
		color: var(--danger);
	}
</style>
