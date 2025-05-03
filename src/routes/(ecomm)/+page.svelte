<script lang="ts">
	import MasonryLayout from '$lib/components/masonry/MasonryLayout.svelte';
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<div class="wrapper">
	{#await data.products}
		<MasonryLayout />
	{:then products} 
		<MasonryLayout products={products} />
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
		margin-right: auto;
		margin-left: auto;
	}
</style>
