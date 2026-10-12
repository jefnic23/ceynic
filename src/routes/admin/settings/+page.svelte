<script lang="ts">
	import { useToast } from '$lib/state/toast';
	import type { ActionData, PageData } from './$types';

	let { data, form }: { data: PageData; form: ActionData } = $props();
	const showToast = useToast();

	$effect(() => {
		if (form?.message) {
			showToast({ type: 'error', title: 'Site settings not saved', message: form.message });
		} else if (form?.success) {
			showToast({
				type: 'success',
				title: 'Site settings saved',
				message: 'Your site settings have been updated.'
			});
		}
	});
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
