<script lang="ts">
	import type { LayoutData } from './$types';
	
	import Sidebar from '$lib/components/Sidebar.svelte';
	import { onNavigate } from '$app/navigation';

	onNavigate((navigation) => {
		if (!document.startViewTransition) return;

		return new Promise((resolve) => {
			document.startViewTransition(async () => {
				resolve();
				await navigation.complete;
			});
		});
	});
	
	export let data: LayoutData;
</script>

<div class="container">
	<Sidebar />

	{#key data.url}
		<main>
			<slot />
		</main>
	{/key}
</div>

<style>
	.container {
		display: flex;
		flex-direction: row;
	}

	main {
		width: 100%;
		display: flex;
		justify-content: center;
		align-items: flex-start;
		margin: 1rem;
		view-transition-name: main;
	}
</style>