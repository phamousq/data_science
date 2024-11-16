<script lang="ts">
    class Counter {
        count: number = $state(Math.floor(Math.random()*100));
        increment() {
            this.count++;
        }
        decrement() {
            this.count--;
        }
        zero() {
            this.count = 0;
        }
    }
    class Counters {
        lstCounters: Counter[] = $state([new Counter()]);
        lenCounters: number = $derived(this.lstCounters.length);
        sumCounters: number = $derived(this.lstCounters.reduce((a, b) => a + b.count, 0));
        averageCounters: number = $derived(this.lstCounters.reduce((a, b) => a + b.count, 0) / this.lstCounters.length);
    }

    const counters = new Counters();

</script>

<!-- # of counters: {counters.lenCounters}, sum of counters: {counters.sumCounters}, average of counters: {counters.averageCounters} -->
<table border="2">
    <thead class="thead-dark">
    </thead>
    <tbody id="tableBody">
        <tr>
          <td># counters</td>
          <td>{counters.lenCounters}</td>
        </tr>
      <tr>
        <td>sum of counters</td>
        <td>{counters.sumCounters}</td>
      </tr>
      <tr>
        <td>average of counters</td>
        <td>{counters.averageCounters}</td>
      </tr>
    </tbody>
  </table>

<p>
    <button onclick={() => {
        const newCounter = new Counter();
        counters.lstCounters = [...counters.lstCounters, newCounter];
    }}>Push</button>
    <button onclick={() => {
        const newCounter = new Counter();
        counters.lstCounters = [newCounter, ...counters.lstCounters];
    }}>Unshift</button>
    <button onclick="{() => {
        if (counters.lstCounters.length > 0) {
            counters.lstCounters.shift();
        }
    }}">Shift</button>
    <button onclick="{() => {
        if (counters.lstCounters.length > 0) {
            counters.lstCounters.pop();
        }
    }}">Pop</button>
</p>

{#each counters.lstCounters as item, index}
    <p>
        <input type="number" bind:value={item.count} disabled={true}>
        <button onclick={() => item.increment()}>Increment</button>
        <button onclick={() => item.decrement()}>Decrement</button>
        <button onclick={() => item.zero()}>Zero</button>
        <button onclick={() => {
            counters.lstCounters = counters.lstCounters.filter((_, i) => i !== index);
        }}>Remove</button>
    </p>
    
{/each}

<!-- todo  add chart functionality-->