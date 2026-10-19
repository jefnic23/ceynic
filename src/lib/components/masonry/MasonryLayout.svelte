<script lang="ts">
	import Skeleton from '$lib/components/shared/Skeleton.svelte';
	import MasonryItem from '$lib/components/masonry/MasonryItem.svelte';
	import type { ProductOut } from '$lib/interfaces/ProductOut';
	import { onMount, tick } from 'svelte';

	interface Props {
		products?: ProductOut[];
	}

	let { products = [] }: Props = $props();

	onMount(() => {
		if (products.length > 0) tick().then(() => window.PinUtils?.build());
	});

	let loadedImages = $state(new Set<number>());

	function handleImageLoad (id: number) {
		loadedImages.add(id);
		loadedImages = new Set(loadedImages);
	};

	function randomAspectRatio() {
		// Choose ratios between 3:4 (0.75) and 9:16 (0.5625)
		const min = 0.5625;
		const max = 0.75;
		const ratio = Math.random() * (max - min) + min;
		return ratio.toFixed(2);
	}
</script>

<div class="masonry-layout">
	{#if products.length === 0}
		{#each Array(12) as _}
			<div class="masonry-skeleton-item" style="aspect-ratio: 1 / {randomAspectRatio()};">
				<Skeleton />
			</div>
		{/each}
	{:else}
		{#each products as product}
			<MasonryItem
				product={product}
				loaded={loadedImages.has(product.id)}
				load={handleImageLoad}
			/>
		{/each}
	{/if}
</div>

<style>
	.masonry-layout {
		column-gap: 13px;
		column-fill: initial;
		columns: 3 24rem;
		inline-size: 100%;
	}

	.masonry-skeleton-item {
		margin-block-end: 34px;
		inline-size: 100%;
		display: inline-block;
		vertical-align: top;
	}

</style>
