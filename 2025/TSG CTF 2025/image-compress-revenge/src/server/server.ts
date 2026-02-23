import { Elysia, t } from "elysia";
import { unlink } from "fs/promises";
import { run } from "./lib/shell.ts";

const CHARS_TO_ESCAPE = "$'\"(){}[]:;/&`~|^!? \n".split("");

export function escape(source: string): string {
	let s = source;
	for (const char of CHARS_TO_ESCAPE) {
		s = s.replaceAll(char, "\\" + char);
	}
	return s;
}

const app = new Elysia()
	.get("/", () => {
		return Bun.file("./public/index.html");
	})
	.post(
		"/compress",
		async ({ body, set }) => {
			const { image, quality } = body;

			if (image.name.includes("..")) {
				throw new Error(`Invalid file name: ${image.name}`);
			}

			const inputPath = `./tmp/inputs/${escape(image.name)}`;
			const outputPath = `./tmp/outputs/${escape(image.name)}`;
			console.log(escape(image.name));

			try {
				await Bun.write(inputPath, image);

				await run(
					`magick "${inputPath}" -quality ${quality} -strip "${outputPath}"`,
				);

				const compressed = await Bun.file(outputPath).arrayBuffer();

				set.headers["Content-Type"] = image.type;
				set.headers["Content-Disposition"] =
					`attachment; filename="${image.name}"`;

				return new Response(compressed);
			} catch (error) {
				set.status = 500;
				return { error: `Failed to compress image: ${error}` };
			} finally {
				await unlink(inputPath).catch(() => {});
				await unlink(outputPath).catch(() => {});
			}
		},
		{
			body: t.Object({
				image: t.File({
					"file-type": "image/*",
					maxSize: "10m",
				}),
				quality: t.Numeric({
					minimum: 1,
					maximum: 100,
					default: 85,
				}),
			}),
		},
	);

app.listen(process.env.PORT ?? "3000", (server) => {
	console.log(
		`🦊 server is running at http://${server.hostname}:${server.port}`,
	);
});
