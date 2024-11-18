<script lang="ts">
    class Temperature {
        farenheight: number = $state(32);
        celcius: number = $derived(parseFloat(((this.farenheight - 32) * 5/9).toFixed(2)));
        celcius2: number = $state(parseFloat(((this.farenheight - 32) * 5/9).toFixed(2)))

        setFarenheight(f: number) {
            this.farenheight = parseFloat(f.toFixed(2));
        }

        setCelcius(c: number) {
            this.farenheight = (c * 9/5) + 32;
        }

        updateFarenheight(e){
            this.farenheight = +e.target.value
            this.celcius2 = +((this.farenheight - 32) * 5/9).toFixed(2)
        }

        updateCelcius(e){
            this.celcius2 = +e.target.value
            this.farenheight = +((this.celcius2 * 9/5) + 32).toFixed(2)
        }

    }
    const temp = new Temperature();
</script>

<div>
    <h1>Farenheight to Celcius</h1>
    <p>
        Farenheight
        <input type="number" value={temp.farenheight} oninput={(e) => temp.updateFarenheight(e)}>
    </p>
    <p>
        Celcius
        <input type="number" value={temp.celcius2} oninput={(e) => temp.updateCelcius(e)}>
    </p>
</div>

<!-- tips -->

<!-- Derived values should never be updated anywhere in the code -->