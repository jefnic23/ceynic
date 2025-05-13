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
	<g 
		fill="none" 
		stroke={color} 
		stroke-linecap="round" 
		stroke-width="2"
	>
		<path d="M19.5 12H8" />
		<path
			stroke-linejoin="round"
			d="M9 4H7a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h2m7-4l4-4l-4-4"
		/>
	</g>
</svg>
