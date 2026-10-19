<script lang="ts">
	import Button from '$lib/components/shared/Button.svelte';
	import Input from '$lib/components/shared/Input.svelte';
	import { enhance } from '$app/forms';
	import type { ActionData } from './$types';
	import Icon from '@iconify/svelte';
	import Modal from '$lib/components/shared/Modal.svelte';
	import AuthLayout from '$lib/components/shared/AuthLayout.svelte';

	interface Props {
		form: ActionData;
	}

	let { form }: Props = $props();
	let showResetModal = $state(false);
</script>

<AuthLayout>
			<h2>Log in</h2>
			<form class="form-stack auth-form" method="POST" action="?/login" use:enhance>
				<div class="field-with-icon">
					<Icon icon="material-symbols:person" />
					<Input id="email" name="username" label="Email" value="" type="email" autocomplete="username" required />
				</div>
				<div class="field-with-icon">
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
			<Button class="text-button" appearance="plain" onclick={() => (showResetModal = true)}>Forgot password?</Button>
</AuthLayout>

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
				<p>Didn't receive an email? <Button type="submit" appearance="plain" class="text-button">Resend the link</Button></p>
			</form>
		{:else}
			<p>Enter your account email and we'll send you a reset link.</p>
			<form method="POST" action="?/requestReset" use:enhance>
				<div class="field-with-icon">
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
