import { createClient } from '@supabase/supabase-js';

// Validated credentials from user
const SUPABASE_URL = 'https://ufawzveswbnaqvfvezbb.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY1NTI0MjcsImV4cCI6MjA4MjEyODQyN30.AxihQaKViHj-e-3fkuWcgKm3-H1cmon4bazka4qEmog';

export const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
