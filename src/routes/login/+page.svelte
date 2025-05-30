<script lang="ts">
	import Button from '$lib/components/shared/Button.svelte';
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
					<input id="email" name="username" value="" placeholder="Email" type="email" required />
				</div>
				<div class="input-container">
					<Icon icon="material-symbols:lock" />
					<input
						id="password"
						name="password"
						value=""
						placeholder="Password"
						type="password"
						required
					/>
				</div>
				<!-- {#if form?.invalid}
					<p class="error">Username and password is required.</p>
				{/if} -->
	
				{#if form?.credentials}
					<p class="error">You have entered the wrong credentials.</p>
				{/if}
				<Button>Submit</Button>
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
		border-bottom: 2px solid #ccc;
		width: 89%;
	}

	input {
		flex-grow: 1;
		padding: 0.5rem 0;
		border: none;
		outline: none;
		background-color: transparent;
		margin-left: 0.5em;
	}

	input::placeholder {
		color: #aaa;
	}

	input:-webkit-autofill,
	input:-webkit-autofill:hover,
	input:-webkit-autofill:focus {
		-webkit-box-shadow: 0 0 0px 1000px white inset !important;
		box-shadow: 0 0 0px 1000px white inset !important;
		-webkit-text-fill-color: #000 !important;
	}

	.input-container:focus-within {
		border-bottom-color: #007bff; /* Change this to your desired color */
	}
</style>
