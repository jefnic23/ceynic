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
	<path fill={color} d="M11 13H5v-2h6V5h2v6h6v2h-6v6h-2z" />
</svg>
