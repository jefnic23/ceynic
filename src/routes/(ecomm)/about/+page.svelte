<script lang="ts">
	import type { PageData } from './$types';
	import { marked } from "marked";
	import Skeleton from '$lib/components/shared/Skeleton.svelte';
	import PageContainer from '$lib/components/shared/PageContainer.svelte';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();

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

<PageContainer>
	{#await aboutContentPromise}
		<Skeleton />
	{:then aboutContent} 
		{@html aboutContent}
	{/await}
</PageContainer>
