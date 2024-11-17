<script lang="ts">
    import { onMount } from "svelte";
    
    let routes: string[] = [];
    onMount(async () => {
        const response = await fetch('/api/routes');
        routes = await response.json();
    });

</script>

<div>
    <h1>Projects (API, SSR)</h1>

    <ol style="">
        {#each routes as route}
            <li>
                <a href="/{route}">{route}</a>
            </li>
        {/each}
    </ol>
</div>

<style>

</style>