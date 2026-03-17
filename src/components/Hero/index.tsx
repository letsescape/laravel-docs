import React, {type ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function Hero(): ReactNode {
  return (
    <section className={styles.hero}>
      <div className={styles.heroBackground} />
      <div className="container">
        <div className={styles.heroInner}>
          <div className={styles.heroContent}>
            <h1 className={styles.heroTitle}>
              <span className={styles.heroTitleHighlight}>생산성을 위해 만들어진 도구</span>로
              소프트웨어 개발하기
            </h1>
            <p className={styles.heroSubtitle}>
              라라벨은 웹 장인을 위한 완벽한 생태계를 제공합니다. 오픈 소스 PHP 프레임워크, 제품,
              패키지 및 스타터 킷은 웹 애플리케이션을 구축, 배포 및 모니터링하는 데 필요한
              모든 것을 제공합니다.
            </p>
            <div className={styles.heroButtons}>
              <Link
                className={clsx(styles.heroButton, styles.heroButtonPrimary)}
                to="/docs/12.x">
                시작하기
              </Link>
              <Link
                className={clsx(styles.heroButton, styles.heroButtonSecondary)}
                to="/docs/12.x/installation">
                설치 가이드
              </Link>
            </div>
          </div>
          <div className={styles.codeSnippet}>
            <div className={styles.codeHeader}>
              <div className={styles.codeDots}>
                <span className={styles.codeDot} />
                <span className={styles.codeDot} />
                <span className={styles.codeDot} />
              </div>
              <span className={styles.codeHeaderTitle}>Terminal</span>
            </div>
            <pre className={styles.codeBlock}>
              <code>
                <span className={styles.codeLine}>
                  <span className={styles.codePrompt}>$</span> composer global require laravel/installer
                </span>
                <span className={styles.codeLine}>
                  <span className={styles.codePrompt}>$</span> laravel new example-app
                </span>
                <span className={styles.codeLine}>&nbsp;</span>
                <span className={clsx(styles.codeLine, styles.codeComment)}>
                  # 모든 준비가 완료되었습니다. 🚀
                </span>
              </code>
            </pre>
          </div>
        </div>
      </div>
    </section>
  );
}
