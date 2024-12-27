<script lang="ts">
	export let id: string = '';
	export let label: string = '';
	export let type: string = 'text';
	export let min: number | null;
	export let max: number | null;
	export let value: string | number;
</script>

<div class="input-container">
	<label for={id}>{label}</label>
	{#if type === 'number'}
		<input {id} type="number" {min} {max} {value} placeholder=" " />
	{:else}
		<input {id} type="text" {value} placeholder=" " />
	{/if}
</div>

<style>
	.input-container {
		position: relative;
		display: inline-block;
		width: 100%;
	}

	.input-container label {
		position: absolute;
		top: 21%;
		left: 13px;
		transform: translateY(-100%);
		background: white;
		padding: 0 5px;
		font-size: 0.8em;
		transition: all 0.2s ease;
	}

	.input-container input {
		width: 100%;
		padding: 10px;
		font-size: 1em;
		box-sizing: border-box;
	}

	.input-container input:focus + label,
	.input-container input:not(:placeholder-shown) + label {
		top: -10px;
		font-size: 0.7em;
		color: #007bff;
	}
</style>
