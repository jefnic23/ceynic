<script lang="ts">
    import { browser } from "$app/environment";

    export let measurementId: string;

    if (browser) {
        window.dataLayer = window.dataLayer || [];
        window.gtag = function gtag(): void {
            window.dataLayer.push(arguments);
        };
        window.gtag("js", new Date());
        window.gtag("config", measurementId);
	}
</script>

<svelte:head>
    <script async src="https://www.googletagmanager.com/gtag/js?id={measurementId}"></script>
</svelte:head>