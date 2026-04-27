const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

/**
 * Supabase Loader: Viral ETL
 * Persiste os resultados das análises no banco de dados.
 */
class SupabaseLoader {
    constructor() {
        this.supabaseUrl = process.env.SUPABASE_URL;
        this.supabaseKey = process.env.SUPABASE_ANON_KEY;
        this.client = createClient(this.supabaseUrl, this.supabaseKey);
    }

    async saveBenchmark(data) {
        console.log(`[SupabaseLoader] Saving benchmark for: ${data.url}`);

        const { data: result, error } = await this.client
            .from('benchmarks')
            .upsert({
                platform: data.platform,
                original_url: data.url,
                author_handle: data.author,
                content_type: data.type || 'video',
                metadata: {
                    title: data.title,
                    description: data.description,
                    imageUrl: data.imageUrl
                },
                analysis: data.intelligence,
                status: 'completed',
                updated_at: new Date().toISOString()
            }, { onConflict: 'original_url' });

        if (error) {
            console.error(`[SupabaseLoader] Error:`, error.message);
            throw error;
        }

        return result;
    }
}

module.exports = SupabaseLoader;
