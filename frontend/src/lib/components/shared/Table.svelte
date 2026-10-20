<script lang="ts" generics="T">
	import type { Snippet } from 'svelte';

	/* eslint-disable no-undef -- ESLint does not recognize T from Svelte's generics attribute. */
	interface Props {
		label: string;
		minWidth?: string;
		rows: T[];
		columns: { label: string; sortValue?: (row: T) => string | number | boolean | null | undefined }[];
		row: Snippet<[T]>;
		emptyMessage?: string;
	}
	/* eslint-enable no-undef */

	let { label, minWidth = '36rem', rows, columns, row, emptyMessage = 'No results found.' }: Props = $props();
	let sortColumn: number | null = $state(null);
	let sortDirection: 'ascending' | 'descending' = $state('ascending');

	function toggleSort(index: number) {
		if (sortColumn === index) {
			sortDirection = sortDirection === 'ascending' ? 'descending' : 'ascending';
		} else {
			sortColumn = index;
			sortDirection = 'ascending';
		}
	}

	let sortedRows = $derived.by(() => {
		const getValue = sortColumn === null ? undefined : columns[sortColumn]?.sortValue;
		if (!getValue) return rows;

		return [...rows].sort((a, b) => {
			const left = getValue(a);
			const right = getValue(b);
			// Keep missing values at the end regardless of direction.
			if (left == null) return right == null ? 0 : 1;
			if (right == null) return -1;

			let result: number;
			if (typeof left === 'number' && typeof right === 'number') {
				result = left - right;
			} else if (typeof left === 'boolean' && typeof right === 'boolean') {
				result = Number(left) - Number(right);
			} else {
				result = String(left).localeCompare(String(right), undefined, { numeric: true, sensitivity: 'base' });
			}
			return sortDirection === 'ascending' ? result : -result;
		});
	});
</script>

<div class="table-scroll">
	<table aria-label={label} style:min-width={minWidth}>
		<thead>
			<tr>
				{#each columns as column, index}
					<th scope="col" aria-sort={column.sortValue ? (sortColumn === index ? sortDirection : 'none') : undefined}>
						{#if column.sortValue}
							<button type="button" class="sort-button" class:active={sortColumn === index} onclick={() => toggleSort(index)}>
								{column.label}
								<span class="sort-icon" aria-hidden="true">{sortColumn === index ? (sortDirection === 'ascending' ? '↑' : '↓') : '↕'}</span>
							</button>
						{:else}
							{column.label}
						{/if}
					</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each sortedRows as item}
				{@render row(item)}
			{:else}
				<tr><td colspan={columns.length}>{emptyMessage}</td></tr>
			{/each}
		</tbody>
	</table>
</div>

<style>
	.table-scroll {
		inline-size: 100%;
		max-inline-size: 100%;
		overflow-x: auto;
		border: 1px solid var(--border);
		border-radius: 0.5rem;
		background: var(--surface);
	}

	table {
		inline-size: 100%;
		border-collapse: collapse;
		text-align: start;
		color: var(--ink);
	}

	table :global(th),
	table :global(td) {
		padding-block: 0.75rem;
		padding-inline: 1rem;
		vertical-align: middle;
	}

	table :global(th) {
		background: var(--surface-muted);
		color: var(--ink-muted);
		font-size: 0.75rem;
		font-weight: 600;
		letter-spacing: 0.05em;
		text-transform: uppercase;
		white-space: nowrap;
	}

	.sort-button {
		display: inline-flex;
		align-items: center;
		gap: 0.4rem;
		padding: 0;
		border: 0;
		background: transparent;
		color: inherit;
		font: inherit;
		font-weight: inherit;
		letter-spacing: inherit;
		text-transform: inherit;
		cursor: pointer;
	}

	.sort-button.active {
		color: var(--ink);
	}
	.sort-button:active { color: var(--link); }
	@media (hover: hover) and (pointer: fine) {
		.sort-button:hover { color: var(--ink); }
		table :global(tbody tr:hover) { background: var(--surface-muted); }
	}

	.sort-button:focus-visible {
		outline: 2px solid var(--link);
		outline-offset: 4px;
		border-radius: 2px;
	}

	.sort-icon {
		color: var(--ink-muted);
		font-size: 0.875rem;
		line-height: 1;
	}

	.sort-button.active .sort-icon {
		color: var(--link);
	}

	table :global(tbody tr) {
		border-block-start: 1px solid var(--border);
	}

	table :global(td[colspan]) {
		padding-block: 2rem;
		padding-inline: 1rem;
		text-align: center;
		color: var(--ink-muted);
	}
</style>
