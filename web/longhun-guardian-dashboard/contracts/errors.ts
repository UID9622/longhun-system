// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-01285b4f
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
type AppError = { tag: "app_error"; status: number; message: string };

function appError(status: number, message: string): AppError {
  return { tag: "app_error", status, message };
}

export const Errors = {
  badRequest: (msg: string) => appError(400, msg),
  unauthorized: (msg: string) => appError(401, msg),
  forbidden: (msg: string) => appError(403, msg),
  notFound: (msg: string) => appError(404, msg),
  internal: (msg: string) => appError(500, msg),
} as const;

export type { AppError };
