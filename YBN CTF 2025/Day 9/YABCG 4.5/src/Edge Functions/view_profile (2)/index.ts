import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const AES_KEY = Deno.env.get("AES_KEY")!;

const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);

function unpad(buf: Uint8Array): Uint8Array {
  const padLen = buf[buf.length - 1];
  return buf.slice(0, buf.length - padLen);
}

async function decrypt(token: string): Promise<string> {
  // Convert base64 token to Uint8Array
  const raw = Uint8Array.from(atob(token), c => c.charCodeAt(0));
  
  const ciphertext = raw
  const iv = new Uint8Array(16)
  
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(AES_KEY),
    { name: "AES-CBC" },
    false,
    ["decrypt"]
  );

  const plaintext = await crypto.subtle.decrypt(
    {
      name: "AES-CBC",
      iv: iv
    },
    key,
    ciphertext
  );

  return new TextDecoder().decode(unpad(new Uint8Array(plaintext)));
}
export const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}
serve(async (req) => {
    if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }
  const { token } = await req.json();

  let plaintext: string;
  try {
    plaintext = await decrypt(token);
  } catch {
    return new Response("Invalid token", { headers:corsHeaders,status: 400 });
  }

  const parts = Object.fromEntries(
    plaintext.split("|").map(p => p.split("="))
  );

  const uid = parts.uid;
  const access = parts.acc;
  
  const exp = parts.exp
  if (!uid || !access) {
    return new Response("Malformed token", {headers:corsHeaders, status: 400 });
  }
  if (exp){
    const expTimestamp = Number(exp); // or parseInt(exp) if it's a string
    
    // Get current time in seconds (Unix timestamp)
    const currentTime = Math.floor(Date.now() / 1000);
    
    // Check if the timestamp has passed
    if (currentTime > expTimestamp) {
        return new Response("expired", { headers:corsHeaders,status: 400 });
    }
    
  }
  let query = supabase
    .from("business_cards")
    .select("*")
    .eq("user_id", uid);
  if (access === "public") {
    query = query.eq("public", true);
  } else if (access !=="private"){
      return new Response("Invalid access state", {status:400,headers:corsHeaders})
  }

  const { data, error } = await query;

  if (error) {
    return new Response(error.message, { status: 500 });
  }

  return new Response(JSON.stringify(data), {
    headers: { "Content-Type": "application/json",...corsHeaders },
  });
});
