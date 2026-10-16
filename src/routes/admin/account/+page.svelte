<script lang="ts">
	import Card from '$lib/components/shared/Card.svelte';
	import Input from '$lib/components/shared/Input.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<div class="wrapper">
	<Card width="100%">
		<h1>Account</h1>
		<div class="fields">
			<Input id="contact-email" label="Contact email" type="email" value={data.user.email} readonly />
			<Input id="first-name" label="First name" value={data.user.firstName ?? ''} readonly />
			<Input id="last-name" label="Last name" value={data.user.lastName ?? ''} readonly />
		</div>
	</Card>
</div>

<style>
	.wrapper {
		width: 100%;
		max-width: 720px;
	}

	h1 {
		margin: 0 0 1.5rem;
	}

	.fields {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}
</style>
