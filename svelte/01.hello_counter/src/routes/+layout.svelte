<script lang="ts">
    import { onMount } from 'svelte';
    
    let { children } = $props(); 
    let routes: string[] = $state([]);
    onMount(async () => {
        const response = await fetch('/api/routes');
        routes = await response.json();
    });
</script>

<div class="app">
    <nav>
        <div class="nav-content">
            <div class="logo">
                <a href="/">SvelteKit Demo</a>
            </div>
            <ul class="nav-links">
                <!-- <li><a href="/" class="nav-link">Home</a></li> -->
                {#each routes as route}
                    <li>
                        <a 
                            href="/{route}" 
                            class="nav-link"
                        >
                            {route.charAt(0).toUpperCase() + route.slice(1)}
                        </a>
                    </li>
                {/each}
            </ul>
        </div>
    </nav>

    <main>
        {@render children()}
    </main>
</div>

<style>
    .app {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }

    nav {
        background-color: #ff875f;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .nav-content {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .logo a {
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        text-decoration: none;
    }

    .nav-links {
        display: flex;
        gap: 1.2rem;
        list-style: none;
        margin: 0;
        padding: 0;
    }

    .nav-link {
        color: white;
        text-decoration: none;
        font-size: 1.1rem;
        padding: 0.5rem;
        border-radius: 4px;
        transition: background-color 0.2s;
    }

    .nav-link:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }

    main {
        flex: 1;
        padding: 0rem;
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
    }

    @media (max-width: 768px) {
        .nav-content {
            flex-direction: column;
            gap: 1rem;
        }

        .nav-links {
            flex-direction: column;
            align-items: center;
        }
    }
</style>
