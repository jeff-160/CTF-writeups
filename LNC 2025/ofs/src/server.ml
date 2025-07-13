(* Custom equality comparator with built-in anti-ddos :D *)
let ( = ) l r =
  let open Lwt.Infix in
  let rec cmp i =
    if i = String.length l && i = String.length r then Lwt.return true
    else
    if i < String.length l && i < String.length r then (
      if l.[i] <> r.[i] then (
        Lwt_unix.sleep 1.0 >>= fun () -> cmp (i + 1)
      ) else cmp (i + 1)
    ) else Lwt.return false
  in cmp 0

(* Looks for matching files using the custom operator *)
let find_matching_file requested_file =
  let requested_lower = String.lowercase_ascii requested_file in
  Lwt_list.find_s (fun f -> (String.lowercase_ascii f = requested_lower)) Files.file_list

(* Serves the file if its found, else send a `404` *)
let serve_file req =
  match Dream.param req "filename" with
    | exception _ -> Dream.empty `Not_Found
    | filename ->
      let open Lwt.Syntax in
      let* matched_file = find_matching_file filename in
      let lowercase_file = String.lowercase_ascii matched_file in
      match Files.read lowercase_file with
      | None -> Dream.empty `Not_Found
      | Some content -> Dream.respond ~headers:["Content-Type", "text/plain"] content

(* Error template logic (includes `404` responses) *)
let error_template _error _debug_info suggested_response =
  let status = Dream.status suggested_response in
  let code = Dream.status_to_int status
  and reason = Dream.status_to_string status in

  Dream.set_header suggested_response "Content-Type" Dream.text_html;
  Dream.set_body suggested_response (Error.render code reason);

  Lwt.return suggested_response

(* Render the index page from a template *)
let index _ =
  Index.render  (* The `Index` module refers to the HTML source of the index page *)
  |> Dream.html

(* Run the main server *)
let () =
  Dream.run ~error_handler:(Dream.error_template error_template) ~interface:"0.0.0.0"
  @@ Dream.logger
  @@ Dream.router [
    Dream.get "/" index;
    Dream.get "/:filename" serve_file;
  ]
