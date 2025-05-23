<script lang="ts">
	import MasonryLayout from '$lib/components/masonry/MasonryLayout.svelte';
	import type { PageData } from './$types';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();
</script>

<div class="wrapper">
	{#await data.products}
		<MasonryLayout />
	{:then products}
		<MasonryLayout {products} />
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}
</div>

<style>
	.wrapper {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 100%;
		max-width: 2000px;
		margin-right: auto;
		margin-left: auto;
	}
</style>
