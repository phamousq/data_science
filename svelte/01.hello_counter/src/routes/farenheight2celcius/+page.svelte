<script lang="ts">
    let farenheight: number = $state(32);
    let celcius: number = $state((farenheight - 32) * 5 / 9);

    function updateFarenheight(e: Event) {
        const input = e.currentTarget as HTMLInputElement;
        farenheight = +input.value;
        celcius = +((farenheight - 32) * 5 / 9).toFixed(2);
    }

    function updateCelcius(e: Event) {
        const input = e.currentTarget as HTMLInputElement;
        celcius = +input.value;
        farenheight = +((celcius * 9 / 5) + 32).toFixed(2);
    }

</script>

<div>
    <h1>Farenheight to Celcius</h1>
    <p>
        Farenheight
        <input type="number" value={farenheight} oninput={updateFarenheight}>
        <input type="range" min="32" max="212" value={farenheight} oninput={updateFarenheight}>
    </p>
    <p>
        Celcius
        <input type="number" value={celcius} oninput={updateCelcius}>
        <input type="range" min="{((32 - 32) * 5 / 9)}" max="{((212 - 32) * 5 / 9)}" value={celcius} oninput={updateCelcius}>
        
    </p>
</div>

<!-- tips -->

<!-- Derived values should never be updated anywhere in the code -->