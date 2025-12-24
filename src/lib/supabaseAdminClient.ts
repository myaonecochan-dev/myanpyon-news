import { createClient } from '@supabase/supabase-js';

// Hardcoded Service Role Key for Admin operations
// WARNING: This key has full access to the database. 
// in a real production app, this should NEVER be exposed to the client bundle.
// Since this is a local/personal demo, we are using it here to simulate admin privileges.

const SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co";
const SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ";

export const supabaseAdmin = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);
