import { serve } from "bun";
import index from "./index.html";

const server = serve({
	routes: {
		"/*": index,

		"/warning": {
			async GET(req) {
				const searchParams = new URL(req.url).searchParams;

				if (searchParams.get("passphrase") !== process.env.passphrase) {
					return new Response("<redacted>", { status: 401 });
				}

				return new Response(
					`trace out the characters for ${process.env.flag}`,
					{ status: 200 },
				);
			},
		},
	},

	development: process.env.NODE_ENV !== "production" && {
		hmr: true,
	},
	port: 80,
});

console.log(`🚀 Server running at ${server.url}`);
