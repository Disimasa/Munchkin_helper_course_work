<svelte:head>
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@200;400;600;800;900&display=swap" rel="stylesheet">
</svelte:head>

<script>
  import {onMount} from 'svelte'
  import {createSmartappDebugger, createAssistant} from '@sberdevices/assistant-client'
  import Player from './Player.svelte';
  import axios from 'axios';
  let players = [];
  let state = {};
  let token = '';
  let initPhrase = 'Включи помощник для  Манчкина'; // <- сюда вставляем активационную фразу своего canvas app

  function getState() {
    console.log("State was get");
    const state = {
      item_selector: {
        items: players,
      }
    }
    return state;
  }

  let assistant;
  onMount(() => {
    const init = () => {
      // return createSmartappDebugger({
      //   token,
      //   initPhrase,
      //   getState,
      //   settings: {debugging: false}
      // })
      return createAssistant({getState});
    }
    assistant = init();

    assistant.on("start", (event) => {
      console.log(`assistant.on(start)`, event);
    });

    assistant.on("data", (event) => {
      console.log('EVENT!!!', event);
      switch (event.action.type) {
        // case 'update_data':
        //   players = event.action.players;
        //   break;
        case 'add_player':
          addPlayer(event.action.name)
        break;
        case 'plus_points':
          const ind = players.map((e) => {return e.name}).indexOf(event.action.name);
          if (ind !== -1) {
            plusPlayer(ind, event.action.points);
          }
        break;
        case 'delete_player':
          const deletedInd = players.map((e) => {return e.name}).indexOf(event.action.name);
          console.log(deletedInd)
          if (deletedInd !== -1) {
            deletePlayer(deletedInd);
          }
        break;
        case 'change_sex':
          const changedInd = players.map((e) => {return e.name}).indexOf(event.action.name);
          if (changedInd !== -1) {
            if (players[changedInd].gender === 'male')
              players[changedInd].gender = 'female';
            else
              players[changedInd].gender = 'male';
          }
        break;
      }
    });
  })

  let newPlayer = '';
  $: newPlayer = newPlayer.charAt(0).toUpperCase() + newPlayer.slice(1);

  function addPlayer(name) {
    // assistant.sendAction({type: 'new_player', name})
    players = [...players, {name, level: 1, gender: '?'}]
  }

  function plusPlayer(id, amount = 1) {
    // assistant.sendAction({type: 'plus_player', name})
    players[id].level+=Number(amount);
  }

  function minusPlayer(id, amount = 1) {
    // assistant.sendAction({type: 'minus_player', name})
    players[id].level-=amount;
  }

  function deletePlayer(id) {
    // assistant.sendAction({type: 'delete_player', name})
    players = [
      ...players.slice(0, id),
      ...players.slice(id + 1, players.length)
    ]
  }

  axios.defaults.withCredentials = true;

  async function handleClick() {
    newPlayer = newPlayer.charAt(0).toLowerCase() + newPlayer.slice(1);
    addPlayer(newPlayer);
    newPlayer = '';
    input.focus()
  }

  let input;
</script>


<svelte:window on:keydown={(event) => {if (event.key === 'Enter' && newPlayer !== '') handleClick()}}/>
<main>
  <div class="card">
<!--    <button id="help-button" on:click={() => {-->
<!--      assistant.sendAction({-->
<!--	"type": "sdk_answer",-->
<!--	"pronounceText": [-->
<!-- 		"Работает!"-->
<!-- 	]})-->
<!--    }}>?</button>-->
    <h1>Игроки</h1>
    <div class="list">
      {#each players as {name, level, gender}, i}
        <Player bind:name bind:level bind:gender
          deleteFunc={() => deletePlayer(i)}
          plusFunc={() => plusPlayer(i)}
          minusFunc={() => minusPlayer(i)}
        />
      {/each}
    </div>
    <div class="add-block">
      <input bind:this={input} bind:value={newPlayer} style="width: {(newPlayer.length) * 10}px"
             class="new-player-input" type="text">
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

  #help-button {
    position: absolute;
    top: 10px;
    right: 20px;
    width: 30px;
    height: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 20px;
    padding: 10px;
    cursor: pointer;
  }

  #help-button:hover {
    border: 1px solid #333333;
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
    background-color: #FFFFFF;
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
    position: relative;
    box-shadow: 0 0 20px 1px rgba(0, 0, 0, 0.1);
    width: 100%;
    height: 100%;
    max-width: 500px;
    max-height: 700px;
    border-radius: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #FFFFFF;
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
    margin-bottom: 100px;
    /*width: 80%;*/
    /*padding-bottom: 20;*/
  }

</style>