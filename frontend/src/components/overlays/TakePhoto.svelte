<script>
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();

  function handleTakePhotoClick() {
    dispatch("nextStep");
  }
</script>

<div class="join">
  <button
    on:click={handleTakePhotoClick}
    class="btn join-item btn-lg btn-primary">One Photo</button
  >
  <button
    on:click={handleTakePhotoClick}
    class="btn join-item btn-lg btn-secondary">Three Photos</button
  >
</div>
