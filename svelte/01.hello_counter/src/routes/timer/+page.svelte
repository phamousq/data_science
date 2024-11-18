<script lang="ts">
    const zeroPad = (num:number, places:number) => String(num).padStart(places, '0')

    let seconds = $state(0);
    // let miliseconds = $derived(Math.floor(seconds * 1000));
    let minutes = $derived(Math.floor(seconds / 60));
    let timerSeconds = $derived(zeroPad(seconds % 60, 2));
    let timerMinutes = $derived(zeroPad(minutes % 60, 2));  

    function setTimer(e: Event) {
        const input = e.currentTarget as HTMLInputElement;
        seconds = +input.value;
    }

    function myFunction() {
        setTimeout(() => {
            alert('Hello');
        }, seconds * 1000);
    }
</script>

<div>
    <h1>Timer</h1>
    <button onclick={myFunction}>Try it</button>

    <input type="number" value={seconds} oninput={setTimer}> 

    {timerMinutes}:{timerSeconds}
</div>

<style>

</style>