<script>
  const trickyNames = ['Дим', 'Степ', 'Ир'];
  export let gender, level, name;
  let refactoredName = name.charAt(0).toUpperCase() + name.slice(1);
  trickyNames.forEach((el) => {
    if (el === refactoredName) refactoredName += 'а';
  })
  export let deleteFunc = () => {
  };
  export let plusFunc = () => {
  };
  export let minusFunc = () => {
  };
  let focused = false;

  function plus() {
    if (level < 10) {
      plusFunc()
    }
  }

  function minus() {
    if (level > 1) {
      minusFunc()
    }
  }

  function focus() {
    focused = true;
  }

  function blur() {
    focused = false
  }
</script>

<div class="player" on:mouseenter={focus} on:mouseleave={blur}>
  <button class="delete-button" on:click={deleteFunc}>
    <svg width="30" height="30" class="delete-icon">
      <line x1="10" x2="20" y1="15" y2="15"></line>
      <line x1="15" x2="15" y1="10" y2="20"></line>
    </svg>
  </button>
  <input type="text" class="name" bind:value={refactoredName} on:focus on:blur>
  <button class="gndr-button" on:click={() => gender === 'male' ? gender = 'female': gender = 'male'}>
    {#if gender === 'male'}
      <img src="./icons/mars.svg" alt="Male">
    {:else}
      <img src="./icons/femenine.svg" alt="Female">
    {/if}
  </button>
  <button class="minus lvl-button" disabled={level === 1} on:click={minus}>
    <svg width="30" height="30">
      <line x1="10" x2="20" y1="15" y2="15"></line>
    </svg>
  </button>
  <p class="level">{level}</p>
  <button class="plus lvl-button" disabled={level === 10} on:click={plus}>
    <svg width="30" height="30">
      <line x1="10" x2="20" y1="15" y2="15"></line>
      <line x1="15" x2="15" y1="10" y2="20"></line>
    </svg>
  </button>
</div>

<style>
  p {
    color: #1A394C;
    user-select: none;
    margin: 0;
  }

  button {
    cursor: pointer;
  }

  button:hover {
    border: 1px solid #333333;
  }

  .hidden {
    opacity: 0;
  }

  img {
    width: 17px;
    height: 17px;
  }

  line {
    color: #333333;
    stroke: currentColor;
  }

  .delete-icon line {
    stroke: #EF2D56;
  }

  .player {
    margin-top: 10px;
    padding: 5px 0;
    display: flex;
    align-items: center;
    justify-content: space-evenly;
    width: 90%;
    max-width: 400px;
  }

  .name {
    flex-grow: 2;
    width: 50px;
    border: none;
    padding: 0;
    margin: 0;
    color: #272C54;
    font-family: 'Raleway', sans-serif;
    font-size: 20px;
    font-weight: 400;
  }

  .level {
    width: 30px;
    text-align: center;
    cursor: default;
    color: #47509A;
    font-family: 'Raleway', sans-serif;
    font-weight: 600;
    font-size: 20px;
  }

  .lvl-button, .gndr-button, .delete-button {
    line-height: 0;
    margin: 0;
    padding: 0;
    width: 31px;
    height: 31px;
    border-radius: 20px;
    background: transparent;
    box-shadow: 0 0 10px 1px rgba(60, 60, 60, 0.1);
    border-color: #cbcbcb;
    transition: background 0.7s ease;
  }

  .lvl-button:disabled {
    cursor: default;
    background: rgba(210, 210, 210, 0.3);
  }

  .gndr-button {
    margin: 0 20px 0 5px;
    border-radius: 5px;
  }

  .delete-button {
    background: none;
    border-color: #EF2D56;
    border-radius: 5px;
    margin-right: 5px;
    /*opacity: 0;*/
    transition: opacity 0.5s ease;
  }

  .delete-button:hover {
    box-shadow: 0px 0px 3px 1px #EF2D56;
    border-color: #EF2D56 !important;
  }

  .delete-icon {
    transform: rotate(45deg);
  }

  .delete-button {
    width: 30px;
    height: 30px;
  }
</style>