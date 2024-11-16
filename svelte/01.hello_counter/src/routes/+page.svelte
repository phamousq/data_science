<script lang="ts">
    let title = "Welcome to SvelteKit";
    import { onMount } from "svelte";
    
    let routes: string[] = [];
    onMount(async () => {
        const response = await fetch('/api/routes');
        routes = await response.json();
    });
</script>

<div class="home">
    <h1>{title}</h1>
    <p>This is a demo application showcasing SvelteKit routing and layouts.</p>

    <h1>Projects (API, SSR)</h1>

    <ol style="">
        {#each routes as route}
            <li>
                <a href="/{route}">{route}
            </li>
        {/each}
    </ol>

</div>

<style>
    .home {
        text-align: left;
        padding: 0.25rem;
    }

    h1 {
        color: #000000;
        font-size: 2rem;
        margin-top: 1rem;
    }

    p {
        color: #444;
        font-size: 1.2rem;
        line-height: 1.6;
    }
</style>
