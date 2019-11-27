<script>
  import axios from 'axios';
  
  // Set up values
  export let serverAddr = "http://localhost:3000";
  if (localStorage.getItem('serverAddr')) {
    userId = localStorage.getItem('serverAddr')
  }
  export let userId = "svelte";
  if (localStorage.getItem('userId')) {
    userId = localStorage.getItem('userId')
  }

  // Define communication functions
  function sendMessage(event) {
    event.preventDefault();

    let url = serverAddr + '/api/v1/send/' + userId
    axios.post(url, { input: event.message.text } )
      .then(response => {
        if (!response.success) {
          console.error(response)
        }
      })
      .catch(console.error)
  }

  function pollMessages() {
    let url = serverAddr + '/api/v1/get/' + userId
    axios.get(url)
      .then(response => {
        console.log(response)
      })
      .catch(console.error)

    // Continue polling
    let interval = 1000;
    setTimeout(pollMessages, interval);
  }
  // Kick off polling
  pollMessages()
</script>

<style>
	h1 {
		color: purple;
	}
  .main-body {
    max-width: 500px;
    margin-right: auto;
    margin-left: auto;
    background-color: grey;
    height: calc(100vh);
  }
</style>

<div class="main-body">
<input bind:value={serverAddr} />
<input bind:value={userId} />
<h1>Hello {userId}!</h1>
</div>
