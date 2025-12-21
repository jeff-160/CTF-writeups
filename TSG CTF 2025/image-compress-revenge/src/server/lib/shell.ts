import { spawn } from "bun";

export async function run(command: string) {
  const proc = spawn(["bash", "-c", command], {
    stderr: "pipe",
  });
  await proc.exited;
  if (proc.exitCode !== 0) {
    const err = await new Response(proc.stderr).text();
    throw new Error(`Shell command failed: \n${err}`);
  }
  const stdout = await new Response(proc.stdout).text();
  return stdout;
}
