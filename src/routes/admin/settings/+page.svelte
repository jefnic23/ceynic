<script lang="ts">
	import Button from '$lib/components/shared/Button.svelte';
	import Checkbox from '$lib/components/shared/Checkbox.svelte';
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

<form class="form-stack" method="POST">
	<Checkbox name="pinterestEnabled" label="Enable Pinterest save buttons on the storefront" checked={form?.pinterestEnabled ?? data.pinterestEnabled} />
	<Checkbox name="sortAndFilterEnabled" label="Enable sort and filter options on the storefront" checked={form?.sortAndFilterEnabled ?? data.sortAndFilterEnabled} />
	<Button type="submit">Save site settings</Button>
</form>
