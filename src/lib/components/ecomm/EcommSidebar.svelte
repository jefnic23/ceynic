<script lang="ts">
	import Cart from "$lib/icons/Cart.svelte";
	import Sidebar from "$lib/components/shared/Sidebar.svelte";
	import Home from "$lib/icons/Home.svelte";
	import Info from "$lib/icons/Info.svelte";
	import Mail from "$lib/icons/Mail.svelte";
	import Browse from "$lib/icons/Browse.svelte";

    export let url: URL;
</script>

<Sidebar>
    <div class="sidebar">
        <div class="sidebar-top">
            <nav>
                <a href="/" data-sveltekit-preload-data class:active={url.pathname === '/'}>
                    <Home />
                    <span class="label">Home</span>
                </a>
                <a href="/products" data-sveltekit-preload-data class:active={url.pathname.startsWith('/products')}>
                    <Browse />
                    <span class="label">Browse</span>
                </a>
                <a href="/about" data-sveltekit-preload-data class:active={url.pathname === '/about'}>
                    <Info />
                    <span class="label">About</span>
                </a>
                <a href="/contact" class:active={url.pathname === '/contact'}>
                    <Mail />
                    <span class="label">Contact</span>
                </a>
            </nav>
        </div>
        <div class="sidebar-bottom">
            <a href="/cart" class:active={url.pathname === '/cart'}>
                <Cart size={32} />
                <span class="label">Cart</span>
            </a>
        </div>
    </div>
</Sidebar>

<style>
    .sidebar {
        display: none;
		flex-direction: column;
		justify-content: space-between;
		align-items: flex-start;
		height: 100%;
		padding: 1rem;
    }

    nav {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	a {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		text-transform: uppercase;
		color: rgba(0, 0, 0, 0.65);
		font-size: 1rem;
		text-decoration: none;
		background: none;
		border: none;
		padding: 0.5rem;
		transition: background 0.2s ease, color 0.2s ease;
		border-radius: 4px;
		width: 100%;
		line-height: normal;
	}

    @media (max-width: 768px) {
        .sidebar {
            display: flex;
        }
    }
</style>