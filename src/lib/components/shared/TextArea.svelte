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

<div class="floating-field">
	<label for={id}>{label}</label>
		<textarea {id} name={id} bind:value placeholder=" "></textarea>
</div>

<style>
	textarea {
		resize: vertical;
		block-size: 89px;
		max-block-size: 477px;
	}
</style>
