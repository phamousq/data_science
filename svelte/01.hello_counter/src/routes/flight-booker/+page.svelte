<script lang="ts">
    import type { PageData } from './$types';
    import { onMount } from "svelte";

    let { data }: { data: PageData } = $props();

    class FlightBooker {
        type: "one way"|"round trip" = $state("one way");
        disabled = $derived(
            this.type === "one way" ? true : false)
        arrival = $state(new Date().toISOString().split('T')[0])
        departure = $state(new Date().toISOString().split('T')[0])
        valid = $derived(
            this.departure >= this.arrival ? true : false 
        )
        setArrival(a: string) {
            this.arrival = a;
            this.departure = a;
        }
    }
    let gui = new FlightBooker();

    onMount(() => {
        let a = document.getElementById("arr"); 
    })
</script>

<div>
    <h1>Flight Booker</h1>
    <select bind:value={gui.type}>
        <option value="one way">One Way</option>
        <option value="round trip">Round Trip</option>
    </select>
    <!-- <div>enabled: {gui.disabled}</div> -->
    <div>
        <p>
        Departure: 
        <input id="arr" type="date" value={gui.departure} style={(gui.valid)===false ? "background-color: red" : "background-color: white"} oninput={(e) => gui.setArrival(new Date(e.currentTarget.value))}>
        </p>
    </div>
    <div>
        <p>
            Arrival: 
            <input id="dep" type="date" bind:value={gui.arrival} disabled={gui.disabled}>
        </p>
    </div>
    <p></p>
    <div>{gui.departure}</div>
    <div>{gui.arrival}</div>
    <p>valid
        {gui.valid}
    </p>
</div>

<!-- todo set default date -->
<!-- todo validate dates and change background color of input if invald -->
    <!-- 1: arrival is before today -->
    <!-- 2: arrival is after departure -->
    <!-- 3: departure is before today -->
    <!-- ! struggling with bind:value and oninput -->
<!-- todo understand how to use onMount -->