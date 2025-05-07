<script lang="ts">
    export let open: boolean = false;
</script>

<button class="hamburger-button" class:open on:click={() => open = !open}>
    <span></span>
    <span></span>
    <span></span>
    <span></span>
</button>

<style>
    .hamburger-button {
        width: 34px;
        height: 21px;
        position: relative;
        -webkit-transform: rotate(0deg);
        -moz-transform: rotate(0deg);
        -o-transform: rotate(0deg);
        transform: rotate(0deg);
        -webkit-transition: .5s ease-in-out;
        -moz-transition: .5s ease-in-out;
        -o-transition: .5s ease-in-out;
        transition: .5s ease-in-out;
        cursor: pointer;
        background: transparent;
        border: none;
	}

	.hamburger-button span {
		display: block;
        position: absolute;
        height: 5px;
        width: 100%;
        background: #666;
        border-radius: 5px;
        opacity: 1;
        left: 0;
        -webkit-transform: rotate(0deg);
        -moz-transform: rotate(0deg);
        -o-transform: rotate(0deg);
        transform: rotate(0deg);
        -webkit-transition: .25s ease-in-out;
        -moz-transition: .25s ease-in-out;
        -o-transition: .25s ease-in-out;
        transition: .25s ease-in-out;
	}

	.hamburger-button span:nth-child(1) {
        top: 0px;
    }

    .hamburger-button span:nth-child(2),.hamburger-button span:nth-child(3) {
        top: 10px;
    }

    .hamburger-button span:nth-child(4) {
        top: 20px;
    }

    .hamburger-button.open span:nth-child(1) {
        top: 10px;
        width: 0%;
        left: 50%;
    }

    .hamburger-button.open span:nth-child(2) {
        -webkit-transform: rotate(45deg);
        -moz-transform: rotate(45deg);
        -o-transform: rotate(45deg);
        transform: rotate(45deg);
    }

    .hamburger-button.open span:nth-child(3) {
        -webkit-transform: rotate(-45deg);
        -moz-transform: rotate(-45deg);
        -o-transform: rotate(-45deg);
        transform: rotate(-45deg);
    }

    .hamburger-button.open span:nth-child(4) {
        top: 10px;
        width: 0%;
        left: 50%;
    }
</style>