<script>
    let currentYear = new Date().getFullYear();
</script>

<div class="about-page">
    <h1>About Us</h1>
    
    <section class="content">
        <h2>Welcome to Our Project</h2>
        <p>This is a demo Svelte application showcasing routing and state management.</p>
        
        <h3>Features</h3>
        <ul>
            <li>Dynamic route generation</li>
            <li>State management with Svelte</li>
            <li>Server-side API endpoints</li>
            <li>Responsive design</li>
        </ul>
    </section>

    <footer>
        <p>© {currentYear} My Svelte Project. All rights reserved.</p>
    </footer>
</div>

<style>
    .about-page {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }

    .content {
        margin: 2rem 0;
    }

    h1 {
        color: #ff3e00;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    h2 {
        color: #444;
        font-size: 1.8rem;
        margin: 1.5rem 0;
    }

    h3 {
        color: #666;
        font-size: 1.4rem;
        margin: 1rem 0;
    }

    ul {
        list-style-type: disc;
        margin-left: 2rem;
    }

    li {
        margin: 0.5rem 0;
    }

    footer {
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
        color: #666;
        font-size: 0.9rem;
    }
</style>
