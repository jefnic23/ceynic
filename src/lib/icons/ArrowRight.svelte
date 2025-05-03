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
    <path fill={color} d="M8.025 22L6.25 20.225L14.475 12L6.25 3.775L8.025 2l10 10z" />
</svg>
