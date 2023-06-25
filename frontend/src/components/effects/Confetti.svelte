<script>
  import { onMount } from "svelte";
  import confetti from "canvas-confetti";

  let confettiCanvas;

  /*
    Maybe use MadHacks colors?
    Example Confetti: https://www.kirilv.com/canvas-confetti/#continuous
  */

  onMount(() => {
    confetti.create(confettiCanvas, {
      resize: true,
      useWorker: true,
    })({
      particleCount: 2500,
      spread: 260,
      decay: 0.95,
      gravity: 1.2,
      ticks: 400,
    });
  });
</script>

<canvas
  bind:this={confettiCanvas}
  class="confetti-canvas pointer-events-none"
/>

<style>
  .confetti-canvas {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    z-index: 9999;
  }
</style>
