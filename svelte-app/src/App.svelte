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
  export let userMsg = "";
  export let messageLog = [];

  // Define communication functions
  function sendMessage(event) {
    event.preventDefault();

    let url = serverAddr + '/api/v1/send/' + userId
    messageLog.push({ message: userMsg, time: Date.now(), bot: false})
    let config = { headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*' }
    }
    axios.post(url, { input: userMsg }, config )
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
        console.log(response.data)
        if (response.data.new == true) {
          messageLog.push({ message: response.data.message, time: Date.now(), bot: true })
        }
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
  body {
    font:12px arial;
    color: #222;
    text-align:center;
    padding:35px; }

  form, p, span {
    margin:0;
    padding:0; }

  input { font:12px arial; }

  a {
    color:#0000FF;
    text-decoration:none; }

    a:hover { text-decoration:underline; }

  #wrapper, #loginform {
    margin:0 auto;
    padding-bottom:25px;
    background:#EBF4FB;
    width:504px;
    border:1px solid #ACD8F0; }

  #loginform { padding-top:18px; }

  #loginform p { margin: 5px; }

  #chatbox {
    text-align:left;
    margin:0 auto;
    margin-bottom:25px;
    padding:10px;
    background:#fff;
    height:270px;
    width:430px;
    border:1px solid #ACD8F0;
    overflow:auto; }

  #usermsg {
    width:395px;
    border:1px solid #ACD8F0; }

  #submit { width: 60px; }

  .error { color: #ff0000; }

  #menu { padding:12.5px 25px 12.5px 25px; }

  .welcome { float:left; }

  .logout { float:right; }

  .msgln { margin:0 0 2px 0; }
</style>

<div class="main-body">
  <input bind:value={serverAddr} />
  <div id="wrapper">
    <div id="menu">
      <p class="welcome">Welcome, <b></b></p>
      <input bind:value={userId} />
      <div style="clear:both"></div>
    </div>

    <div id="chatbox">
      {#each messageLog as message}
      <div class='msgln'>{message.date}<b>Self</b>: {message.message}<br></div>
      {/each}
    </div>

    <div name="message">
      <input name="usermsg" type="text" id="usermsg" bind:value={userMsg} size="63" />
      <input name="submitmsg" type="submit" on:click|once={sendMessage}  id="submitmsg" value="Send" />
    </div>
  </div>
</div>
