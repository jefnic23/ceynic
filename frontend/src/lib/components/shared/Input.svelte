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
		readonly?: boolean;
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
		readonly = false,
		autocomplete,
		value = $bindable()
	}: Props = $props();
</script>

<div class="floating-field">
	<label for={id}>{label}</label>
	<input {id} {name} {type} min={type === 'number' ? min : undefined} max={type === 'number' ? max : undefined} bind:value {autocomplete} placeholder=" " {required} {readonly} />
</div>

