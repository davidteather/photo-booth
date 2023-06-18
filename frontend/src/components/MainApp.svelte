<script>
    import { onMount } from 'svelte';
    import TakePhoto from './overlays/TakePhoto.svelte';
    import Countdown from './overlays/Countdown.svelte';
    import UserInfo from './overlays/UserInfo.svelte';
    import ThankYou from './overlays/ThankYou.svelte';
    
    let currentStep = 0;
    let steps = [TakePhoto, Countdown, UserInfo, ThankYou];

    onMount(() => {
        // Add your transition logic here, for example:
        const intervalId = setInterval(() => {
            if (currentStep < steps.length - 1) {
                currentStep++;
            } else {
                clearInterval(intervalId);
            }
        }, 3000); // This will switch to the next component every 3 seconds
    });
</script>

<svelte:component this={steps[currentStep]} />
