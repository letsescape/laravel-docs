import React, {type ReactNode} from 'react';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function PreviewSection(): ReactNode {
  return (
    <section>
      <div className={styles.container}>
        <div className={styles.splitLayout}>
          <div className={styles.splitText}>
            <div className={styles.sectionHeader}>
              <p className={styles.sectionLabel}>Preview Environments</p>
              <h2 className={styles.sectionTitle}>
                팀(또는 에이전트)의 PR을
                <br />
                프리뷰 환경에서 확인하세요
              </h2>
              <p className={styles.sectionDescription}>
                제로 리스크, 프로덕션과 동일한 환경에서 풀 리퀘스트를 검토하세요.
                GitHub Actions 통합과 안전한 마이그레이션 테스트를 지원합니다.
              </p>
            </div>
            <ul className={styles.featureList}>
              <li>프로덕션과 동일한 환경</li>
              <li>GitHub Actions 통합</li>
              <li>안전한 마이그레이션 테스트</li>
            </ul>
            <Link className={styles.ctaLink} to="/docs/12.x">
              Preview Environments 살펴보기
            </Link>
          </div>

          <div className={styles.splitVisual}>
            <div style={{textAlign: 'center', padding: '2rem', color: 'var(--ifm-font-color-secondary)'}}>
              <div style={{fontSize: '3rem', marginBottom: '1rem'}}>🔍</div>
              <p style={{fontFamily: 'monospace', fontSize: '0.8125rem'}}>
                pr-42.laravel.cloud
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
