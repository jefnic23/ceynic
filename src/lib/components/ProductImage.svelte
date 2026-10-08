<script lang="ts">
	import type { HTMLImgAttributes } from 'svelte/elements';

	interface Props extends Omit<HTMLImgAttributes, 'src'> {
		url?: string;
		rounded?: boolean;
		fill?: boolean;
		crop?: boolean;
	}

	let {
		url,
		rounded = false,
		fill = false,
		crop = false,
		alt = '',
		...attributes
	}: Props = $props();
</script>

{#if url}
	<img src={url} {alt} class:rounded class:fill class:crop {...attributes} />
{/if}

<style>
	img {
		display: block;
		max-width: 100%;
		height: auto;
		object-fit: cover;
	}

	.fill {
		width: 100%;
	}

	.crop {
		width: 100%;
		height: 100%;
	}

	.rounded {
		border-radius: 8px;
	}
</style>
