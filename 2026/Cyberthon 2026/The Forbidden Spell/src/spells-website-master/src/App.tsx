import { Home, NotFound, Content } from "./pages";
import data from "./pages/spells.json" with { type: "json" };

const routes = {
	"/": Home,
	...Object.fromEntries(
		data.map((v) => [`/${v.name}`, Content.bind(null, { spell: v })]),
	),
};
export function App() {
	const Render =
		routes[window.location.pathname as keyof typeof routes] ?? NotFound;
	return <Render />;
}

export default App;
