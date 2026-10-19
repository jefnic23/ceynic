<script lang="ts">
	import { page } from '$app/state';
	const sections = [{ href: '/admin/settings', label: 'Site' }, { href: '/admin/settings/payments', label: 'Payments' }];
</script>

<nav aria-label="Settings sections">
	{#each sections as section (section.href)}
		<a href={section.href} aria-current={page.url.pathname === section.href ? 'page' : undefined}>{section.label}</a>
	{/each}
</nav>

<style>
	nav { display: flex; gap: 1.5rem; border-block-end: 1px solid var(--border); margin-block-end: 1.5rem; }
	a { color: color-mix(in oklch, var(--ink) 65%, transparent); padding-block: 0.5rem; text-decoration: none; border-block-end: 2px solid transparent; }
	a[aria-current='page'] { color: var(--ink); border-block-end-color: currentColor; }
	a:active { color: var(--link); }
	@media (hover: hover) and (pointer: fine) { a:hover { color: var(--ink); } }
</style>
