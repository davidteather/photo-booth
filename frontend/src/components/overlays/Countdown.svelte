<script>
  import { onMount, createEventDispatcher } from "svelte";
  import API from "../../services/api";
  import { sessionPhotoIDs } from "../../stores/appStore";
  const dispatch = createEventDispatcher();
  let count = 3;

  onMount(() => {
    const intervalId = setInterval(() => {
      if (count > 0) {
        count--;
      } else {
        clearInterval(intervalId);
        finishCountdown();
      }
    }, 1000);
  });

  function finishCountdown() {
    API.takePhoto()
      .then((data) => {
        sessionPhotoIDs.update((currentIDs) => [...currentIDs, data.photo_id]);
        dispatch("nextStep");
      })
      .catch((error) => {
        dispatch("error", error.message);
        throw error;
      });
  }
</script>

<div
  class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"
>
  <div class="text-white text-9xl">
    {count}
  </div>
</div>
