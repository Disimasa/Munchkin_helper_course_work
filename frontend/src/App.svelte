<script>
  import { onMount} from 'svelte'
  import {createSmartappDebugger, createAssistant} from '@sberdevices/assistant-client'
	export let name;
  let players = [{name: 'Чувак', level: 1}];
  let state = {};
  let token ='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2ZTBlNGU0NjkwNDUzNmZhNTgyYmVhNjU4MDNhYmI5M2VlZjQ3NGVlYTZmNjI1M2IxZDM5ODQ1ZTRhOTYzMDhlNTM5YmU5MjcwMDQyNjI5OCIsImF1ZCI6IlZQUyIsImV4cCI6MTYyMDE0ODY3OSwiaWF0IjoxNjIwMDYyMjY5LCJpc3MiOiJLRVlNQVNURVIiLCJ0eXBlIjoiQmVhcmVyIiwianRpIjoiMzY1MTRlZDctMmE3Yi00NmE1LThhZjAtMjU4NzViN2MzODMzIiwic2lkIjoiMGFmMWNiOWItMTgzOC00ZjFhLWIyY2QtYjM0NTdiNDhhZTUwIn0.ZLmVqcFB2uziBiRGgk6okkfUKIoOPx1_DEX2Ip8pI03vfPsCTMC5JzbirQ4S1iDePwsVMLavobnEtYhOV-oillfWTBmUi40c1R4VaSI9QZjxSB4x6HYMwS_U9P5uRc8TJ-NFjCo5WcWI7uJoJmJbBgmUUnRr90TG6-r1dfkHzy1SkOHwjW6GEtLLgiXon8pe9cnmZ42PbgnZBTl92rLyLYRuvI6q0WmDWW9uI6Yd9QBgYKNd3ghmAZHz58Ru7SF8JZPJAhivR7ZL-5KAun33Op0IIhaJFeRKDuRWRoYRptYqOlGcmkamalLrjPSm8vWpvHT0hRZNqvG1ZDeI4y2VQToqM1lRmhdGo6_cHSjZOqdvmTBFAQqPGOhRb_RPMyTMpTcvgJsMjYKiF9QlXc1jvIzK5e5L-OJE8w0c_JUU-dadiq4ffYjsHWqAsVWo91Y-A_PBhIbjlzmJ2m5PUhAs_q-SO0Vo70oTCYX3xdTlBxzfzM5DmkzEBDqqaETzniKC99JD1MPe7U25WGU_YvEQt1HwlYCxKQsZxZ44VF2jrDU_4Xf-8nFG6rot4LAc2pH8lP-wwdtNRVMi8pa5AvIy2aOoIPNUIL3nToDVhrNpcDIhdv3T9LucamQRmFpIGRs_iq3oehUMsDdyAGRTQJZZtVhzldvinbD53o-okhno2lA';
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