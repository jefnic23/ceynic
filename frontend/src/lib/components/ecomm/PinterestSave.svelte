<script lang="ts">
	import Icon from '@iconify/svelte';

	let {
		enabled,
		imageUrl,
		productUrl,
		description
	}: {
		enabled: Promise<boolean>;
		imageUrl?: string;
		productUrl: string;
		description: string;
	} = $props();

	let href = $derived(
		imageUrl
			? `https://www.pinterest.com/pin/create/button/?${new URLSearchParams({ url: productUrl, media: imageUrl, description })}`
			: undefined
	);
</script>

{#await enabled then isEnabled}
	{#if isEnabled && href}
		<a class="pinterest-save" {href} target="_blank" rel="noopener noreferrer" aria-label="Save {description} to Pinterest">
			<Icon icon="mdi:pinterest" width={16} height={16} aria-hidden="true" />
			Save
		</a>
	{/if}
{/await}

<style>
	.pinterest-save {
		position: absolute;
		inset-block-start: 0.75rem;
		inset-inline-start: 0.75rem;
		z-index: 1;
		display: inline-flex;
		align-items: center;
		gap: 0.25rem;
		padding: 0.375rem 0.625rem;
		border-radius: 0.5rem;
		background: oklch(0.59 0.23 28);
		color: oklch(1 0 none);
		font-size: 0.875rem;
		font-weight: 600;
		line-height: 1.25;
		text-decoration: none;
		box-shadow: 0 2px 8px oklch(0 0 none / 0.2);
		transition: opacity 180ms var(--ease-out);
	}

	.pinterest-save:focus-visible {
		outline-color: oklch(0.59 0.23 28);
	}

	.pinterest-save:active {
		background: color-mix(in oklch, oklch(0.59 0.23 28) 80%, oklch(0 0 none));
	}

	@media (hover: hover) and (pointer: fine) {
		.pinterest-save {
			opacity: 0;
			pointer-events: none;
		}

		:global(.pinterest-save-target:hover) .pinterest-save,
		.pinterest-save:focus-visible {
			opacity: 1;
			pointer-events: auto;
		}
	}
</style>
