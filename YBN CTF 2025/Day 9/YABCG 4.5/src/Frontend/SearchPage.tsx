import { useState } from "react";
import { supabase} from "../lib/supabase"
export function SearchPage() {
  const [email, setEmail] = useState("");
async function handleSearch() {
  try {
    const { data, error } = await supabase.functions.invoke('mint_token', {
      body: { email }
    });

    if (error) throw error;

    const { token } = data;
    window.location.href = `/profile?token=${encodeURIComponent(token)}`;
  } catch (error) {
    console.error('Error minting token:', error);
    // Handle error appropriately (e.g., show error message to user)
  }
}




  return (

    <div>
      <h1>Profile Lookup</h1>
      <input
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="user@example.com"
      />
      <button onClick={handleSearch}>View Profile</button>
    </div>
  );
}
