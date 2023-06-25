<script>
  import { onMount } from "svelte";
  import TakePhoto from "./overlays/TakePhoto.svelte";
  import Countdown from "./overlays/Countdown.svelte";
  import UserInfo from "./overlays/UserInfo.svelte";
  import ThankYou from "./overlays/ThankYou.svelte";
  import { componentIndex } from "../stores/appStore";

  let currentStep = 0;
  componentIndex.subscribe((value) => {
    currentStep = value;
  });

  let steps = [TakePhoto, Countdown, UserInfo, ThankYou];
  let error = null;
  let showError = false;

  import API from "../services/api";

  let streamUrl = API.getStreamUrl();
</script>

<div class="flex flex-col justify-center items-center min-h-screen">
  {#if currentStep <= 1}
    <div class="flex justify-center items-center mb-4">
      <img
        class="w-[90%] max-w-screen-xl border-2 border-blue-300"
        src={streamUrl}
        alt="Livestream"
      />
    </div>
  {/if}

  <div class="flex justify-center items-center">
    <svelte:component
      this={steps[currentStep]}
      on:nextStep={() => {
        currentStep = (currentStep + 1) % steps.length;
      }}
      on:error={(event) => {
        error = event.detail;
        showError = true;
      }}
    />
  </div>

  {#if showError}
    <div class="fixed bottom-4 right-4 w-full sm:w-auto">
      <div class="alert alert-error">
        <div class="flex-1">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            class="w-6 h-6 mx-2 stroke-current"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 9v2m0 4h.01"
            />
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 20H12c-4.41828 0-8-3.58172-8-8V12C4 7.58172 7.58172 4 12 4h0c4.41828 0 8 3.58172 8 8v0c0 4.41828-3.58172 8-8 8z"
            />
          </svg>
          <p>{error}</p>
        </div>
        <button class="alert-close" on:click={() => (showError = false)}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            class="w-6 h-6 mx-2 stroke-current"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>
  {/if}
</div>
