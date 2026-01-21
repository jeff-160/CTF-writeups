import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const AES_KEY = Deno.env.get("AES_KEY")!; // 16 bytes

const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);

function pad(buf: Uint8Array): Uint8Array {
  const padLen = 16 - (buf.length % 16);
  return new Uint8Array([...buf, ...Array(padLen).fill(padLen)]);
}
async function encrypt(plaintext: string): Promise<string> {
  console.log("pt",plaintext)
  const iv = new Uint8Array(16)
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(AES_KEY),
    { name: "AES-CBC" },
    false,
    ["encrypt"]
  );

  const padded = pad(new TextEncoder().encode(plaintext));
  console.log("padenc", padded)
  const ciphertext = await crypto.subtle.encrypt(
    { name: "AES-CBC", iv },
    key,
    padded
  );
  
  
  return btoa(String.fromCharCode(...new Uint8Array(ciphertext)));

}
export const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
      
}
serve(async (req) => {
  if (req.method === 'OPTIONS') {
        return new Response('ok', { headers: corsHeaders })
          }
  
  const { email, exp } = await req.json();

  const authHeader = req.headers.get("Authorization");
  let access = "public";

  if (authHeader) {
    const jwt = authHeader.replace("Bearer ", "");
    const { data } = await supabase.auth.getUser(jwt);
    if (data.user?.email === email) {
      access ="private";
    }
  }

const { data, error } = await supabase
  .from('users')//RLS restricts this to service_role
  .select('id')
  .eq('email', email)
  .single();
  
  // If exp isnt available we just dont use it.
  let expfield
  if (exp){
      expfield = `exp=${exp}|`
  } else {
      expfield =""
  }
  console.log("uid", data.id)
  const tokenPlaintext = `acc=${access}|${expfield}uid=${data.id}`;

  const token = await encrypt(tokenPlaintext);

  return new Response(JSON.stringify({ token }), {
    headers: {...corsHeaders, "Content-Type": "application/json" },
  });
});
