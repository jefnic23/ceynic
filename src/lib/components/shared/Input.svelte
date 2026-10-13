<script lang="ts">
	import type { HTMLInputAttributes } from 'svelte/elements';

	interface Props {
		id?: string;
		name?: string;
		label?: string;
		type?: 'text' | 'number' | 'email' | 'password';
		min?: number | null;
		max?: number | null;
		required?: boolean;
		autocomplete?: HTMLInputAttributes['autocomplete'];
		value: string | number;
	}

	let {
		id = '',
		name = id,
		label = '',
		type = 'text',
		min = null,
		max = null,
		required = false,
		autocomplete,
		value = $bindable()
	}: Props = $props();
</script>

<div class="container">
	<label for={id}>{label}</label>
	<input {id} {name} {type} min={type === 'number' ? min : undefined} max={type === 'number' ? max : undefined} bind:value {autocomplete} placeholder=" " {required} />
</div>

<style>
	.container {
		position: relative;
		display: inline-block;
		width: 100%;
	}

	.container label {
		position: absolute;
		top: 10px;
		left: 13px;
		transform: translateY(-100%);
		background: white;
		padding: 0 5px;
		font-size: 0.8em;
		transition: all 0.2s ease;
	}

	.container input {
		width: 100%;
		padding: 10px;
		font-size: 1em;
		box-sizing: border-box;
	}

	.container :global(input:focus + label),
	.container :global(input:not(:placeholder-shown) + label) {
		top: -10px;
		font-size: 0.7em;
		color: #007bff;
	}
</style>
