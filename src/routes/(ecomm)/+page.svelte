<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;

	let loadedImages = new Set<number>();
	const handleImageLoad = (id: number) => {
		loadedImages.add(id);
		loadedImages = new Set(loadedImages);
	};

	const placeholderCount = 12;
</script>

<svelte:head>
	<link href="https://fonts.googleapis.com/css2?family=Sarina&display=swap" rel="stylesheet" />
</svelte:head>

<div class="wrapper">
	<h1 class="header-text">Original Abstract Oil Paintings on Canvas and Prints</h1>
	<div class="masonry-layout">
		{#await data.products}
			{#each Array(placeholderCount) as _, index}
				<div class="masonry-item skeleton">
					<div class="skeleton-box"></div>
				</div>
			{/each}
		{:then products}
			{#each products as product}
				<div
					class="masonry-item {loadedImages.has(product.id) ? 'visible' : ''}"
					style="opacity: {loadedImages.has(product.id) ? 1 : 0};"
				>
					{#if product.imageUrl}
						<a href="/products/{product.id}" data-sveltekit-preload-data>
							<img
								src={product.imageUrl}
								alt={product.title}
								on:load={() => handleImageLoad(product.id)}
							/>
						</a>
					{/if}
				</div>
			{/each}
		{:catch error}
			<p style="color: red">{error.message}</p>
		{/await}
	</div>
</div>

<style>
	.header-text {
		font-family: 'Sarina', cursive;
		font-weight: 400;
		font-style: normal;
		color: #62b2b2;
	}

	.wrapper {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 100%;
		margin-right: auto;
		margin-left: auto;
	}

	.masonry-layout {
		transition: all 0.5s ease-in-out;
		column-gap: 34px;
		column-fill: initial;
		max-width: 1002px;
	}

	.masonry-item {
		margin-bottom: 34px;
		display: inline-block;
		vertical-align: top;
		opacity: 0;
		transition: opacity 0.5s ease-in-out;
	}

	.masonry-item.visible {
		opacity: 1;
	}

	img {
		max-width: 225px;
		object-fit: contain;
		transition: all 0.5s ease-in-out;
		backface-visibility: hidden;
	}

	/* Skeleton Loader Styles */
	.masonry-item.skeleton {
		opacity: 1;
		animation: shimmer 1.5s infinite;
	}

	.skeleton-box {
		width: 225px;
		height: 300px; /* Placeholder height */
		background: linear-gradient(to right, #eeeeee 8%, #dddddd 18%, #eeeeee 33%);
		background-size: 800px 104px;
		animation: shimmer 1.5s infinite;
		border-radius: 4px;
	}

	@keyframes shimmer {
		0% {
			background-position: -400px 0;
		}
		100% {
			background-position: 400px 0;
		}
	}

	/* Masonry on large screens */
	@media only screen and (min-width: 1100px) {
		.masonry-layout {
			column-count: 4;
		}
	}

	/* Masonry on medium-sized screens */
	@media only screen and (max-width: 1099px) and (min-width: 900px) {
		.masonry-layout {
			column-count: 3;
			width: 743px;
		}
	}

	/* Masonry on small screens */
	@media only screen and (max-width: 899px) and (min-width: 600px) {
		.masonry-layout {
			column-count: 2;
			width: 484px;
		}
	}

	@media only screen and (max-width: 599px) {
		.masonry-layout {
			column-count: 1;
			width: 225px;
		}
	}
</style>
