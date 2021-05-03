<script>
  import { onMount} from 'svelte'
  import {createSmartappDebugger, createAssistant} from '@sberdevices/assistant-client'
	export let name;
  let players = [{name: 'Чувак', level: 1}];
  let state = {};
  let token =''; // <- сюда токен
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
        getState
      })
      // return createAssistant({getState});
    }
    let assistant = init();

    assistant.on("start", (event) => {
      console.log(`assistant.on(start)`, event);
    });

    assistant.on("data", (event) => {
      console.log(event);
      if (event.action) {
        dispatchAction(event.action);
      }
    });
  })

  function dispatchAction(action) {
    switch (action.type) {
      case 'add_player':
        addPlayer(action.name);
      break

      case 'delete_player':

      break
    }
  }

  function addPlayer(name) {
    players = [...players, {name, level: 1}];
  }
</script>

<main>
  {#each players as player}
    <p>{player.name}</p>
  {/each}
</main>

<style>
	#log {
    color: #ff3e00;
  }
</style>