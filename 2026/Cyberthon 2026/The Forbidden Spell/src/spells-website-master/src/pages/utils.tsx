import { useEffect, useState } from "react";

export function useFlag({ shouldFetch }: { shouldFetch: boolean }) {
	const [res, setRes] = useState<string>("");
	useEffect(() => {
		const fetchData = async () => {
			if (!shouldFetch) return;
			const loc = new URL(window.location.href);
			const res = await fetch(`/warning?${loc.searchParams.toString()}`);
			setRes((await res.text()) ?? "");
		};

		fetchData();
	}, []);
	return res;
}
