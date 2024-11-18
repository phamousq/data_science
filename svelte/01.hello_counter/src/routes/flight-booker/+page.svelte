<script lang="ts">
    import type { PageData } from './$types';
    import { onMount } from "svelte";

    let { data }: { data: PageData } = $props();

    let type: "one way"|"round trip" = $state("one way");
    let enabled = $derived(type === "one way" ? false : true)
    let today = $state(new Date().toISOString().split('T')[0])
    let arrival = $state(today)
    let departure = $state(today)
    let valid = $derived(departure <= arrival && departure >= today)

    function readableDate(date: string) {  
        return new Date(date).toISOString().split('T')[0]
    }
    function setDeparture(e: Event) {
        const input = e.currentTarget as HTMLInputElement;
        let a = readableDate(input.value);
        departure = a;
        if (!enabled) {
            arrival = a;
        }
        if (a > arrival) {
            arrival = a;
        }
    }
    function setArrival(e: Event) {
        const input = e.currentTarget as HTMLInputElement;
        let a = readableDate(input.value);
        arrival = a;
        if (a < departure) {
            departure = a;
        }
    }
</script>

<div>
    <h1>Flight Booker</h1>
    <select bind:value={type}>
        <option value="one way">One Way</option>
        <option value="round trip">Round Trip</option>
    </select>
    <!-- <div>enabled: {disabled}</div> -->
    <div>
        <p>
        Departure: 
        <input id="arr" type="date" value={departure} style={!valid ? "background-color: red" : "background-color: white"} oninput={setDeparture}>
        </p>
    </div>
    <div>
        <p>
            Arrival: 
            <input id="dep" type="date" value={arrival} disabled={!enabled} oninput={setArrival}>
        </p>
    </div>
    <p></p>
    <!-- <div>{departure}</div>
    <div>{arrival}</div> -->
    <!-- <p>valid: {valid}</p> -->
</div>

<!-- todo set default date -->
<!-- todo validate dates and change background color of input if invald -->
    <!-- 1: arrival is before today -->
    <!-- 2: arrival is after departure -->
    <!-- 3: departure is before today -->
    <!-- ! struggling with bind:value and oninput -->
<!-- todo understand how to use onMount -->