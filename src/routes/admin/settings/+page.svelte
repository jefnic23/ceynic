<script lang="ts">
	import type { ActionData, PageData } from './$types';

	let { data, form }: { data: PageData; form: ActionData } = $props();
</script>

<form method="POST">
	<label>
		<input
			type="checkbox"
			name="pinterestEnabled"
			checked={form?.pinterestEnabled ?? data.pinterestEnabled}
		/>
		Enable Pinterest save buttons on the storefront
	</label>
	<label>
		<input
			type="checkbox"
			name="sortAndFilterEnabled"
			checked={form?.sortAndFilterEnabled ?? data.sortAndFilterEnabled}
		/>
		Enable sort and filter options on the storefront
	</label>
	<button type="submit">Save site settings</button>
	{#if form?.message}
		<p role="alert">{form.message}</p>
	{:else if form?.success}
		<p role="status">Site settings saved.</p>
	{/if}
</form>

<style>
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
