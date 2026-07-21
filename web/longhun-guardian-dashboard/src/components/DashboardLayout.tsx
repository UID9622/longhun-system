/**
 * 龍魂操作台布局
 * DNA: #龍芯⚡️2026-07-11-LONGHUN-DASHBOARD-LAYOUT-v1.0
 */
import { useAuth } from "@/hooks/useAuth";
import { trpc } from "@/providers/trpc";
import { useNavigate, useLocation, Link } from "react-router";
import { useEffect, useState } from "react";
import {
  Shield, Key, FileText, Users, Cog, ScrollText,
  Cpu, Activity, Lock, LogOut, Menu, X, ChevronRight,
  BrainCircuit, Smartphone, Fingerprint, CreditCard, DollarSign,
  Beaker, Sword
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";

const navItems = [
  { path: "/dashboard", label: "仪表盘", icon: Activity },
  { path: "/dashboard/content", label: "内容管理", icon: FileText },
  { path: "/dashboard/persona", label: "人格助手", icon: BrainCircuit },
  { path: "/dashboard/devices", label: "设备证书", icon: Smartphone },
  { path: "/dashboard/smkeys", label: "国密密钥", icon: Fingerprint },
  { path: "/dashboard/intake", label: "容器收入口", icon: Beaker },
  { path: "/dashboard/guardian", label: "龍魂守护", icon: Sword },
  { path: "/dashboard/recharge", label: "e-CNY充值", icon: CreditCard },
  { path: "/dashboard/payments", label: "支付管理", icon: DollarSign },
  { path: "/dashboard/audit", label: "审计日志", icon: ScrollText },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, isAuthenticated, isLoading, logout } = useAuth({
    redirectOnUnauthenticated: true,
  });
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  const { data: stats } = trpc.admin.dashboardStats.useQuery(undefined, {
    enabled: isAuthenticated && user?.role === "admin",
  });

  if (isLoading) {
    return (
      <div className="flex h-screen w-screen items-center justify-center bg-slate-950">
        <div className="text-center">
          <Shield className="mx-auto h-12 w-12 animate-pulse text-amber-500" />
          <p className="mt-4 text-lg text-slate-300">龙魂操作台启动中...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) return null;

  const Sidebar = () => (
    <div className="flex h-full flex-col bg-slate-900 border-r border-slate-800">
      {/* Header */}
      <div className="p-4">
        <div className="flex items-center gap-3">
          <Shield className="h-8 w-8 text-amber-500" />
          <div>
            <h1 className="text-lg font-bold text-white tracking-wider">龍魂操作台</h1>
            <p className="text-[10px] text-slate-500 font-mono">LONGHUN PANEL v5.0</p>
          </div>
        </div>
        <div className="mt-3 flex items-center gap-2">
          <Badge
            variant={user?.role === "admin" ? "default" : "secondary"}
            className="text-[10px] bg-amber-600 hover:bg-amber-700"
          >
            <Lock className="mr-1 h-3 w-3" />
            {user?.role === "admin" ? "超级管理员" : "普通用户"}
          </Badge>
          <span className="text-[10px] text-slate-400 truncate">{user?.name}</span>
        </div>
      </div>

      <Separator className="bg-slate-800" />

      {/* Nav */}
      <nav className="flex-1 overflow-y-auto p-3 space-y-1">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          const Icon = item.icon;
          return (
            <Link
              key={item.path}
              to={item.path}
              onClick={() => setMobileOpen(false)}
              className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm transition-all ${
                isActive
                  ? "bg-amber-600/20 text-amber-400 border border-amber-600/30"
                  : "text-slate-300 hover:bg-slate-800 hover:text-white"
              }`}
            >
              <Icon className="h-4 w-4" />
              <span className="flex-1">{item.label}</span>
              {isActive && <ChevronRight className="h-4 w-4" />}
            </Link>
          );
        })}
      </nav>

      <Separator className="bg-slate-800" />

      {/* Footer */}
      <div className="p-3 space-y-2">
        {stats && (
          <div className="rounded-lg bg-slate-800/50 p-2 space-y-1">
            <div className="flex justify-between text-[10px] text-slate-400">
              <span>用户</span><span className="text-amber-400">{stats.stats.users}</span>
            </div>
            <div className="flex justify-between text-[10px] text-slate-400">
              <span>设备</span><span className="text-amber-400">{stats.stats.devices}</span>
            </div>
            <div className="flex justify-between text-[10px] text-slate-400">
              <span>技能</span><span className="text-amber-400">{stats.stats.skills}</span>
            </div>
          </div>
        )}
        <Button
          variant="ghost"
          size="sm"
          onClick={logout}
          className="w-full justify-start text-slate-400 hover:text-red-400 hover:bg-red-900/20"
        >
          <LogOut className="mr-2 h-4 w-4" />
          安全登出
        </Button>
        <p className="text-[9px] text-slate-600 text-center font-mono">
          DNA: #龍芯⚡️2026-07-11
        </p>
      </div>
    </div>
  );

  return (
    <div className="flex h-screen w-screen bg-slate-950 text-slate-100 overflow-hidden">
      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex w-64 flex-shrink-0">
        <Sidebar />
      </aside>

      {/* Mobile Sidebar */}
      <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
        <SheetTrigger asChild className="lg:hidden fixed top-4 left-4 z-50">
          <Button variant="outline" size="icon" className="bg-slate-900 border-slate-700">
            <Menu className="h-4 w-4" />
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-64 p-0 border-slate-800">
          <Sidebar />
        </SheetContent>
      </Sheet>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <div className="p-4 lg:p-6 min-h-screen">
          {children}
        </div>
      </main>
    </div>
  );
}
