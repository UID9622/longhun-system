// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-3ce81ae1
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { authRouter } from "./auth-router";
import { adminRouter } from "./routers/admin-router";
import { paymentRouter } from "./routers/payment-router";
import { intakeRouter } from "./routers/intake-router";
import { guardianRouter } from "./routers/guardian-router";
import { createRouter, publicQuery } from "./middleware";

export const appRouter = createRouter({
  ping: publicQuery.query(() => ({ ok: true, ts: Date.now() })),
  auth: authRouter,
  admin: adminRouter,
  payment: paymentRouter,
  intake: intakeRouter,
  guardian: guardianRouter,
});

export type AppRouter = typeof appRouter;
