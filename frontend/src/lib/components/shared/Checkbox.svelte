<script lang="ts">
	interface Props {
		name: string;
		label: string;
		id?: string;
		checked?: boolean;
	}

	let { name, label, id = name, checked = $bindable(false) }: Props = $props();
</script>

<label for={id}>
	<input {id} {name} type="checkbox" bind:checked />
	{label}
</label>

<style>
	label {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
	}

	input {
		width: 21px;
		height: 21px;
		margin: 0;
	}
</style>
