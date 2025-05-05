<script lang="ts">
    import Etsy from '$lib/icons/Etsy.svelte';
	import Instagram from '$lib/icons/Instagram.svelte';
	import Pinterest from '$lib/icons/Pinterest.svelte';

	export let copyright: string = "";

    let year: number = new Date().getFullYear();
</script>

<div class="footer">
    <div class="icons">
        <a href="https://www.etsy.com/shop/TraceyNicholasArt" target="_blank">
            <Etsy size={32} />
        </a>
        <a href="https://www.instagram.com/traceynicholas_art/" target="_blank">
            <Instagram size={32} />
        </a>
        <a href="https://www.pinterest.com/tnicholas48169/" target="_blank">
            <Pinterest size={32} color={"#E60023"} />
        </a>
    </div>
    <div class="copyright">
		<div>
			Copyright © {year}{copyright ? `, ${copyright}` : ""}. All rights reserved.
		</div>
		<div>
			<a href="/admin" style:color="#666666" style:text-decoration="none" target="_blank">Administration</a>
		</div>
		<div>
			Powered by <a href="https://github.com/jefnic23" target="_blank">ceynic.org</a>
		</div>
    </div>
</div>

<style>
    .footer {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
		padding: 1rem;
		background-color: #f8f8f8;
		border: 1px solid #e7e7e7;
	}

	.icons {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 1rem;
	}

	.copyright {
		display: flex;
		flex-direction: row;
		font-size: 12px;
	}

	.copyright > div {
		position: relative;
		padding: 0 0.5rem;
	}

	.copyright > div:not(:last-child)::after {
		content: "|";
		position: absolute;
		right: 0;
	}
</style>