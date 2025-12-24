import { createClient } from '@supabase/supabase-js';

// Hardcoded for now due to .env restrictions in this environment
// In production, these should be environment variables
const SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co";
const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ";

export const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
