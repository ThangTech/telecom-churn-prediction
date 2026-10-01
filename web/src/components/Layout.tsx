import type { PropsWithChildren } from 'react';
import { NavLink } from 'react-router-dom';

const navigation = [
  { to: '/', label: 'Giới thiệu', end: true },
  { to: '/predict', label: 'Dự đoán' },
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/model-card', label: 'Model Card' },
];

export function Layout({ children }: PropsWithChildren) {
  return (
    <div className="app-shell">
      <header className="topbar">
        <NavLink className="brand" to="/" aria-label="ChurnCare - Trang chủ">
          <span className="brand-mark" aria-hidden="true">C</span>
          <span><strong>ChurnCare</strong><small>Telecom intelligence</small></span>
        </NavLink>
        <nav aria-label="Điều hướng chính">
          {navigation.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <span className="system-pill"><span /> Week 5 · Frontend</span>
      </header>
      <main>{children}</main>
      <footer>
        <span>Đề 15 · Iranian Churn Dataset</span>
        <span>Công cụ hỗ trợ quyết định — cần có giám sát của con người</span>
      </footer>
    </div>
  );
}
