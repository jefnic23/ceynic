<script lang="ts">
	import MasonryLayout from '$lib/components/masonry/MasonryLayout.svelte';
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<svelte:head>
	<link href="https://fonts.googleapis.com/css2?family=Sarina&display=swap" rel="stylesheet" />
</svelte:head>

<div class="wrapper">
	<div class="header-text">Original Abstract Oil Paintings on Canvas and Prints</div>
	<MasonryLayout data={data.products} />
</div>

<style>
	.header-text {
		font-family: 'Sarina', cursive;
		font-weight: 400;
		font-style: normal;
		font-size: xx-large;
		color: #62b2b2;
		margin-bottom: 21px;
		text-align: center;
	}

	.wrapper {
		display: flex;
		flex-direction: column;
		align-items: center;
		width: 100%;
		margin-right: auto;
		margin-left: auto;
	}

	/* Header text on medium-sized screens */
	@media only screen and (max-width: 1099px) and (min-width: 850px) {
		.header-text {
			font-size: x-large;
		}
	}

	/* Header text on small screens */
	@media only screen and (max-width: 849px) and (min-width: 600px) {
		.header-text {
			font-size: larger;
		}
	}

	@media only screen and (max-width: 599px) {
		.header-text {
			font-size: large;
		}
	}
</style>
