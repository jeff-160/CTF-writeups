// =============================================================================
// sentinel — DECOMPILED / RECONSTRUCTED SOURCE
// Binary:   sentinel (ELF 64-bit, x86-64, statically linked, Go, not stripped)
// BuildID:  AS1c67nlth4kjnq8uRHI/hV_k5tDtJ-AnaNKLNo02/...
// Method:   symbol table (nm), DWARF debug info, disassembly (objdump),
//           embedded string extraction
//
// Packages identified:
//   main                  — entry point, config, HTTP wiring
//   sentinel/handlers     — HTTP handler methods on *Server
//   sentinel/crypto       — token create / sign / verify logic
//
// Third-party deps:
//   github.com/tidwall/gjson   — JSON field extraction
//   github.com/tidwall/match   — pattern matching (used by gjson)
//   github.com/tidwall/pretty  — JSON pretty-print (used by gjson)
// =============================================================================

package main

import (
	"crypto/hmac"
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"

	"github.com/tidwall/gjson"
	// sentinel/crypto and sentinel/handlers are sub-packages of this module
)

// ---------------------------------------------------------------------------
// Config holds runtime configuration loaded from environment variables.
// ---------------------------------------------------------------------------
type Config struct {
	// Raw bytes of the HMAC secret key (derived from HMAC_SECRET env var,
	// or a freshly generated random hex string if the var is absent).
	HMACSecret []byte // env: HMAC_SECRET  (falls back to generateRandomHex(32))

	// Base URL of the downstream "Arcanum" service.
	// env: ARCANUM_URL  (default: "http://localhost:21337")  ← placeholder default
	ArcanumURL string

	// TCP port this server listens on.
	// env: PORT  (default: "3001")
	Port string
}

// ---------------------------------------------------------------------------
// main.LoadConfig  (0x671bc0)
// ---------------------------------------------------------------------------
func LoadConfig() *Config {
	hmacSecret := os.Getenv("HMAC_SECRET") // length 11
	if hmacSecret == "" {
		log.Println("HMAC_SECRET not set; generating random secret")
		hmacSecret = generateRandomHex(32)
	}

	arcanumURL := os.Getenv("ARCANUM_URL") // length 11
	if arcanumURL == "" {
		arcanumURL = "http://localhost:21337" // 21 chars — placeholder; exact default unclear
	}

	port := os.Getenv("PORT") // length 4
	if port == "" {
		port = "3001"
	}

	return &Config{
		HMACSecret: []byte(hmacSecret),
		ArcanumURL: arcanumURL,
		Port:       port,
	}
}

// ---------------------------------------------------------------------------
// main.generateRandomHex  (0x671e20)
//
// Allocates n random bytes via crypto/rand, then hex-encodes them into a
// 2n-character string using the charset "0123456789abcdef".
// ---------------------------------------------------------------------------
func generateRandomHex(n int) string {
	buf := make([]byte, n)
	if _, err := rand.Read(buf); err != nil {
		log.Fatal(err)
	}

	const hexChars = "0123456789abcdef"
	out := make([]byte, n*2)
	for i, b := range buf {
		out[i*2] = hexChars[b>>4]
		out[i*2+1] = hexChars[b&0xf]
	}
	return string(out)
}

// ---------------------------------------------------------------------------
// main.main  (0x671f60)
//
// Wires up three HTTP routes then starts the server.
// ---------------------------------------------------------------------------
func main() {
	cfg := LoadConfig()

	srv := &handlers.Server{Config: cfg}

	// POST /api/rune/issue        → IssueRune
	http.Handle("/api/rune/issue", http.HandlerFunc(srv.IssueRune))

	// POST /api/rune/issue_s_rank → IssueSRankRune
	http.Handle("/api/rune/issue_s_rank", http.HandlerFunc(srv.IssueSRankRune))

	// POST /api/portal/warp       → WarpPortal
	http.Handle("/api/portal/warp", http.HandlerFunc(srv.WarpPortal))

	fmt.Printf("🛡️  Sentinel starting on port %s\n", cfg.Port)
	fmt.Printf("   Arcanum URL: %s\n", cfg.ArcanumURL)

	if err := http.ListenAndServe(":"+cfg.Port, nil); err != nil {
		log.Fatal(err)
	}
}

// =============================================================================
// Package sentinel/handlers
// =============================================================================

package handlers

import (
	"encoding/json"
	"io"
	"net/http"

	"sentinel/crypto"
)

// Server holds shared dependencies injected into all handlers.
type Server struct {
	Config *main.Config
}

// ---------------------------------------------------------------------------
// RuneRequest is the JSON body expected by IssueRune and IssueSRankRune.
// ---------------------------------------------------------------------------
type RuneRequest struct {
	Rune string `json:"rune"` // confirmed by DWARF field name "runeAt"
}

// ---------------------------------------------------------------------------
// (*Server).IssueRune  (0x670400)
//
// POST /api/rune/issue
//
// Flow:
//  1. Reject non-POST requests (405).
//  2. Read and JSON-decode the request body into RuneRequest.
//  3. Call crypto.CreateRuneToken to sign the rune.
//  4. Forward the signed body as a POST to cfg.ArcanumURL + "/api/rune/issue"
//     using the default http.Client.
//  5. Pipe the Arcanum response status / body back to the caller.
// ---------------------------------------------------------------------------
func (s *Server) IssueRune(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed) // 405 = 0x195
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		// error path observed in disasm: writes error and returns
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	var req RuneRequest
	if err := json.Unmarshal(body, &req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Sign the rune using the HMAC key and arcanum URL as context
	token, err := crypto.CreateRuneToken(
		req.Rune,
		s.Config.HMACSecret,
		s.Config.ArcanumURL,
	)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Forward to Arcanum — response status must be 200 (0xc8)
	resp, err := http.Post(
		s.Config.ArcanumURL+"/api/rune/issue", // "/api/rune/issue" = 0xf chars
		"application/json",                    // 16 chars observed
		bytes.NewReader(body),
	)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	// IssueRune.func1 (0x670b80) — closure that copies response body
	io.Copy(w, resp.Body)
}

// ---------------------------------------------------------------------------
// (*Server).IssueSRankRune  (0x670be0)
//
// POST /api/rune/issue_s_rank
//
// Identical flow to IssueRune but targets the "/api/rune/issue_s_rank"
// downstream endpoint.  (The "S-rank" variant likely carries elevated
// privileges or a different token claim.)
// ---------------------------------------------------------------------------
func (s *Server) IssueSRankRune(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	var req RuneRequest
	if err := json.Unmarshal(body, &req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	token, err := crypto.CreateRuneToken(
		req.Rune,
		s.Config.HMACSecret,
		s.Config.ArcanumURL,
	)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	resp, err := http.Post(
		s.Config.ArcanumURL+"/api/rune/issue_s_rank",
		"application/json",
		bytes.NewReader(body),
	)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	// IssueSRankRune.func1 (0x671300) — response copy closure
	io.Copy(w, resp.Body)
}

// ---------------------------------------------------------------------------
// (*Server).WarpPortal  (0x671360)
//
// POST /api/portal/warp
//
// Verifies an inbound rune token then proxies to Arcanum's warp endpoint.
// ---------------------------------------------------------------------------
func (s *Server) WarpPortal(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Verify the token carried in the request before forwarding
	dest, nonce, err := crypto.VerifyRuneToken(
		string(body),
		s.Config.HMACSecret,
		s.Config.ArcanumURL,
	)
	if err != nil {
		http.Error(w, err.Error(), http.StatusUnauthorized)
		return
	}

	resp, err := http.Post(
		s.Config.ArcanumURL+"/api/portal/warp",
		"application/json",
		bytes.NewReader(body),
	)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	// WarpPortal.func1 (0x671a00) — response copy closure
	_ = dest
	_ = nonce
	io.Copy(w, resp.Body)
}

// =============================================================================
// Package sentinel/crypto
// =============================================================================

package crypto

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
	"fmt"

	"github.com/tidwall/gjson"
)

// ---------------------------------------------------------------------------
// ExtractDestinationAndNonce  (0x66fb40)
//
// Parses a JSON payload and extracts two fields using gjson:
//   - "destination"  (11 chars)
//   - "nonce"        (5 chars)
//
// Returns (destination, nonce, error).
// Error cases:
//   "nonce field not found"       — nonce JSON value is zero/absent
//   "destination field not found" — destination JSON value is zero/absent
// ---------------------------------------------------------------------------
func ExtractDestinationAndNonce(payload string) (destination, nonce string, err error) {
	destResult := gjson.Get(payload, "destination")
	nonceResult := gjson.Get(payload, "nonce")

	if destResult.Type == 0 && nonceResult.Type == 0 {
		return "", "", fmt.Errorf("destination field not found")
	}
	if nonceResult.Type == 0 {
		return "", "", fmt.Errorf("nonce field not found")
	}

	return destResult.String(), nonceResult.String(), nil
}

// ---------------------------------------------------------------------------
// SignRune  (0x66fe80)
//
// Creates an HMAC-SHA256 signature over a canonical string of the form
//
//   "<destination>.<nonce>"          (format string: "%s.%s")
//
// The HMAC is keyed with `key` and the result is base64url-encoded
// (no padding — RawURLEncoding).
//
// The debug log line emitted reads:
//   "destination=%s\nnonce=%s\n"
// ---------------------------------------------------------------------------
func SignRune(destination, nonce string, key []byte) string {
	canonical := fmt.Sprintf("%s.%s", destination, nonce)

	mac := hmac.New(sha256.New, key)
	mac.Write([]byte(canonical))
	sig := mac.Sum(nil)

	return base64.RawURLEncoding.EncodeToString(sig)
}

// ---------------------------------------------------------------------------
// CreateRuneToken  (0x670020)
//
// High-level function called by the handlers to mint a new signed token.
//
//  1. Extract destination + nonce from the JSON payload.
//  2. Sign them with SignRune.
//  3. Base64url-encode the original payload.
//  4. Return "<encoded_payload>.<signature>" (format: "%s.%s").
//
// Returns (token string, error).
// ---------------------------------------------------------------------------
func CreateRuneToken(payload string, key []byte, _ string) (string, error) {
	dest, nonce, err := ExtractDestinationAndNonce(payload)
	if err != nil {
		return "", err
	}

	sig := SignRune(dest, nonce, key)
	encodedPayload := base64.RawURLEncoding.EncodeToString([]byte(payload))

	// Final token: "<base64url(payload)>.<signature>"
	return fmt.Sprintf("%s.%s", encodedPayload, sig), nil
}

// ---------------------------------------------------------------------------
// VerifyRuneToken  (0x6701a0)
//
// Verifies a token produced by CreateRuneToken.
//
//  1. Split token on "." into exactly 2 parts (errors: "invalid rune format").
//  2. Base64url-decode part[0] → raw payload.
//  3. Extract destination + nonce from the decoded payload.
//  4. Re-compute the HMAC signature.
//  5. Constant-time compare the provided signature (part[1]) against computed.
//     - Length mismatch            → return (payload, "", error)       [eax=0]
//     - Bytes differ               → "invalid signature"               [eax≠1]
//     - Match                      → return (dest, nonce, nil)         [eax=1]
//
// Error strings observed:
//   "invalid rune format"    — split did not produce exactly 2 parts
//   "invalid payload encoding" — base64 decode of part[0] failed
//   "invalid signature"      — HMAC mismatch
// ---------------------------------------------------------------------------
func VerifyRuneToken(token string, key []byte, arcanumURL string) (payload, nonce string, err error) {
	parts := strings.SplitN(token, ".", 2)
	if len(parts) != 2 {
		return "", "", fmt.Errorf("invalid rune format")
	}

	rawPayload, decErr := base64.RawURLEncoding.DecodeString(parts[0])
	if decErr != nil {
		return "", "", fmt.Errorf("invalid payload encoding")
	}

	dest, nonceVal, extractErr := ExtractDestinationAndNonce(string(rawPayload))
	if extractErr != nil {
		return "", "", extractErr
	}

	expected := SignRune(dest, nonceVal, key)
	provided := parts[1]

	// Constant-time comparison (XOR-accumulate loop observed in disasm)
	if len(expected) != len(provided) {
		return string(rawPayload), "", fmt.Errorf("invalid signature")
	}
	var diff byte
	for i := range expected {
		diff |= expected[i] ^ provided[i]
	}
	if diff != 0 {
		return "", "", fmt.Errorf("invalid signature")
	}

	return string(rawPayload), nonceVal, nil
}