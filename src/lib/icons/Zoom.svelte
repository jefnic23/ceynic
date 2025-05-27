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
    <path fill={color} d="M3 21v-6h2v2.6l3.1-3.1l1.4 1.4L6.4 19H9v2zM15.9 9.5l-1.4-1.4L17.6 5H15V3h6v6h-2V6.4z"/>
</svg>