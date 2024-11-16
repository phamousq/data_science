import { json } from '@sveltejs/kit';
import fs from 'node:fs';
import path from 'node:path';

export async function GET() {
    const routesDir = path.join(process.cwd(), 'src', 'routes');
    
    function getRoutes(dir: string) {
        const files = fs.readdirSync(dir);
        const routes = [];
        
        for (const file of files) {
            const fullPath = path.join(dir, file);
            const stat = fs.statSync(fullPath);
            
            if (stat.isDirectory()) {
                // Skip api and internal directories
                if (!file.startsWith('api') && !file.startsWith('_')) {
                    routes.push(file);
                }
            }
        }
        
        return routes;
    }
    
    const routes = getRoutes(routesDir);
    return json(routes);
}
