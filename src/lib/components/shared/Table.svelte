<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		label: string;
		minWidth?: string;
		children?: Snippet;
	}

	let { label, minWidth = '36rem', children }: Props = $props();
</script>

<div class="table-scroll">
	<table aria-label={label} style:min-width={minWidth}>
		{@render children?.()}
	</table>
</div>

<style>
	.table-scroll {
		width: 100%;
		max-width: 100%;
		overflow-x: auto;
		border: 1px solid #e5e7eb;
		border-radius: 0.5rem;
		background: #fff;
	}

	table {
		width: 100%;
		border-collapse: collapse;
		text-align: left;
		color: #374151;
	}

	table :global(th),
	table :global(td) {
		padding: 0.75rem 1rem;
		vertical-align: middle;
	}

	table :global(th) {
		background: #f9fafb;
		color: #4b5563;
		font-size: 0.75rem;
		font-weight: 600;
		letter-spacing: 0.05em;
		text-transform: uppercase;
		white-space: nowrap;
	}

	table :global(tbody tr) {
		border-top: 1px solid #e5e7eb;
	}

	table :global(tbody tr:hover) {
		background: #f9fafb;
	}

	table :global(td[colspan]) {
		padding: 2rem 1rem;
		text-align: center;
		color: #6b7280;
	}
</style>
