<script lang="ts">
	import type { PageData } from './$types';
	import { marked } from 'marked';
	import Skeleton from '$lib/components/shared/Skeleton.svelte';
	import PageContainer from '$lib/components/shared/PageContainer.svelte';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();

	marked.use({
		gfm: true,
		breaks: true,
		renderer: {
			html({ text }) {
				return text.replace(/[&<>"']/g, (character) => {
					const entities: Record<string, string> = {
						'&': '&amp;',
						'<': '&lt;',
						'>': '&gt;',
						'"': '&quot;',
						"'": '&#39;'
					};
					return entities[character];
				});
			}
		}
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
		<!-- eslint-disable-next-line svelte/no-at-html-tags -->
		{@html aboutContent}
	{/await}
</PageContainer>
