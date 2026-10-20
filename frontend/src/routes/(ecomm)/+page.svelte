<script lang="ts">
	import MasonryLayout from '$lib/components/masonry/MasonryLayout.svelte';
	import type { PageData } from './$types';
	import PageContainer from '$lib/components/shared/PageContainer.svelte';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();
</script>

<PageContainer max="2000px">
	{#await data.products}
		<MasonryLayout />
	{:then products}
		<MasonryLayout {products} />
	{:catch error}
		<p class="error" role="alert">{error.message}</p>
	{/await}
</PageContainer>

<style>
	.error { color: var(--danger); }
</style>
