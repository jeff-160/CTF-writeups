export const resolve = (specifier, context, nextResolve) => {
    if (specifier.startsWith("./") || specifier.startsWith("../")) {
      if (
        !(
          specifier.endsWith(".js") ||
          specifier.endsWith(".mjs") ||
          specifier.endsWith(".cjs")
        )
      ) {
        if (specifier.endsWith("/")) {
          const newSpecifier = specifier + "index.js";
          return nextResolve(newSpecifier, context);
        }
        const newSpecifier = specifier + ".js";
        return nextResolve(newSpecifier, context);
      }
    }
    return nextResolve(specifier, context);
  };