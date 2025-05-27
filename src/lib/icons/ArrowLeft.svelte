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
    <path fill={color} d="M10 22L0 12L10 2l1.775 1.775L3.55 12l8.225 8.225z" />
</svg>
