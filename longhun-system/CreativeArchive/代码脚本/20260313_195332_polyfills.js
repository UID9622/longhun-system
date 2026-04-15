// globals.js
if (typeof globalThis.fetch !== 'function') {
    const { fetch, Headers, Request, Response, FormData, Blob, File } = require('node-fetch');
    globalThis.fetch = fetch;
    globalThis.Headers = Headers;
    globalThis.Request = Request;
    globalThis.Response = Response;
    globalThis.FormData = FormData;
    globalThis.Blob = Blob;
    globalThis.File = File;
}