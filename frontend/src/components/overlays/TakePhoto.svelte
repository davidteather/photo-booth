<script>
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();

  function handleTakePhotoClick() {
    dispatch("nextStep");
  }
</script>

<button on:click={handleTakePhotoClick} class="btn join-item btn-lg btn-primary">
  Take Photo
</button>
