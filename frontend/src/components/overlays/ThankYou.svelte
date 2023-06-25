<script>
  import { onMount } from "svelte";
  import Confetti from "../effects/Confetti.svelte";

  onMount(() => {
    setTimeout(() => {
      window.location.href = "/";
    }, 10000);
  });

  let eventName = import.meta.env.PUBLIC_EVENT_NAME;

  function handleRestart() {
    window.location.href = "/";
  }
</script>

<Confetti />

<div class="text-white flex flex-col items-center justify-center">
  <div class="text-center">
    <h1 class="text-5xl font-bold text-blue-500">🎉 Thank You! 🎉</h1>
    <p class="text-xl mt-4">Your photo has been sent successfully.</p>
    <p class="text-xl">
      Enjoy the rest of {eventName} 🤠
    </p>
    <button
      on:click={handleRestart}
      class="mt-4 btn btn-primary btn-lg text-white">Take another photo</button
    >
  </div>
</div>
