function isObject(obj: any) {
  return typeof obj === 'function' || typeof obj === 'object';
}

export function clone(target: any) {
  const d = {};
  const visited = new WeakSet(); // to avoid circular reference
  
  function merge(target: any, source: any) {
    if (visited.has(source)) {
      return target;
    }
    
    visited.add(source);
    
    for (let key in source) {
      if (isObject(target[key]) && isObject(source[key])) {
        merge(target[key], source[key]);
      } else {
        target[key] = source[key];
      }
    }
    return target;
  }

  return merge(d, target);
}

