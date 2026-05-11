import data from "./spells.json" with { type: "json" };

export function Home() {
	return (
		<main>
			<h1>Magic Spell List</h1>
			<p>
				Click on each link to find out more about the spell! Please report any
				errors to me at{" "}
				<a href="https://bsky.app/profile/larry-wizarder.bsky.social">
					@larry-wizarder.bsky.social
				</a>
				.
			</p>
			<ul>
				{data.map((v) => (
					<>
						{v.isSafe && (
							<li key={v.name}>
								<a href={`/${v.name}`}>{v.name}</a>
							</li>
						)}
					</>
				))}
				<li key="moresoon">More coming soon!</li>
			</ul>
		</main>
	);
}
