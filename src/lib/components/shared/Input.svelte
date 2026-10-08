<script lang="ts">
	interface Props {
		id?: string;
		label?: string;
		type?: string;
		min?: number | null;
		max?: number | null;
		required?: boolean;
		value: string | number;
	}

	let {
		id = '',
		label = '',
		type = 'text',
		min = null,
		max = null,
		required = false,
		value = $bindable()
	}: Props = $props();
</script>

<div class="container">
	<label for={id}>{label}</label>
	{#if type === 'number'}
		<input {id} name={id} type="number" {min} {max} {value} placeholder=" " required={required} />
	{:else}
		<input {id} name={id} type="text" {value} placeholder=" " required={required}  />
	{/if}
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
