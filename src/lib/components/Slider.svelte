<script lang="ts">
	import { createEventDispatcher, onMount } from 'svelte';

	export let min: number = 0;
	export let max: number = 1000;

	// Initially selected range (can be bound from the parent)
	export let selectedMin: number = min;
	export let selectedMax: number = max;

	const dispatch = createEventDispatcher();

	// Ensure that the sliders don't cross over each other
	function handleMinChange(event: Event) {
		const newMin = Number((event.target as HTMLInputElement).value);
		selectedMin = Math.min(newMin, selectedMax - 1);
		dispatch('change', { min: selectedMin, max: selectedMax });
	}

	function handleMaxChange(event: Event) {
		const newMax = Number((event.target as HTMLInputElement).value);
		selectedMax = Math.max(newMax, selectedMin + 1);
		dispatch('change', { min: selectedMin, max: selectedMax });
	}

    // Dynamic calculations for thumb positions (absolute pixels)
    let sliderWidth: number = 0;
	let rangeContainer: HTMLElement;

    // Measure container width on mount
    onMount(() => {
        sliderWidth = rangeContainer.offsetWidth;
    });

    // Calculate absolute positions of min and max thumbs
    $: minPosition = ((selectedMin - min) / (max - min)) * sliderWidth;
    $: maxPosition = ((selectedMax - min) / (max - min)) * sliderWidth;
</script>

<div class="slider-container" bind:this="{rangeContainer}">
	<div class="track"></div>

	<!-- Min slider -->
	<input
		type="range"
		class="slider"
		{min}
		{max}
		step="1"
		value={selectedMin}
		on:input={handleMinChange}
	/>

	<!-- Max slider -->
	<input
		type="range"
		class="slider"
		{min}
		{max}
		step="1"
		value={selectedMax}
		on:input={handleMaxChange}
	/>

	<div
		class="progress-bar"
		style="left: {minPosition}px; width: {maxPosition - minPosition}px;"
	></div>

	<div class="label" style="left: {minPosition}px">${selectedMin}</div>
	<div class="label" style="left: {maxPosition}px">${selectedMax}</div>
</div>

<style>
	.slider-container {
		position: relative;
		width: 100%;
		height: 50px; /* Increased height to center everything */
	}

	/* Full track (gray background) */
	.track {
		position: absolute;
		top: 50%;
		transform: translateY(-50%);
		width: 100%;
		height: 8px;
		background-color: #ddd;
		border-radius: 4px;
	}

	/* Selected range (progress bar) */
	.progress-bar {
		position: absolute;
		top: 50%;
		transform: translateY(-50%);
		height: 8px;
		background-color: #4caf50;
        border-radius: 4px;
		z-index: 1;
	}

	/* Range sliders */
	.slider {
		position: absolute;
		width: 100%;
		height: 40px; /* Ensures interactivity without visual issues */
		margin: 0;
		-webkit-appearance: none;
		appearance: none;
		background: none;
		pointer-events: none;
        z-index: 2;
	}

	/* Style for slider thumbs */
	.slider::-webkit-slider-thumb {
		-webkit-appearance: none;
		appearance: none;
		width: 20px;
		height: 20px;
		background-color: #4caf50;
		border-radius: 50%;
		cursor: pointer;
		pointer-events: auto;
		transform: translateY(5px); /* Align thumb to center */
	}

	.slider::-moz-range-thumb {
		width: 20px;
		height: 20px;
		background-color: #4caf50;
		border-radius: 50%;
		cursor: pointer;
	}

	/* Labels */
	.label {
		position: absolute;
		top: calc(50% + 20px); /* Position below the sliders */
		font-size: 14px;
		color: #333;
		transform: translateX(-50%);
		white-space: nowrap;
	}
</style>
