(function () {
  'use strict';

  const G = globalThis;
  const { defineProperty, getOwnPropertyDescriptor } = Object;

  const blocked = [
    'atob',
    'btoa',
    'decodeURI',
    'decodeURIComponent',
    'encodeURI',
    'encodeURIComponent',
    'escape',
    'unescape',
    'TextEncoder',
    'TextDecoder',
    'URLSearchParams'
  ];

  const lockValue = (obj, name, msg) => {
    if (name in obj) {
      try {
        defineProperty(obj, name, {
          configurable: false,
          writable: false,
          enumerable: false,
          value: function () { throw new Error(msg || (name + ' is disabled')); }
        });
      } catch (_) {}
    }
  };

  const lockMethod = (obj, name, msg) => {
    const d = getOwnPropertyDescriptor(obj, name);
    if (!d || typeof d.value !== 'function') return;
    try {
      defineProperty(obj, name, {
        configurable: false,
        writable: false,
        enumerable: !!d.enumerable,
        value: function () { throw new Error(msg || (name + ' is disabled')); }
      });
    } catch (_) {}
  };

  for (const name of blocked) lockValue(G, name, name + ' is disabled');

  lockValue(G, 'Function', 'Function constructor is disabled');
  if (G.Function && G.Function.prototype) {
    try {
      defineProperty(G.Function.prototype, 'constructor', {
        configurable: false,
        writable: false,
        enumerable: false,
        value: function () { throw new Error('Function constructor is disabled'); }
      });
    } catch (_) {}
  }

  ['Worker', 'SharedWorker', 'ServiceWorker', 'BroadcastChannel', 'MessageChannel']
    .forEach(name => lockValue(G, name, name + ' is disabled'));

  if ('document' in G && G.document && typeof G.document.createElement === 'function') {
    const origCreateElement = G.document.createElement;
    try {
      defineProperty(G.document, 'createElement', {
        configurable: false,
        writable: false,
        enumerable: false,
        value: function (tagName, ...args) {
          const t = String(tagName).toLowerCase();
          if (t === 'iframe') throw new Error('iframe creation is disabled');
          return origCreateElement.call(this, tagName, ...args);
        }
      });
    } catch (_) {}
    if (typeof G.document.write === 'function') lockMethod(G.document, 'write', 'document.write is disabled');
    if (typeof G.document.writeln === 'function') lockMethod(G.document, 'writeln', 'document.writeln is disabled');
  }

  if ('HTMLIFrameElement' in G && G.HTMLIFrameElement && G.HTMLIFrameElement.prototype) {
    try {
      defineProperty(G.HTMLIFrameElement.prototype, 'src', {
        configurable: false,
        set() { throw new Error('iframe creation is disabled'); }
      });
    } catch (_) {}
  }

  if ('Element' in G && G.Element && G.Element.prototype) {
    try {
      defineProperty(G.Element.prototype, 'innerHTML', {
        configurable: false,
        set() { throw new Error('innerHTML is disabled'); }
      });
    } catch (_) {}
    if ('insertAdjacentHTML' in G.Element.prototype) {
      lockMethod(G.Element.prototype, 'insertAdjacentHTML', 'insertAdjacentHTML is disabled');
    }
  }
})();
