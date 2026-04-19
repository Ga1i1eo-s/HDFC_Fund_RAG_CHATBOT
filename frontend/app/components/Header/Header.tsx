import styles from './Header.module.css';
import { Search, Bell, User } from 'lucide-react';
import Link from 'next/link';

export default function Header() {
  return (
    <header className={styles.header}>
      <nav className={styles.leftNav}>
        <Link href="#" className={`${styles.navLink} ${styles.active}`}>Portfolio</Link>
        <Link href="#" className={styles.navLink}>Investments</Link>
        <Link href="#" className={styles.navLink}>Insights</Link>
        <Link href="#" className={styles.navLink}>Support</Link>
      </nav>
      
      <div className={styles.rightControls}>
        <div className={styles.searchContainer}>
          <Search size={18} className={styles.searchIcon} />
          <input type="text" placeholder="Search funds..." className={styles.searchInput} />
        </div>
        <button className={styles.iconBtn} aria-label="Notifications">
          <Bell size={20} />
        </button>
        <button className={styles.iconBtn} aria-label="Profile">
          <User size={20} />
        </button>
      </div>
    </header>
  );
}
