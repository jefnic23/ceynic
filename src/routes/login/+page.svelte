<script lang="ts">
	import Button from '$lib/components/shared/Button.svelte';
	import Input from '$lib/components/shared/Input.svelte';
	import { enhance } from '$app/forms';
	import type { ActionData } from './$types';
	import Card from '$lib/components/shared/Card.svelte';
	import Icon from '@iconify/svelte';
	import Modal from '$lib/components/shared/Modal.svelte';

	interface Props {
		form: ActionData;
	}

	let { form }: Props = $props();
	let showResetModal = $state(false);
</script>

<div class="wrapper">
	<Card>
		<div class="body">
			<h2>Log in</h2>
			<form method="POST" action="?/login" use:enhance>
				<div class="input-container">
					<Icon icon="material-symbols:person" />
					<Input id="email" name="username" label="Email" value="" type="email" autocomplete="username" required />
				</div>
				<div class="input-container">
					<Icon icon="material-symbols:lock" />
					<Input id="password" label="Password" value="" type="password" autocomplete="current-password" required />
				</div>
				<!-- {#if form?.invalid}
					<p class="error">Username and password is required.</p>
				{/if} -->
	
				{#if form?.credentials}
					<p class="error">You have entered the wrong credentials.</p>
				{/if}
				<Button type="submit">Submit</Button>
			</form>
			<Button class="forgot-password" appearance="plain" onclick={() => (showResetModal = true)}>Forgot password?</Button>
		</div>
	</Card>
</div>

{#if showResetModal}
	<Modal bind:showModal={showResetModal} title="Reset your password">
		{#if form?.resetRequested}
			<p>If an account exists for that email, you'll receive a password reset link shortly.</p>
			{#if form?.resetError}
				<p class="error">{form.resetError}</p>
			{/if}
			<form method="POST" action="?/requestReset" use:enhance>
				<input type="hidden" name="email" value={form.email} />
				<input type="hidden" name="resend" value="true" />
				<p class="resend-prompt">Didn't receive an email? <Button type="submit" appearance="plain">Resend the link</Button></p>
			</form>
		{:else}
			<p>Enter your account email and we'll send you a reset link.</p>
			<form method="POST" action="?/requestReset" use:enhance>
				<div class="input-container">
					<Input id="reset-email" name="email" label="Email" value="" type="email" autocomplete="email" required />
				</div>
				{#if form?.resetError}
					<p class="error">{form.resetError}</p>
				{/if}
				<Button type="submit">Send reset link</Button>
			</form>
		{/if}
	</Modal>
{/if}


<style>
	.wrapper {
		display: flex;
		width: fit-content;
		height: 100vh;
		margin: auto;
		align-items: center;
	}

	.body {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 377px;
	}

	form {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 100%;
		margin-bottom: 0.83em;
	}

	.input-container {
		display: flex;
		align-items: center;
		margin-bottom: 1rem;
		gap: 0.5rem;
		width: 100%;
	}

	.resend-prompt :global(button),
	.body :global(button.forgot-password) {
		color: #0066cc;
		text-decoration: underline;
		text-underline-offset: 2px;
		cursor: pointer;
	}

	.resend-prompt :global(button:hover),
	.body :global(button.forgot-password:hover) {
		color: #004b99;
	}

	.resend-prompt :global(button:focus-visible),
	.body :global(button.forgot-password:focus-visible) {
		outline: 2px solid #0066cc;
		outline-offset: 2px;
	}
</style>
