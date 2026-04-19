import styles from './FloatingCTA.module.css';

export default function FloatingCTA() {
  return (
    <div className={styles.ctaContainer}>
      <div className={styles.ctaText}>Ready to grow?</div>
      <button className={styles.ctaBtn}>Invest Now</button>
    </div>
  );
}
