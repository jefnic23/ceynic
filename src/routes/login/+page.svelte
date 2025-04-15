<script lang="ts">
	import Modal from '$lib/components/shared/Modal.svelte';
	import Person from '$lib/icons/Person.svelte';
	import Lock from '$lib/icons/Lock.svelte';
	import { createEventDispatcher } from 'svelte';
	import Button from '$lib/components/shared/Button.svelte';
	import { redirect } from '@sveltejs/kit';
	import { enhance } from '$app/forms';
	import type { ActionData } from './$types';

	export let form: ActionData;
</script>

<Modal showModal={true} showClose={false} title="Log In">
	<div class="body">
		<form method="POST" use:enhance>
			<div class="input-container">
				<Person />
				<input id="email" name="username" value="" placeholder="Email" type="email" required />
			</div>
			<div class="input-container">
				<Lock />
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
			<Button text="Submit" />
		</form>
	</div>
</Modal>

<style>
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
