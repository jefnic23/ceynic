<script lang="ts">
	export let id: string = '';
	export let label: string = '';
	export let type: string = 'text';
	export let min: number | null;
	export let max: number | null;
	export let value: string | number;
</script>

<div class="container">
	<label for={id}>{label}</label>
	{#if type === 'number'}
		<input {id} type="number" {min} {max} {value} placeholder=" " />
	{:else}
		<input {id} type="text" {value} placeholder=" " />
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
		top: 21%;
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

	.container input:focus + label,
	.container input:not(:placeholder-shown) + label {
		top: -10px;
		font-size: 0.7em;
		color: #007bff;
	}
</style>
