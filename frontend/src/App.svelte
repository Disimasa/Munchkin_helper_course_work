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
  let token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzNjk4NTAzMzgzMjViZmViZjg2ZGVjYjAzZDkzZjkwZDQ2ZmMxNmNmZGZiNTUyMDAzNGQxOTFkMWEwYTQ4NDQyNTM5YmU5MjcwMDQyNjI5OCIsImF1ZCI6IlZQUyIsImV4cCI6MTYyMTE1ODg2MywiaWF0IjoxNjIxMDcyNDUzLCJpc3MiOiJLRVlNQVNURVIiLCJ0eXBlIjoiQmVhcmVyIiwianRpIjoiMTcyOTIzMmUtOTE2Mi00YjU2LTllOTMtMGQ2N2MxM2QzOWJjIiwic2lkIjoiODkxNDdhOTQtMjdiNy00NDY0LTk5ZDgtODZjMDNlZTkyMjgxIn0.ZYpJfZZIR3hnKBUpZfbjc3AcH45iUcph_OKpcWXbAKvuS-NFm5dSXXfx2h5zDqoFlA6i1FLJpWnx4QwIZI-Y98yaS5R38kCw85Ke3BInXnl056rYDX1LZWgyhBD9GeOdRxjJnkW6YOkwdkSjpxyk25K_dD-aVZ7mcLkTw2eMr1mjpIGpo-lO8HiKSCAjqK3F6IFIbDX-lvli0m48kcdspKIwAeDbevisLoikkI3JB1qwMiBXGlaBuZbAadB9fLkyan-Puhz3ee2u0FPgp26gfxUWXoeMMzWlnYyMJ7LVt-3MajYfjCBmmQd56GtFNp7WpCfsJEKYDBWA3UQ6Gj2qQRUOh8-1xVqgppl8ZGZOH4qjAlHCVx-b222lmoViqL4M0zZM_JWxwMjckXPZvrDX0aJc8E0kfNoMzeQ6lCzhQXFc2aJV9ukvFEVR7llOSZww1ysFRFCYCek90dPDzReqtdhDCJw7OqzQvPcJuh__GuU13JKLaGyPId8PMzJU4BdWIvIimCfAzldsoWDZf769LQWaemoB4VdvzWy3p2yYENcwtJbnKzMWvMFwtgqZJWVqIPwv3jvdDMWeaLPmNAvweuJA0h5MeUnhZCIdRAvEPxb5d5qKM7EShp7xWgwfAKoQRanmU9RnDyEhGlssvsI1JN15voRW8Q_ty-vlGjA8kAM';
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

  let assistant;
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
    assistant = init();

    assistant.on("start", (event) => {
      console.log(`assistant.on(start)`, event);
    });

    assistant.on("data", (event) => {
      console.log('EVENT!!!', event);
      switch (event.type) {
        case 'update_data':
          players = event.action.players;
          break;
      }
    });
  })

  let newPlayer = '';
  $: newPlayer = newPlayer.charAt(0).toUpperCase() + newPlayer.slice(1);

  function addPlayer(name) {
    assistant.sendAction({type: 'new_player', name})
  }

  function plusPlayer(name) {
    assistant.sendAction({type: 'plus_player', name})
  }

  function minusPlayer(name) {
    assistant.sendAction({type: 'minus_player', name})
  }

  function deletePlayer(name) {
    assistant.sendAction({type: 'delete_player', name})
  }

  axios.defaults.withCredentials = true;

  async function handleClick() {
    addPlayer(newPlayer);
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
        <Player bind:name bind:level bind:gender
          deleteFunc={() => deletePlayer(name)}
          plusFunc={() => plusPlayer(name)}
          minusFunc={() => minusPlayer(name)}
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