import { useFlag } from "./utils";
type Spell = {
	name: string;
	detail: {
		effect: string;
		type: string;
	};
	isSafe: boolean;
};

export function Content({ spell }: { spell: Spell }) {
	const flag = useFlag({ shouldFetch: !spell.isSafe });
	return (
		<main>
			<h1 style={{ textTransform: "uppercase" }}>{spell.name}</h1>
			<div style={{ display: "flex", flexDirection: "column", gap: "0.5em" }}>
				<p style={{ margin: 0 }}>
					<span style={{ fontWeight: "bold" }}>Type:</span> {spell.detail.type}
				</p>
				<p style={{ margin: 0 }}>
					<span style={{ fontWeight: "bold" }}>Effect:</span>{" "}
					{spell.detail.effect}
				</p>
				<p style={{ margin: 0 }}>
					<span style={{ fontWeight: "bold" }}>Safe for use?:</span>{" "}
					{spell.isSafe ? "Yes" : "No."}
				</p>
				{!spell.isSafe && (
					<div style={{ marginTop: "1em" }}>
						<p style={{ margin: 0 }}>
							You must {flag} to cast this spell safely.
						</p>
					</div>
				)}
			</div>
		</main>
	);
}
