<script lang="ts">
	import ScrollableInput from '$lib/components/shared/ScrollableInput.svelte';

	let { title, minimum = $bindable(), maximum = $bindable(), minimumChanged = $bindable(), maximumChanged = $bindable(), lower, upper, unit }: {
		title: string;
		minimum: number;
		maximum: number;
		minimumChanged: boolean;
		maximumChanged: boolean;
		lower: number;
		upper: number;
		unit: 'price' | 'size';
	} = $props();
	let id = title.toLowerCase();
</script>

<fieldset>
	<legend>{title}</legend>
	<div class="bounds">
		<ScrollableInput bind:value={minimum} bind:relatedValue={maximum} bind:isChanged={minimumChanged} isMinimum id="min{id}" label="Min" min={lower} max={upper} className={unit} />
		<ScrollableInput bind:value={maximum} bind:relatedValue={minimum} bind:isChanged={maximumChanged} id="max{id}" label="Max" min={lower} max={upper} className={unit} />
	</div>
</fieldset>

<style>
	fieldset { border: 0; padding: 0; margin: 0; min-inline-size: 0; }
	legend { font-size: 1em; font-weight: bold; padding: 0; margin-block-end: 1.33em; }
	.bounds { display: flex; gap: 1rem; }
</style>
