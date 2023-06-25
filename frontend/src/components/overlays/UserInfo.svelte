<script>
  import { onMount, createEventDispatcher } from "svelte";
  import API from "../../services/api";
  import { sessionPhotoIDs } from "../../stores/appStore";

  const dispatch = createEventDispatcher();

  let emails = [""];
  let phones = [""];
  let promotionalConsent = false;
  let sessionIDs;
  let photoUrls = [];
  let eventName = import.meta.env.PUBLIC_EVENT_NAME;

  onMount(async () => {
    sessionPhotoIDs.subscribe((value) => {
      sessionIDs = value;
    });
    photoUrls = await Promise.all(sessionIDs.map((id) => API.getPhoto(id)));
  });

  function addEmailInput() {
    emails = [...emails, ""];
  }

  function addPhoneInput() {
    phones = [...phones, ""];
  }

  function deleteEmailInput(index) {
    emails = emails.filter((_, i) => i !== index);
  }

  function deletePhoneInput(index) {
    phones = phones.filter((_, i) => i !== index);
  }

  async function sendUserData(event) {
    event.preventDefault();
    const sendPhotoRequest = {
      photo_ids: sessionIDs,
      emails,
      phones,
      promotional_consent: promotionalConsent,
    };

    API.sendPhoto(sendPhotoRequest)
      .then((res) => {
        dispatch("nextStep");
      })
      .catch((err) => {
        dispatch("error", err.message);
        throw err;
      });
  }
</script>

<div class="flex flex-col items-center">
  <div class="carousel w-4/5 mt-4">
    {#each photoUrls as url, i}
      <div id={`item${i}`} class="carousel-item w-full">
        <img src={url} class="w-full" alt={`Your Photo ${i}`} />
      </div>
    {/each}
  </div>
  <div class="flex justify-center w-full py-2 gap-2">
    {#each photoUrls as url, i}
      <a href={`#item${i}`} class="btn btn-xs">{i + 1}</a>
    {/each}
  </div>

  <form on:submit={sendUserData} class="w-4/5 mx-auto mt-8 p-8">
    {#each emails as email, i}
      <div class="mb-4">
        <label
          class="block text-white text-sm font-bold mb-2"
          for={`email-${i}`}
        >
          Email {i + 1}
        </label>
        <div class="flex items-center space-x-4">
          <input
            class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
            id={`email-${i}`}
            type="email"
            bind:value={email}
            placeholder="Email"
          />
          <button
            type="button"
            class="bg-red-500 hover:bg-red-700 text-white p-1 rounded focus:outline-none focus:shadow-outline"
            on:click={() => deleteEmailInput(i)}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              class="h-6 w-6"
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
    {/each}
    <button
      type="button"
      class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mb-4"
      on:click={addEmailInput}>Add Another Email</button
    >

    {#each phones as phone, i}
      <div class="mb-4">
        <label
          class="block text-white text-sm font-bold mb-2"
          for={`phone-${i}`}
        >
          Phone {i + 1}
        </label>
        <div class="flex items-center space-x-4">
          <input
            class="shadow appearance-none border rounded w-full py-2 px-3 text-white leading-tight focus:outline-none focus:shadow-outline"
            id={`phone-${i}`}
            type="tel"
            bind:value={phone}
            placeholder="Phone Number"
          />
          <button
            type="button"
            class="bg-red-500 hover:bg-red-700 text-white p-1 rounded focus:outline-none focus:shadow-outline"
            on:click={() => deletePhoneInput(i)}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              class="h-6 w-6"
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
    {/each}

    <button
      type="button"
      class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mb-4"
      on:click={addPhoneInput}>Add Another Phone</button
    >

    <div class="mb-4">
      <input
        class="mr-2 leading-tight"
        type="checkbox"
        id="promotionalConsent"
        bind:checked={promotionalConsent}
      />
      <label class="text-md text-white" for="promotionalConsent">
        Allow {eventName} to use these photos as promotional material
      </label>
    </div>
    <div class="flex items-center justify-between">
      <button
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        type="submit"
      >
        Send
      </button>
    </div>
  </form>
</div>
