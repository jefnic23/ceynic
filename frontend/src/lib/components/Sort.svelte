<script lang="ts">
	import { onMount } from 'svelte';
	import { slide } from 'svelte/transition';

	interface Props {
		options?: { value: string; label: string }[];
		selected?: string;
		change: CallableFunction;
	}

	let { options = [], selected = $bindable(''), change }: Props = $props();

	let isDropdownOpen = $state(false);

	function selectOption(optionValue: string) {
		selected = optionValue; // Update local state
		change(optionValue); // Notify parent
		isDropdownOpen = false; // Close dropdown
	}

	// Function to handle clicks outside the dropdown
	function handleClickOutside(event: MouseEvent) {
		const dropdown = document?.querySelector('.dropdown-container');
		if (dropdown && !dropdown.contains(event.target as Node)) {
			isDropdownOpen = false; // Close dropdown
		}
	}

	// Attach and detach the document click listener
	onMount(() => {
		document?.addEventListener('click', handleClickOutside);

		return () => {
			document?.removeEventListener('click', handleClickOutside);
		}
	});
</script>

<div class="dropdown-container">
	<div
		class="dropdown-header {isDropdownOpen ? 'open' : ''}"
		onclick={() => (isDropdownOpen = !isDropdownOpen)}
		onkeydown={(e) => { 
            if (e.key !== "Enter" && e.key !== " ") return; 
            e.preventDefault();
            (e.target as HTMLElement).click();
        }} 
		role="button" 
        tabindex="0" 
        aria-pressed="false"
	>
		Sort: {options.find((option) => option.value === selected)?.label || ''}
		<span class="icon">▼</span>
	</div>
	{#if isDropdownOpen}
		<div class="dropdown-list" transition:slide={{ duration: typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: no-preference)').matches ? 233 : 0 }}>
			{#each options as option}
				<div 
					class:selected={option.value === selected} 
					onclick={() => selectOption(option.value)}
					onkeydown={(e) => { 
						if (e.key !== "Enter" && e.key !== " ") return; 
						e.preventDefault();
						(e.target as HTMLElement).click();
					}} 
					role="button" 
					tabindex="0" 
					aria-pressed="false"
				>
					<span>{option.label}</span>
					{#if option.value === selected}
						<span class="checkmark">✔</span>
					{/if}
				</div>
			{/each}
		</div>
	{/if}
</div>

<style>
	.dropdown-container {
		position: relative;
		inline-size: 200px;
		cursor: pointer;
	}

	.dropdown-header {
		padding: 0.5rem 1rem;
		background-color: var(--surface-muted);
		border: 1px solid var(--border);
		border-radius: 5px;
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 0.9rem;
		transition: border-radius 0.2s ease; /* Smoothly adjust border-radius */
	}

	.dropdown-header.open {
		border-end-start-radius: 0;
		border-end-end-radius: 0;
	}
	.dropdown-header:active { background: var(--border); }

	.dropdown-header .icon {
		margin-inline-start: 10px;
		transform: rotate(0deg);
	}

	.dropdown-header.open .icon {
		transform: rotate(180deg);
	}

	.dropdown-list {
		background-color: var(--surface-muted);
		border: 1px solid var(--border);
		border-block-start: none;
		border-radius: 0 0 5px 5px;
		position: absolute;
		inset-block-start: 100%;
		inset-inline-start: 0;
		inline-size: 100%;
		overflow-y: auto;
		box-shadow: 0 3px 5px color-mix(in oklch, var(--ink) 20%, transparent);
		z-index: 100;
	}

	.dropdown-list div {
		padding: 0.5rem 1rem;
		cursor: pointer;
		font-size: 0.9rem;
	}

	.dropdown-list div:active { background: var(--border); }
	@media (hover: hover) and (pointer: fine) { .dropdown-list div:hover { background: var(--border); } }
	@media (prefers-reduced-motion: no-preference) { .dropdown-header .icon { transition: transform 200ms var(--ease-out); } }

	/* Highlight selected option */
	.dropdown-list .selected {
		font-weight: bold;
		background-color: var(--border);
	}

	.checkmark {
		color: var(--success);
		font-size: 1rem;
		margin-inline-start: 5px;
	}
</style>
