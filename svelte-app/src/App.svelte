<script>
  import axios from 'axios';
  import { beforeUpdate, afterUpdate } from 'svelte';
  
  // Set up values
  export let serverAddr = "http://localhost:3000";
  if (localStorage.getItem('serverAddr')) {
    serverAddr = localStorage.getItem('serverAddr')
  }
  function updateServerAddr(event) {
    localStorage.setItem('serverAddr', serverAddr)
  }
  export let userId = "svelte";
  if (localStorage.getItem('userId')) {
    userId = localStorage.getItem('userId')
  }
  function updateUserId(event) {
    localStorage.setItem('userId', userId)
  }
  export let userMsg = "";
  export let messageLog = { log: [] };

  let messageDiv;

  // Define quick action ability
  function quickAction(message) {
    userMsg = message;
    sendMessage();
  }

  // Define communication functions
  function sendMessage(event) {
    if (event) {
      event.preventDefault();
    }

    let url = serverAddr + '/api/v1/send/' + userId
    messageLog.log.push({ message: userMsg, time: new Date(), bot: false})
    messageLog.log = messageLog.log
    let config = { headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*' }
    }
    axios.post(url, { input: userMsg }, config )
      .then(response => {
        if (!response.success) {
          console.error(response)
        }
        userMsg = "" // clear old message
      })
      .catch(console.error)
  }

  // Setup on enter handling
  function handleKeyPress(event) {
    if (event.keyCode == 13) { // enter key pressed
      sendMessage(event);
    }
  }

  function processMessage(msg) {
    let split = msg.split('(');
    let options = [];
    if (msg[msg.length-1] == ')' && split.length > 1) {
      let lastBit = split[split.length-1]
      lastBit = lastBit.slice(0, lastBit.length-1)
      options = lastBit.split(',')
    }
    if (options) {
      msg = msg.slice(0, msg.lastIndexOf('('))
    }
    return { msg, options }
  }

  function pollMessages() {
    let url = serverAddr + '/api/v1/get/' + userId
    axios.get(url)
      .then(response => {
        if (response.data.new == true || response.data.new == "true") {
          let processed = processMessage(response.data.message);
          messageLog.log.push({ message: processed.msg, options: processed.options,
            time: new Date(), bot: true })
          messageLog.log = messageLog.log
        }
      })
      .catch(console.error)

    // Continue polling
    let interval = 1000;
    setTimeout(pollMessages, interval);
  }
  // Kick off polling
  pollMessages()

  afterUpdate(() => {
    messageDiv.scrollTo(0, messageDiv.scrollHeight);
  });
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
  :global(body) {
    font:12px arial;
    color: #222;
    padding: 0px !important;
  }

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
    border:1px solid #ACD8F0; }

  #loginform { padding-top:18px; }

  #loginform p { margin: 5px; }

  #chatbox {
    height: calc(100vh - 200px);
    text-align:left;
    margin:0 auto;
    margin-bottom:25px;
    padding: 10px 20px;
    background:#fff;
    border:1px solid #ACD8F0;
    overflow:auto; }

  #usermsg {
    width: calc(100% - 50px);
    border:1px solid #ACD8F0; }

  #submit { width: 60px; }

  #message { padding: 12.5px 25px 12.5px 25px; }

  .error { color: #ff0000; }

  #menu { padding:12.5px 25px 12.5px 25px; }

  .welcome { float:left; }

  .logout { float:right; }

  .msgln { margin:0 0 2px 0; }
</style>

<div class="main-body">
  <span>Server: <input on:keyup={updateServerAddr} bind:value={serverAddr} /></span>
  <div id="wrapper">
    <div id="menu">
      <p class="welcome">Welcome, <b></b></p>
      <input on:keyup={updateUserId} bind:value={userId} />
      <div style="clear:both"></div>
    </div>

    <div id="chatbox" bind:this={messageDiv}>
      {#each messageLog.log as message}
      <div class='msgln'>{message.time.toLocaleString()}
        <b>
        {#if message.bot }
        Clara
        {:else}
        Self
        {/if}
        </b>: {message.message}<br>
        {#if message.options }
          {#each message.options as option}
          <button on:click={quickAction(option)}>{option}</button>
          {/each}
        {/if}
        </div>
      {/each}
    </div>

    <div name="message">
      <input name="usermsg" on:keydown={handleKeyPress} type="text" id="usermsg" bind:value={userMsg} size="63" />
      <input name="submitmsg" type="submit" on:click={sendMessage}  id="submitmsg" value="Send" />
    </div>
  </div>
</div>
