// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-dc0b8095
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import type { CookieOptions } from "hono/utils/cookie";

function isLocalhost(headers: Headers): boolean {
  const host = headers.get("host") || "";
  return host.startsWith("localhost:") || host.startsWith("127.0.0.1:");
}

export function getSessionCookieOptions(headers: Headers): CookieOptions {
  const localhost = isLocalhost(headers);

  return {
    httpOnly: true,
    path: "/",
    sameSite: localhost ? "Lax" : "None",
    secure: !localhost,
  };
}
