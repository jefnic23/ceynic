<!-- @migration-task Error while migrating Svelte code: $$props is used together with named props in a way that cannot be automatically migrated. -->
<script lang="ts">
	export let size: number = 24;
	export let color: string = 'currentColor';
</script>

<svg 
	xmlns="http://www.w3.org/2000/svg" 
	width={size}
	height={size}
	viewBox="0 0 24 24" 
	{...$$props}
>
	<path
		fill={color}
		d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V7H6z"
	/>
</svg>
