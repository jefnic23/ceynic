<script lang="ts">
	import Card from '$lib/components/shared/Card.svelte';
	import type { ActionData, PageData } from './$types';

	let { data, form }: { data: PageData; form: ActionData } = $props();
</script>

<div class="wrapper">
	<Card width="100%">
		<h1>Settings</h1>
		<form method="POST">
			<label>
				<input
					type="checkbox"
					name="pinterestEnabled"
					checked={form?.pinterestEnabled ?? data.pinterestEnabled}
				/>
				Enable Pinterest save buttons on the storefront
			</label>
			<button type="submit">Save settings</button>
			{#if form?.message}
				<p role="alert">{form.message}</p>
			{:else if form?.success}
				<p role="status">Settings saved.</p>
			{/if}
		</form>
	</Card>
</div>

<style>
	.wrapper {
		width: 100%;
	}

	form {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 1rem;
	}

	label {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}
</style>
