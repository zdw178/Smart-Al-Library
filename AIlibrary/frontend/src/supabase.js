
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://tesgvfyvhwaavqoxmbah.supabase.co'
const supabaseKey = 'sb_publishable_MbA25J-t8DKae2QAg87L0Q_vB9G0Mds'

export const supabase = createClient(supabaseUrl, supabaseKey)

