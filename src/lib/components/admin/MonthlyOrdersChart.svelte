<script lang="ts">
	let { months }: { months: { label: string; count: number }[] } = $props();
	let chartMax = $derived(Math.max(2, Math.ceil(Math.max(...months.map((month) => month.count)) / 2) * 2));
</script>

<div class="chart-scroll">
	<div class="chart">
		<div class="y-axis" aria-hidden="true">
			<span>{chartMax}</span><span>{chartMax / 2}</span><span>0</span>
		</div>
		<div class="plot">
			<div class="gridline top" aria-hidden="true"></div>
			<div class="gridline middle" aria-hidden="true"></div>
			<div class="gridline bottom" aria-hidden="true"></div>
			<ul class="monthly-orders" aria-label="Orders per month for the last six months">
				{#each months as month (month.label)}
					<li style:--bar-height="{(month.count / chartMax) * 100}%">
						<span class="bar-value">{month.count}</span>
						<div class="bar" aria-hidden="true"></div>
						<span class="month-label">{month.label}</span>
					</li>
				{/each}
			</ul>
		</div>
	</div>
</div>

<style>
	.chart-scroll { overflow-x: auto; padding-block-start: 1.5rem; }
	.chart { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: 0.5rem; min-inline-size: 22rem; padding-block-end: 2.5rem; }
	.y-axis { display: flex; flex-direction: column; justify-content: space-between; align-items: flex-end; block-size: 10rem; color: var(--ink-muted); font-size: 0.75rem; line-height: 1; font-variant-numeric: tabular-nums; }
	.plot { position: relative; block-size: 10rem; }
	.gridline { position: absolute; inset-inline: 0; border-block-start: 1px solid var(--border); }
	.gridline.top { inset-block-start: 0; }
	.gridline.middle { inset-block-start: 50%; }
	.gridline.bottom { inset-block-end: 0; }
	.monthly-orders { position: relative; display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 0.375rem; block-size: 100%; list-style: none; margin: 0; padding: 0; }
	.monthly-orders li { position: relative; display: flex; align-items: flex-end; justify-content: center; padding: 0; border: 0; }
	.bar { inline-size: 70%; max-inline-size: 3rem; block-size: var(--bar-height); border-radius: 0.25rem 0.25rem 0 0; background: var(--info); }
	.bar-value { position: absolute; inset-block-end: calc(var(--bar-height) + 0.25rem); font-size: 0.75rem; font-weight: 600; font-variant-numeric: tabular-nums; }
	.month-label { position: absolute; inset-block-start: calc(100% + 0.5rem); font-size: 0.75rem; text-align: center; color: var(--ink-muted); }
</style>
