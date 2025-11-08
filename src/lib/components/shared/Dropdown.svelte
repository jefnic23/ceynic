<script lang="ts">
	import type { Snippet } from "svelte";

	interface Props {
		id: string;
		label: string;
		value: string;
        children?: Snippet;
	}

	let {
		id,
		label,
		value,
        children
	}: Props = $props();
</script>

<div class="container">
	<label for={id}>{label}</label>
	<select {id} name={id} {value} style:padding="13px">
        {@render children?.()}
    </select>
</div>

<style>
	.container {
		position: relative;
		display: inline-block;
		width: 100%;
	}

	.container label {
		position: absolute;
		top: 21%;
		left: 13px;
		transform: translateY(-100%);
		background: white;
		padding: 0 5px;
		font-size: 0.8em;
		transition: all 0.2s ease;
	}

	.container select {
		width: 100%;
		padding: 10px;
		font-size: 1em;
		box-sizing: border-box;
	}

	.container :global(select:focus + label),
	.container :global(select:not(:placeholder-shown) + label) {
		top: -10px;
		font-size: 0.7em;
		color: #007bff;
	}
</style>
