<script lang="ts">
	import Card from '$lib/components/shared/Card.svelte';
	import type { Snippet } from 'svelte';
	import PageContainer from '$lib/components/shared/PageContainer.svelte';
	import SettingsTabs from '$lib/components/admin/SettingsTabs.svelte';

	let { children }: { children: Snippet } = $props();
</script>

<PageContainer max="100%">
	<Card width="100%">
		<h1>Settings</h1>
		<SettingsTabs />
		{@render children()}
	</Card>
</PageContainer>
