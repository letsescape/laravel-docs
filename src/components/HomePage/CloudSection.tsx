import React, {type ReactNode} from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function CloudSection(): ReactNode {
  return (
    <section className={styles.sectionAlt}>
      <div className={styles.container}>
        <div className={styles.splitLayout}>
          <div className={styles.splitText}>
            <div className={styles.sectionHeader}>
              <p className={styles.sectionLabel}>Laravel Cloud</p>
              <h2 className={styles.sectionTitle}>
                로컬에서 라이브까지
                <br />
                몇 초 만에
              </h2>
              <p className={styles.sectionDescription}>
                Laravel Cloud는 자동 스케일링, 제로 다운타임 배포, 그리고 서버리스 인프라를 제공합니다.
                대시보드에서 모든 것을 제어할 수 있습니다.
              </p>
            </div>
            <ul className={styles.featureList}>
              <li>대시보드에서 완전한 제어</li>
              <li>리소스 즉시 추가</li>
              <li>자동 스케일링</li>
              <li>제로 다운타임 배포</li>
            </ul>
            <Link className={styles.ctaLink} to="/docs/12.x">
              Laravel Cloud 살펴보기
            </Link>
          </div>

          <div className={styles.splitVisual}>
            <div style={{textAlign: 'center', padding: '2rem', color: 'var(--ifm-font-color-secondary)'}}>
              <div style={{fontSize: '3rem', marginBottom: '1rem'}}>☁️</div>
              <p style={{fontFamily: 'monospace', fontSize: '0.875rem'}}>
                Idling → Scaling up → Scaling down
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
