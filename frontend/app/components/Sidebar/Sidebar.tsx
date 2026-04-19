import styles from './Sidebar.module.css';
import { LayoutDashboard, BarChart2, PieChart, Briefcase, Settings } from 'lucide-react';

export default function Sidebar() {
  return (
    <aside className={styles.sidebar}>
      <div className={styles.logoArea}>
        <div className={styles.logoTitle}>HDFC AMC</div>
        <div>
          <div className={styles.portalTitle}>Investment Portal</div>
          <div className={styles.premiumTier}>Premium Tier</div>
        </div>
      </div>
      
      <nav className={styles.nav}>
        <ul className={styles.navList}>
          <li className={`${styles.navItem} ${styles.active}`}>
            <LayoutDashboard size={20} />
            <span>Dashboard</span>
          </li>
          <li className={styles.navItem}>
            <BarChart2 size={20} />
            <span>Mutual Funds</span>
          </li>
          <li className={styles.navItem}>
            <PieChart size={20} />
            <span>Stock Portfolio</span>
          </li>
          <li className={styles.navItem}>
            <Briefcase size={20} />
            <span>Wealth Basket</span>
          </li>
          <li className={styles.navItem}>
            <Settings size={20} />
            <span>Settings</span>
          </li>
        </ul>
      </nav>
    </aside>
  );
}
