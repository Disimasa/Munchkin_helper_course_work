<svelte:head>
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@200;400;600;800;900&display=swap" rel="stylesheet">
</svelte:head>

<script>
  import {onMount} from 'svelte'
  import {createSmartappDebugger, createAssistant} from '@sberdevices/assistant-client'
  import Player from './Player.svelte';
  import axios from 'axios';

  let players = [
    {name: 'Игрок 1', level: 1, gender: 'male'},
    {name: 'Игрок 2', level: 1, gender: 'female'},
  ];
  let state = {};
  let token = '';
  let initPhrase = 'Включи Манчкин'; // <- сюда вставляем активационную фразу своего canvas app

  function getState() {
    console.log("State was get");
    const state = {
      item_selector: {
        items: players,
      }
    }
    return state;
  }

  onMount(() => {
    const init = () => {
    return createSmartappDebugger({
      token,
      initPhrase,
      getState,
      settings: {debugging: false}
    })
    // return createAssistant({getState});
    }
    let assistant = init();

    assistant.on("start", (event) => {
      console.log(`assistant.on(start)`, event);
    });

    assistant.on("data", (event) => {
      console.log('EVENT!!!', event);
      let name, gender, level;
      switch (event.type) {
        case 'add_player':
          ({name, gender} = event.action);
          addPlayer(name, gender);
          break;

        case 'set_level':
          ({name, level} = event.action);
          setLVL(name, level);
          break;

        // case
      }
    });
  })

  let newPlayer = '';
  $: newPlayer = newPlayer.charAt(0).toUpperCase() + newPlayer.slice(1);
  function addPlayer(name, gender) {
    players = [...players, {name, gender, level: 1}];
  }

  function setLVL(name, lvl){
    let i = -1;
    for (let player of players){
      if (player.name === name){
        players[players.indexOf(player)].level = lvl;
        break;
      }
    }
  }


  function deletePlayer(i) {
    players = players.slice(0, i).concat(players.slice(i + 1))
  }

  axios.defaults.withCredentials = true;

  async function handleClick() {
    let gender;
    try {
      // let test = await axios.get('http://localhost:8000/test')
      // console.log(test.data)
      // let resp = await fetch('http://localhost:8000/gender', {method:'POST', body: JSON.stringify({name: newPlayer})}).then(r => r.json())
      gender = (await axios.post('http://localhost:8000/gender', {name: newPlayer})).data.gender;
    } catch (e) {
      console.error(e);
      gender = 'female';
    }
    addPlayer(newPlayer, gender);
    newPlayer = '';
    input.focus()
  }

  let input;
</script>


<svelte:window on:keydown={(event) => {if (event.key === 'Enter' && newPlayer !== '') handleClick()}}/>
<main>
  <div class="card">
    <h1>Игроки</h1>
    <div class="list">
      {#each players as {name, level, gender}, i}
        <Player bind:name bind:level bind:gender deleteFunc={() => deletePlayer(i)}/>
      {/each}
    </div>
    <div class="add-block">
      <input bind:this={input} bind:value={newPlayer} style="width: {(newPlayer.length) * 10}px" class="new-player-input" type="text">
      <button disabled={newPlayer.length === 0} class="new-player-button" on:click={handleClick}>
        Добавить
      </button>
    </div>
  </div>
</main>

<style>
  input {
    color: inherit;
  }

  button {
    vertical-align: middle;
    margin: 0;
    padding: 5px;
    line-height: normal;
  }

  h1 {
    text-align: center;
    color: #272C54;
    font-family: 'Raleway', sans-serif;
    font-weight: 700;
    width: 80%;
    z-index: 2;
    box-shadow: 0 10px 10px 2px white;
    margin: 40px 0 0 0;
  }

  main {
    display: grid;
    place-items: center;
    height: 100%;
  }

  .list {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-grow: 2;
    overflow-y: scroll;
    width: 100%;
  }

  .card {
    box-shadow: 0 0 20px 1px rgba(0, 0, 0, 0.1);
    width: 100%;
    height: 100%;
    max-width: 500px;
    max-height: 700px;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }


  .new-player-input {
    border: 0;
    border-bottom: 1px double #666666;
    min-width: 100px;
    text-align: center;
  }

  .new-player-input:focus {
    outline: none;
  }

  div::-webkit-scrollbar {
    width: 7px; /* width of the entire scrollbar */
  }

  div::-webkit-scrollbar-track {
    background: transparent; /* color of the tracking area */
  }

  div::-webkit-scrollbar-thumb {
    background-color: #4361EE; /* color of the scroll thumb */
    border-radius: 20px; /* roundness of the scroll thumb */
    border: 3px solid #4361EE; /* creates padding around scroll thumb */
  }

  div {
    scrollbar-width: thin; /* "auto" or "thin"  */
    scrollbar-color: #4361EE transparent; /* scroll thumb & track */
    scroll-bar-border: 5px;
  }

  .new-player-button {
    background: none;
    border-radius: 20px;
    padding: 7px 14px;
    border-color: #272C54;
    color: #272C54;
    width: 120px;
  }

  .new-player-button:hover {
    cursor: pointer;
    background: #272C54;
    color: white;
  }

  .new-player-button:disabled {
    cursor: default;
    color: rgba(39, 44, 84, 0.44);
    border-color: rgba(39, 44, 84, 0.41);
    background: white;
  }

  .add-block {
    /*height: 90px;*/
    padding: 20px;
    box-shadow: 0 -5px 10px 4px white;
    display: flex;
    flex-direction: column;
    align-items: center;
    /*width: 80%;*/
    /*padding-bottom: 20;*/
  }

</style>