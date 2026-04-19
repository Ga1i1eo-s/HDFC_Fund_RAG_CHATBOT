import styles from './Dashboard.module.css';
import { ArrowRight, TrendingUp } from 'lucide-react';

export default function DashboardContent() {
  return (
    <div className={styles.dashboard}>
      <div className={styles.topSection}>
        <div className={styles.stockInfo}>
          <div className={styles.ticker}>NSE: HDFCAMC</div>
          <div className={styles.price}>₹3,942.50</div>
          <div className={styles.change}>
            <TrendingUp size={16} className={styles.changeIcon} />
            <span>+₹114.20 (2.98%)</span>
            <span className={styles.timeText}>Today</span>
          </div>
        </div>
        
        <div className={styles.chartContainer}>
          <div className={styles.chartFilters}>
            <button className={`${styles.filterBtn} ${styles.active}`}>1D</button>
            <button className={styles.filterBtn}>1W</button>
            <button className={styles.filterBtn}>1M</button>
            <button className={styles.filterBtn}>1Y</button>
          </div>
          {/* A simple SVG curve matching the sparkline */}
          <svg className={styles.chartSvg} viewBox="0 0 400 100" preserveAspectRatio="none">
            <defs>
              <linearGradient id="gradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="rgba(11, 63, 136, 0.2)" />
                <stop offset="100%" stopColor="rgba(11, 63, 136, 0)" />
              </linearGradient>
            </defs>
            <path
              d="M0,80 C50,70 100,85 150,70 C200,55 250,20 300,30 C350,40 380,10 400,20 L400,100 L0,100 Z"
              fill="url(#gradient)"
            />
            <path
              d="M0,80 C50,70 100,85 150,70 C200,55 250,20 300,30 C350,40 380,10 400,20"
              fill="none"
              stroke="var(--primary-color)"
              strokeWidth="3"
            />
          </svg>
        </div>
      </div>

      <div className={styles.statsGrid}>
        <div className={styles.statCard}>
          <div className={styles.statLabel}>AUM</div>
          <div className={styles.statValue}>₹6.12L Cr</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statLabel}>P/E RATIO</div>
          <div className={styles.statValue}>42.4</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statLabel}>MARKET CAP</div>
          <div className={styles.statValue}>₹84,200 Cr</div>
        </div>
        <div className={styles.statCard}>
          <div className={styles.statLabel}>DIVIDEND YIELD</div>
          <div className={styles.statValue}>1.76%</div>
        </div>
      </div>

      <div className={styles.aboutSection}>
        <h2 className={styles.sectionTitle}>About HDFC AMC</h2>
        <p className={styles.aboutText}>
          HDFC Asset Management Company Ltd is one of India's largest and most profitable mutual fund managers. 
          As a joint venture between HDFC Bank and abrdn Investment Management, we provide comprehensive suite 
          of savings and investment products across asset classes, ensuring precision and transparency in every portfolio.
        </p>
        <button className={styles.linkBtn}>
          View Annual Report <ArrowRight size={16} />
        </button>
      </div>

      <div className={styles.fundsSection}>
        <h2 className={styles.sectionTitle}>Top Performing Funds</h2>
        <div className={styles.fundsSubtitle}>Direct Plans • Growth Option</div>
        
        <table className={styles.fundsTable}>
          <thead>
            <tr>
              <th>FUND NAME</th>
              <th>CATEGORY</th>
              <th>NAV</th>
              <th>1Y RETURN</th>
            </tr>
          </thead>
          <tbody>
            <tr className={styles.fundsRow}>
              <td>
                <div className={styles.fundName}>HDFC Top 100 Fund</div>
                <div className={styles.fundType}>Large Cap Fund</div>
              </td>
              <td><span className={`${styles.badge} ${styles.equity}`}>EQUITY</span></td>
              <td className={styles.navValue}>₹1,124.45</td>
              <td className={styles.return}>24.2% p.a.</td>
            </tr>
            <tr className={styles.fundsRow}>
              <td>
                <div className={styles.fundName}>HDFC Mid-Cap Opportunities</div>
                <div className={styles.fundType}>Mid Cap Fund</div>
              </td>
              <td><span className={`${styles.badge} ${styles.equity}`}>EQUITY</span></td>
              <td className={styles.navValue}>₹182.12</td>
              <td className={styles.return}>31.8% p.a.</td>
            </tr>
            <tr className={styles.fundsRow}>
              <td>
                <div className={styles.fundName}>HDFC Hybrid Equity Fund</div>
                <div className={styles.fundType}>Aggressive Hybrid</div>
              </td>
              <td><span className={`${styles.badge} ${styles.hybrid}`}>HYBRID</span></td>
              <td className={styles.navValue}>₹98.40</td>
              <td className={styles.return}>19.5% p.a.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
