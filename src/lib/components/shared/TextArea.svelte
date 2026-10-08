<script lang="ts">
	interface Props {
		id?: string;
		label?: string;
		value: string;
	}

	let {
		id = '',
		label = '',
		value = $bindable()
	}: Props = $props();
</script>

<div class="container">
	<label for={id}>{label}</label>
	<textarea {id} name={id} {value} placeholder=" "></textarea>
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

	.container textarea {
		width: 100%;
		padding: 10px;
		font-size: 1em;
		box-sizing: border-box;
		resize: vertical;
		height: 89px;
		max-height: 477px;
	}

	.container :global(textarea:focus + label),
	.container :global(textarea:not(:placeholder-shown) + label) {
		top: -10px;
		font-size: 0.7em;
		color: #007bff;
	}
</style>
