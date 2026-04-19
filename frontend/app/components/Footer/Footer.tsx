import styles from './Footer.module.css';
import { Share2, Mail } from 'lucide-react';
import Link from 'next/link';

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.links}>
        <Link href="#" className={styles.link}>Disclosures</Link>
        <Link href="#" className={styles.link}>Privacy Policy</Link>
        <Link href="#" className={styles.link}>Terms of Service</Link>
        <Link href="#" className={styles.link}>SEBI Compliance</Link>
      </div>
      
      <div>
        <div className={styles.company}>HDFC AMC Ltd.</div>
        <div className={styles.copyright}>© 2024 HDFC Asset Management Company Ltd. All rights reserved.</div>
      </div>
      
      <div className={styles.social}>
        <button className={styles.socialBtn}><Share2 size={16} /></button>
        <button className={styles.socialBtn}><Mail size={16} /></button>
      </div>
    </footer>
  );
}
