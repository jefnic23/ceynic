<script lang="ts">
	import { tick } from "svelte";

	interface Props {
		value: number;
		relatedValue: number;
		isChanged: boolean;
		isMinimum: boolean;
		id?: string;
		label?: string;
		min: number | null;
		max: number | null;
		className?: "price" | "size" | "";
	}

	let {
		value = $bindable(),
		relatedValue = $bindable(),
		isChanged = $bindable(),
		isMinimum,
		id = "",
		label = "",
		min,
		max,
		className = ""
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
				setValue(newValue);

				// Mark the value as updated
				setFlag(true);
			}
		}
	}
</script>

<div class="container {className}">
    <label for={id}>{label}</label>
    <input
        id={id}
        type="number"
        min={min}
        max={max}
        step="1"
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
	.container {
		position: relative;
		display: inline-block;
		width: 100%;
	}

	.container label {
		position: absolute;
		top: 21%;
		left: 13px;
		transform: translateY(-100%);
		background: white;
		padding: 0 5px;
		font-size: 0.8em;
		transition: all 0.2s ease;
	}

	.container input {
		width: 100%;
		padding: 10px;
		font-size: 1em;
		box-sizing: border-box;
	}

	.container :global(input:focus + label),
	.container :global(input:not(:placeholder-shown) + label) {
		top: -10px;
		font-size: 0.7em;
		color: #007bff;
	}

    .price input {
		padding-left: 1rem; /* Add space for the dollar sign */
	}

    .price::before {
		content: '$';
		position: absolute;
		left: 0.5em; /* Adjust positioning as needed */
		top: 50%;
		transform: translateY(-50%);
		font-size: 1em;
		font-weight: bold;
		color: #333; /* Adjust color as needed */
	}

	.size::after {
		content: 'in.';
		position: absolute;
		right: 2rem; /* Adjust positioning as needed */
		top: 50%;
		transform: translateY(-50%);
		line-height: normal;
		font-size: 1em;
		font-weight: bold;
		color: #333; /* Adjust color as needed */
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

	input.at-limit {
		animation: pulseLimit 0.377s ease-out;
	}
</style>