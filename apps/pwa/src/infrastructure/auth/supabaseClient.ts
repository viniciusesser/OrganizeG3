import {
    createClient,
} from "@supabase/supabase-js";
import type {
    SupabaseClient,
} from "@supabase/supabase-js";

import {
    requireSupabaseBrowserConfiguration,
} from "@/infrastructure/environment/environment";

let cachedClient:
    SupabaseClient | null = null;

export function getSupabaseClient():
    SupabaseClient {
    if (cachedClient !== null) {
        return cachedClient;
    }

    const configuration =
        requireSupabaseBrowserConfiguration();

    cachedClient = createClient(
        configuration.url,
        configuration.anonKey,
        {
            auth: {
                autoRefreshToken: true,
                persistSession: true,
                detectSessionInUrl: true,
            },
        },
    );

    return cachedClient;
}

export function resetSupabaseClientForTests():
    void {
    cachedClient = null;
}