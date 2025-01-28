<script lang="ts">
	import type { PageData } from './$types';
	import { marked } from "marked";
	import Skeleton from '$lib/components/Skeleton.svelte';

	export let data: PageData;

	marked.use({
		gfm: true,
		breaks: true
	});

	const aboutContentPromise = loadAboutContent();

	async function loadAboutContent() {
		const aboutContent = await data.about;
		return marked.parse(aboutContent);
	}
</script>

<div class="wrapper">
	{#await aboutContentPromise}
		<Skeleton placeholderCount={1} />
	{:then aboutContent} 
		{@html aboutContent}
	{/await}
</div>

<style>
	.wrapper {
		width: 750px;
		display: flex;
		flex-direction: column;
	}
</style>
