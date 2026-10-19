<script lang="ts">
	import { tick } from "svelte";

	interface Props {
		value: number;
		relatedValue?: number;
		isChanged?: boolean;
		isMinimum?: boolean;
		id?: string;
		label?: string;
		min?: number;
		max?: number;
		step?: number;
		className?: "price" | "size" | "";
	}

	let {
		value = $bindable(),
		relatedValue = $bindable(),
		isChanged = $bindable(),
		isMinimum = false,
		id = "",
		label = "",
		min = 0,
		max = Infinity,
		className = "",
		step = 1
	}: Props = $props();

	let minAtLimit = $state(false);
	let maxAtLimit = $state(false);

	async function flashLimit(setLimit: (v: boolean) => void) {
		setLimit(false);
		await tick();
		setLimit(true);
		await tick();
		setTimeout(() => setLimit(false), 377);
	}

    function handleInput(
        event: Event,
		setValue: (newValue: number) => void,
		setFlag: (newFlag: boolean) => void,
		relatedValue?: number,
		isMin?: boolean
    ): void {
        const input = event.target as HTMLInputElement;
        
        let newValue = Number(input.value);

        const min = Number(input.min) || -Infinity;
        const max = Number(input.max) || Infinity;

        // Clamp between min/max
        newValue = Math.max(min, Math.min(max, newValue));

        if (isMin && relatedValue !== undefined) {
            // If this is a min value, make sure it doesn't exceed max
            newValue = Math.min(newValue, relatedValue);
        } else if (!isMin && relatedValue !== undefined) {
            // If this is a max value, make sure it doesn't go below min
            newValue = Math.max(newValue, relatedValue);
        }

		setValue(newValue);

		// Mark the value as updated
		setFlag(true);
    }

    function handleWheel(
		event: WheelEvent,
		setValue: (newValue: number) => void,
		setFlag: (newFlag: boolean) => void,
		relatedValue?: number,
		isMin?: boolean,
		flashLimitReached?: () => void
	): void {
		const input = event.target as HTMLInputElement;

		if (document?.activeElement === input) {
			event.preventDefault(); // Prevent page scrolling behavior

			const step = Number(input.step) || 1;
			const min = Number(input.min) || -Infinity;
			const max = Number(input.max) || Infinity;

			// Determine new value based on scroll direction
			let newValue = Number(input.value) + (event.deltaY < 0 ? step : -step);

			// Clamp the value between min and max
			newValue = Math.max(min, Math.min(max, newValue));

			if (isMin && relatedValue !== undefined) {
                // If this is a min value, make sure it doesn't exceed max
                newValue = Math.min(newValue, relatedValue);
            } else if (!isMin && relatedValue !== undefined) {
                // If this is a max value, make sure it doesn't go below min
                newValue = Math.max(newValue, relatedValue);
            }

			if (newValue === value && flashLimitReached) {
				flashLimitReached(); // trigger the animation
			} else {
				// Update the bound value
				if (Number.isInteger(newValue)) {
					setValue(newValue);
				} else {
					setValue(parseFloat(newValue.toFixed(2)))
				}

				// Mark the value as updated
				setFlag(true);
			}
		}
	}
</script>

<div class="floating-field {className}">
    <label for={id}>{label}</label>
    <input
        id={id}
		name={id}
        type="number"
        min={min}
        max={max}
        step={step}
        bind:value={value}
		class:at-limit={isMinimum ? minAtLimit : maxAtLimit}
        onblur={(e) => handleInput(
			e, 
			(newValue) => value = newValue, 
			(newFlag) => isChanged = newFlag, 
			relatedValue, 
			isMinimum
		)}
        onwheel={(e) => handleWheel(
			e, 
			(newValue) => value = newValue, 
			(newFlag) => isChanged = newFlag, 
			relatedValue, 
			isMinimum,
			() => flashLimit((v) => (isMinimum ? minAtLimit = v : maxAtLimit = v))
		)}
    />
</div>

<style>
    .price input {
		padding-inline-start: 1rem;
	}

    .price::before {
		content: '$';
		position: absolute;
		inset-inline-start: 0.5em;
		inset-block-start: 50%;
		transform: translateY(-50%);
		font-size: 1em;
		font-weight: bold;
		color: var(--ink-muted);
	}

	.size::after {
		content: 'in.';
		position: absolute;
		inset-inline-end: 2rem;
		inset-block-start: 50%;
		transform: translateY(-50%);
		line-height: normal;
		font-size: 1em;
		font-weight: bold;
		color: var(--ink-muted);
	}

	@keyframes pulseLimit {
		0% {
			box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.6);
			border-color: red;
		}
		50% {
			box-shadow: 0 0 0 6px rgba(255, 0, 0, 0);
			border-color: red;
		}
		100% {
			box-shadow: 0 0 0 0 rgba(255, 0, 0, 0);
			border-color: inherit;
		}
	}

	@media (prefers-reduced-motion: no-preference) {
		input.at-limit { animation: pulseLimit 0.377s var(--ease-out); }
	}
</style>
