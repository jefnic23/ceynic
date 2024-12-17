<script lang="ts">
	import { createEventDispatcher, onMount, onDestroy } from 'svelte';
	import { slide } from 'svelte/transition';

	export let options: { value: string; label: string }[] = [];
	export let selected: string = '';

	let isDropdownOpen = false;

	const dispatch = createEventDispatcher();

	function selectOption(optionValue: string) {
		selected = optionValue; // Update local state
		dispatch('change', optionValue); // Notify parent
		isDropdownOpen = false; // Close dropdown
	}

	// Function to handle clicks outside the dropdown
	function handleClickOutside(event: MouseEvent) {
		const dropdown = document.querySelector('.dropdown-container');
		if (dropdown && !dropdown.contains(event.target as Node)) {
			isDropdownOpen = false; // Close dropdown
		}
	}

	// Attach and detach the document click listener
	onMount(() => {
		document.addEventListener('click', handleClickOutside);
	});

	onDestroy(() => {
		document.removeEventListener('click', handleClickOutside);
	});
</script>

<div class="dropdown-container">
	<div
		class="dropdown-header {isDropdownOpen ? 'open' : ''}"
		on:click={() => (isDropdownOpen = !isDropdownOpen)}
	>
		Sort: {options.find((option) => option.value === selected)?.label || ''}
		<span class="icon">▼</span>
	</div>
	{#if isDropdownOpen}
		<div class="dropdown-list" transition:slide={{ duration: 233 }}>
			{#each options as option}
				<div class:selected={option.value === selected} on:click={() => selectOption(option.value)}>
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
		width: 200px;
		cursor: pointer;
	}

	.dropdown-header {
		padding: 0.5rem 1rem;
		background-color: #f9f9f9;
		border: 1px solid #ccc;
		border-radius: 5px;
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 0.9rem;
		transition: border-radius 0.2s ease; /* Smoothly adjust border-radius */
	}

	.dropdown-header.open {
		border-bottom-left-radius: 0;
		border-bottom-right-radius: 0;
	}

	.dropdown-header .icon {
		margin-left: 10px;
		transform: rotate(0deg);
		transition: transform 0.2s ease-in-out;
	}

	.dropdown-header.open .icon {
		transform: rotate(180deg);
	}

	.dropdown-list {
		background-color: #f9f9f9;
		border: 1px solid #ccc;
		border-top: none;
		border-radius: 0 0 5px 5px;
		position: absolute;
		top: 100%;
		left: 0;
		width: 100%;
		overflow-y: auto;
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
		z-index: 100;
	}

	.dropdown-list div {
		padding: 0.5rem 1rem;
		cursor: pointer;
		font-size: 0.9rem;
	}

	.dropdown-list div:hover {
		background-color: #f0f0f0;
	}

	/* Highlight selected option */
	.dropdown-list .selected {
		font-weight: bold;
		background-color: #e0e0e0;
	}

	.checkmark {
		color: green;
		font-size: 1rem;
		margin-left: 5px;
	}
</style>
