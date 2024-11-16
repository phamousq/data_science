<script lang="ts">
    class Temperature {
        farenheight: number = $state(32);
        celcius: number = $derived(parseFloat(((this.farenheight - 32) * 5/9).toFixed(2)));

        setFarenheight(f: number) {
            this.farenheight = parseFloat(f.toFixed(2));
        }

        setCelcius(c: number) {
            this.farenheight = (c * 9/5) + 32;
        }
    }
    const temp = new Temperature();
</script>

<div>
    <h1>Farenheight to Celcius</h1>
    <p>
        Farenheight
        <input type="number" value={temp.farenheight} oninput={(e) => temp.setFarenheight(parseFloat(e.currentTarget.value))}>
    </p>
    <p>
        Celcius
        <input type="number" value={temp.celcius} oninput={(e) => temp.setCelcius(parseFloat(e.currentTarget.value))}>
    </p>
</div>

<!-- tips -->

<!-- Derived values should never be updated anywhere in the code -->