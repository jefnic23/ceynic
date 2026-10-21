<script lang="ts">
	import Card from '$lib/components/shared/Card.svelte';
	import Input from '$lib/components/shared/Input.svelte';
	import type { PageData } from './$types';
	import PageContainer from '$lib/components/shared/PageContainer.svelte';

	let { data }: { data: PageData } = $props();
</script>

<PageContainer max="720px">
	<Card width="100%">
		<h1>Account</h1>
		<div class="form-stack fields">
			<Input id="contact-email" label="Contact email" type="email" value={data.user.email} readonly />
			<Input id="first-name" label="First name" value={data.user.firstName ?? ''} readonly />
			<Input id="last-name" label="Last name" value={data.user.lastName ?? ''} readonly />
		</div>
	</Card>
</PageContainer>

<style>
	h1 {
		margin-block: 0 1.5rem;
	}

	.fields {
		gap: 1.5rem;
	}
</style>
