<script lang="ts">
	import Button from '$lib/components/shared/Button.svelte';
	import Input from '$lib/components/shared/Input.svelte';
	import { enhance } from '$app/forms';
	import type { ActionData } from './$types';
	import Card from '$lib/components/shared/Card.svelte';
	import Icon from '@iconify/svelte';

	interface Props {
		form: ActionData;
	}

	let { form }: Props = $props();
</script>

<div class="wrapper">
	<Card>
		<div class="body">
			<h2>Log in</h2>
			<form method="POST" use:enhance>
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
		</div>
	</Card>
</div>


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
	}

	.input-container {
		display: flex;
		align-items: center;
		margin-bottom: 1rem;
		gap: 0.5rem;
		width: 89%;
	}
</style>
